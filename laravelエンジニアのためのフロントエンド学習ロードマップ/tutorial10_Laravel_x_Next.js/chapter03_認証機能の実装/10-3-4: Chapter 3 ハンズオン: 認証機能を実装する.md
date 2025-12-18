# 10-3-4: Chapter 3 ハンズオン: 認証機能を実装する

## 🎯 このハンズオンで作るもの

このハンズオンでは、Laravel SanctumとNextAuth.jsを使って、**フルスタックの認証機能**を実装します。

**完成イメージ:**
- ログインフォーム（メールアドレス・パスワード）
- ログイン状態の表示（ユーザー名、ログアウトボタン）
- 認証が必要なページの保護
- ログアウト機能

## 前提条件

- Chapter 1で構築した開発環境（Laravel Sail + Next.js）が動作していること
- Chapter 2で作成した商品一覧ページが完成していること
- 10-3-1〜10-3-3のセクションを完了していること

## Step 1: Laravel側の認証APIを確認

10-3-1で設定したLaravel Sanctumの認証エンドポイントを確認します。

### 1.1 ルートの確認

`routes/api.php`に以下のルートが設定されていることを確認します。

```php
<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;

// 認証不要のルート
Route::post('/login', [AuthController::class, 'login']);
Route::post('/register', [AuthController::class, 'register']);

// 認証が必要なルート
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/user', function (Request $request) {
        return $request->user();
    });
    Route::post('/logout', [AuthController::class, 'logout']);
});
```

### 1.2 AuthControllerの確認

`app/Http/Controllers/AuthController.php`の内容を確認します。

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

class AuthController extends Controller
{
    public function login(Request $request)
    {
        $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);

        $user = User::where('email', $request->email)->first();

        if (!$user || !Hash::check($request->password, $user->password)) {
            throw ValidationException::withMessages([
                'email' => ['認証情報が正しくありません。'],
            ]);
        }

        $token = $user->createToken('auth-token')->plainTextToken;

        return response()->json([
            'user' => $user,
            'token' => $token,
        ]);
    }

    public function logout(Request $request)
    {
        $request->user()->currentAccessToken()->delete();

        return response()->json(['message' => 'ログアウトしました']);
    }

    public function register(Request $request)
    {
        $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|email|unique:users',
            'password' => 'required|min:8|confirmed',
        ]);

        $user = User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => Hash::make($request->password),
        ]);

        $token = $user->createToken('auth-token')->plainTextToken;

        return response()->json([
            'user' => $user,
            'token' => $token,
        ]);
    }
}
```

### 1.3 テストユーザーの作成

Seederを使ってテストユーザーを作成します。

```bash
# Laravelコンテナに入る
docker compose exec laravel.test bash

# Seederを実行
php artisan db:seed
```

`database/seeders/DatabaseSeeder.php`にテストユーザーを追加しておきます。

```php
<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        User::create([
            'name' => 'テストユーザー',
            'email' => 'test@example.com',
            'password' => Hash::make('password'),
        ]);
    }
}
```

## Step 2: Next.js側の認証設定

### 2.1 NextAuth.jsの設定確認

10-3-2で設定した`app/api/auth/[...nextauth]/route.ts`を確認します。

```typescript
import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

const handler = NextAuth({
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        try {
          const res = await fetch(`${process.env.LARAVEL_API_URL}/api/login`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
            body: JSON.stringify({
              email: credentials.email,
              password: credentials.password,
            }),
          });

          if (!res.ok) {
            return null;
          }

          const data = await res.json();

          return {
            id: data.user.id,
            name: data.user.name,
            email: data.user.email,
            accessToken: data.token,
          };
        } catch (error) {
          console.error("Login error:", error);
          return null;
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.accessToken = user.accessToken;
        token.id = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      session.accessToken = token.accessToken;
      session.user.id = token.id;
      return session;
    },
  },
  pages: {
    signIn: "/login",
  },
});

export { handler as GET, handler as POST };
```

### 2.2 型定義の追加

`types/next-auth.d.ts`を作成して、セッションの型を拡張します。

```typescript
import "next-auth";

declare module "next-auth" {
  interface Session {
    accessToken?: string;
    user: {
      id?: string;
      name?: string | null;
      email?: string | null;
    };
  }

  interface User {
    accessToken?: string;
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    accessToken?: string;
    id?: string;
  }
}
```

## Step 3: ログインページの作成

### 3.1 ログインフォームコンポーネント

`app/login/page.tsx`を作成します。

```tsx
"use client";

import { useState } from "react";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const result = await signIn("credentials", {
        email,
        password,
        redirect: false,
      });

      if (result?.error) {
        setError("メールアドレスまたはパスワードが正しくありません");
      } else {
        router.push("/");
        router.refresh();
      }
    } catch (error) {
      setError("ログイン中にエラーが発生しました");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold text-center mb-6">ログイン</h1>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              メールアドレス
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="test@example.com"
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              パスワード
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? "ログイン中..." : "ログイン"}
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-gray-600">
          テストアカウント: test@example.com / password
        </p>
      </div>
    </div>
  );
}
```

## Step 4: 認証状態の表示

### 4.1 ヘッダーコンポーネントの作成

`components/Header.tsx`を作成します。

```tsx
"use client";

