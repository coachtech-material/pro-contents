# 9-1-5: Chapter 1 ハンズオン: Next.jsプロジェクトを作成する

## 🎯 このハンズオンの目的

このハンズオンでは、Next.jsプロジェクトを作成し、基本的なページとレイアウトを実装します。Server ComponentsとClient Componentsの使い分けを実践しながら、Next.jsの基本的な開発フローを体験しましょう。

## Step 1: プロジェクトの作成

まず、新しいNext.jsプロジェクトを作成します。

```bash
npx create-next-app@latest nextjs-practice --typescript --tailwind --eslint --app --turbopack
cd nextjs-practice
npm run dev
```

ブラウザで `http://localhost:3000` にアクセスし、Next.jsのウェルカムページが表示されることを確認します。

## Step 2: トップページの作成

`app/page.tsx`を以下のように編集します。

```typescript
import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold mb-8">Next.js Practice</h1>
      
      <nav className="space-y-4">
        <Link 
          href="/about" 
          className="block p-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          About Page →
        </Link>
        <Link 
          href="/counter" 
          className="block p-4 bg-green-500 text-white rounded-lg hover:bg-green-600"
        >
          Counter Page (Client Component) →
        </Link>
        <Link 
          href="/users" 
          className="block p-4 bg-purple-500 text-white rounded-lg hover:bg-purple-600"
        >
          Users Page (Server Component) →
        </Link>
      </nav>
    </main>
  );
}
```

## Step 3: レイアウトの設定

`app/layout.tsx`を編集して、共通のヘッダーを追加します。

```typescript
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Link from 'next/link';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Next.js Practice',
  description: 'Next.jsの学習用プロジェクト',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body className={inter.className}>
        <header className="bg-gray-800 text-white p-4">
          <nav className="max-w-4xl mx-auto flex gap-4">
            <Link href="/" className="hover:text-gray-300">Home</Link>
            <Link href="/about" className="hover:text-gray-300">About</Link>
            <Link href="/counter" className="hover:text-gray-300">Counter</Link>
            <Link href="/users" className="hover:text-gray-300">Users</Link>
          </nav>
        </header>
        <div className="max-w-4xl mx-auto">
          {children}
        </div>
      </body>
    </html>
  );
}
```

## Step 4: Aboutページの作成（Server Component）

`app/about/page.tsx`を作成します。

```typescript
export default function AboutPage() {
  // Server Componentなので、サーバー上で実行される
  console.log('This runs on the server');
  
  return (
    <main className="p-8">
      <h1 className="text-3xl font-bold mb-4">About</h1>
      <p className="text-gray-600 mb-4">
        これはServer Componentです。サーバー上でレンダリングされ、
        クライアントにはHTMLのみが送信されます。
      </p>
      <p className="text-gray-600">
        ビルド時刻: {new Date().toLocaleString('ja-JP')}
      </p>
    </main>
  );
}
```

## Step 5: Counterページの作成（Client Component）

`app/counter/page.tsx`を作成します。

```typescript
'use client';

import { useState } from 'react';

export default function CounterPage() {
  const [count, setCount] = useState(0);

  return (
    <main className="p-8">
      <h1 className="text-3xl font-bold mb-4">Counter</h1>
      <p className="text-gray-600 mb-4">
        これはClient Componentです。&apos;use client&apos;ディレクティブにより、
        クライアント側でインタラクティブに動作します。
      </p>
      
      <div className="flex items-center gap-4 mt-8">
        <button
          onClick={() => setCount(count - 1)}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
        >
          -1
        </button>
        <span className="text-4xl font-bold">{count}</span>
        <button
          onClick={() => setCount(count + 1)}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          +1
        </button>
      </div>
    </main>
  );
}
```

## Step 6: Usersページの作成（Server Componentでのデータ取得）

`app/users/page.tsx`を作成します。

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  company: {
    name: string;
  };
}

async function getUsers(): Promise<User[]> {
  const res = await fetch('https://jsonplaceholder.typicode.com/users');
  if (!res.ok) {
    throw new Error('Failed to fetch users');
  }
  return res.json();
}

export default async function UsersPage() {
  const users = await getUsers();

  return (
    <main className="p-8">
      <h1 className="text-3xl font-bold mb-4">Users</h1>
      <p className="text-gray-600 mb-4">
        これはServer Componentでのデータ取得の例です。
        fetchはサーバー上で実行され、結果がHTMLとしてクライアントに送信されます。
      </p>
      
      <ul className="space-y-4">
        {users.map((user) => (
          <li 
            key={user.id}
            className="p-4 border rounded-lg hover:bg-gray-50"
          >
            <h2 className="font-bold">{user.name}</h2>
            <p className="text-gray-600">{user.email}</p>
            <p className="text-sm text-gray-500">{user.company.name}</p>
          </li>
        ))}
      </ul>
    </main>
  );
}
```

## Step 7: 動作確認

開発サーバーが起動していることを確認し、以下のページにアクセスしてみましょう。

- `http://localhost:3000` - トップページ
- `http://localhost:3000/about` - Aboutページ（Server Component）
- `http://localhost:3000/counter` - Counterページ（Client Component）
- `http://localhost:3000/users` - Usersページ（Server Componentでのデータ取得）

## ✨ まとめ

このハンズオンでは、以下のことを実践しました。

- Next.jsプロジェクトの作成と基本的なディレクトリ構造の理解
- `layout.tsx`を使った共通レイアウトの実装
- Server Component（デフォルト）の作成
- `'use client'`ディレクティブを使ったClient Componentの作成
- Server Componentでの非同期データ取得

Server ComponentsとClient Componentsの使い分けを理解することで、パフォーマンスの高いNext.jsアプリケーションを構築できます。次のチャプターでは、ルーティングとデータ取得についてより詳しく学んでいきましょう。