import { useSession, signOut } from "next-auth/react";
import Link from "next/link";

export default function Header() {
  const { data: session, status } = useSession();

  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/" className="text-xl font-bold text-gray-800">
          ECサイト
        </Link>

        <nav className="flex items-center gap-4">
          <Link href="/products" className="text-gray-600 hover:text-gray-800">
            商品一覧
          </Link>

          {status === "loading" ? (
            <span className="text-gray-400">読み込み中...</span>
          ) : session ? (
            <div className="flex items-center gap-4">
              <span className="text-gray-600">
                {session.user?.name}さん
              </span>
              <button
                onClick={() => signOut({ callbackUrl: "/" })}
                className="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300 transition-colors"
              >
                ログアウト
              </button>
            </div>
          ) : (
            <Link
              href="/login"
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
            >
              ログイン
            </Link>
          )}
        </nav>
      </div>
    </header>
  );
}
```

### 4.2 SessionProviderの設定

`app/providers.tsx`を作成します。

```tsx
"use client";

import { SessionProvider } from "next-auth/react";

export default function Providers({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>;
}
```

### 4.3 レイアウトの更新

`app/layout.tsx`を更新します。

```tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Providers from "./providers";
import Header from "@/components/Header";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ECサイト",
  description: "Laravel + Next.js ECサイト",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body className={inter.className}>
        <Providers>
          <Header />
          <main>{children}</main>
        </Providers>
      </body>
    </html>
  );
}
```

## Step 5: 認証が必要なページの保護

### 5.1 ミドルウェアの作成

`middleware.ts`をプロジェクトルートに作成します。

```typescript
import { withAuth } from "next-auth/middleware";

export default withAuth({
  pages: {
    signIn: "/login",
  },
});

export const config = {
  matcher: ["/dashboard/:path*", "/profile/:path*"],
};
```

### 5.2 保護されたページの作成

`app/dashboard/page.tsx`を作成します。

```tsx
import { getServerSession } from "next-auth";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await getServerSession();

  if (!session) {
    redirect("/login");
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-4">ダッシュボード</h1>
      <div className="bg-white p-6 rounded-lg shadow">
        <p className="text-gray-600">
          ようこそ、{session.user?.name}さん！
        </p>
        <p className="text-gray-600 mt-2">
          このページは認証されたユーザーのみアクセスできます。
        </p>
      </div>
    </div>
  );
}
```

## Step 6: 動作確認

### 6.1 開発サーバーの起動

```bash
# Laravelの起動（Docker）
docker compose up -d

# Next.jsの起動
cd frontend
npm run dev
```

### 6.2 確認項目

以下の動作を確認します。

| 確認項目 | 期待される動作 |
|:---|:---|
| 未ログイン状態でトップページにアクセス | ヘッダーに「ログイン」ボタンが表示される |
| ログインページでテストアカウントでログイン | ログイン成功後、トップページにリダイレクト |
| ログイン状態でトップページにアクセス | ヘッダーにユーザー名と「ログアウト」ボタンが表示される |
| ログアウトボタンをクリック | ログアウト後、トップページにリダイレクト |
| 未ログイン状態で`/dashboard`にアクセス | ログインページにリダイレクト |
| ログイン状態で`/dashboard`にアクセス | ダッシュボードが表示される |

## トラブルシューティング

### ログインできない場合

1. **Laravel APIが起動しているか確認**
   ```bash
   curl http://localhost/api/login -X POST \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"password"}'
   ```

2. **CORSの設定を確認**
   `config/cors.php`で`allowed_origins`にNext.jsのURLが含まれているか確認

3. **環境変数を確認**
   `.env.local`に`LARAVEL_API_URL`が正しく設定されているか確認

### セッションが保持されない場合

1. **NEXTAUTH_SECRETが設定されているか確認**
   ```bash
   # .env.local
   NEXTAUTH_SECRET=your-secret-key
   NEXTAUTH_URL=http://localhost:3000
   ```

2. **ブラウザのCookieを確認**
   開発者ツール → Application → Cookies で`next-auth.session-token`が存在するか確認

## ✨ まとめ

このハンズオンでは、以下の機能を実装しました。

- **Laravel Sanctum**を使ったトークンベースの認証API
- **NextAuth.js**を使ったNext.js側の認証管理
- **ログインフォーム**の作成
- **認証状態の表示**（ヘッダーコンポーネント）
- **ミドルウェア**による認証が必要なページの保護

これで、LaravelとNext.jsを連携したフルスタックアプリケーションの基本的な認証機能が完成しました。

## 📝 学習のポイント

- [ ] Laravel Sanctumでトークンベースの認証APIを作成できる
- [ ] NextAuth.jsでCredentialsProviderを設定できる
- [ ] ログインフォームを作成し、認証処理を実装できる
- [ ] セッション情報を使って認証状態を表示できる
- [ ] ミドルウェアで認証が必要なページを保護できる

## 🚀 発展課題

- ユーザー登録機能を追加する
- パスワードリセット機能を追加する
- ソーシャルログイン（Google, GitHub）を追加する
- 認証エラーのバリデーションメッセージを詳細化する
