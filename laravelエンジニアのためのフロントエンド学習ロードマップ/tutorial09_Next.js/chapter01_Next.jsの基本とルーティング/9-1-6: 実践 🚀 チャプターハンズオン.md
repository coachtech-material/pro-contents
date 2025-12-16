# Tutorial 9: Next.js

## Chapter 1: Next.jsの基本とルーティング

### Chapter 1 ハンズオン: シンプルなブログを作成する

🎯 **このハンズオンで達成すること**

-   ファイルベースルーティングを使って、複数のページを持つアプリケーションを構築できるようになる。
-   静的ルート（`/`）、ネストされたルート（`/about`）、動的ルート（`/posts/[id]`）を実際に作成する。
-   `Link`コンポーネントを使って、ページ間のクライアントサイドナビゲーションを実装する。
-   `layout.tsx`を使って、全ページ共通のヘッダーとフッターを配置する。
-   `generateMetadata`を使って、記事詳細ページのタイトルを動的に設定する。

--- 

🖼️ **完成イメージ**

3つのページを持つシンプルなブログサイトを作成します。

1.  **トップページ (`/`)**: 記事の一覧と、各記事へのリンクが表示される。
2.  **Aboutページ (`/about`)**: このサイトについての説明ページ。
3.  **記事詳細ページ (`/posts/[id]`)**: 個別の記事の内容が表示される。

全ページに共通のヘッダーとフッターが表示されます。

![完成イメージ](https://placehold.jp/800x600.png?text=ブログサイト%0A---%0Aヘッダー%0A---%0A%0A[トップページ]%0A記事一覧%0A・記事1へ%0A・記事2へ%0A%0A[記事詳細ページ]%0A記事タイトル%0A記事本文...%0A%0A---%0Aフッター)

--- 

### 🧠 先輩エンジニアの思考プロセス

「Next.jsで簡単なブログ作って」と言われたら、こう考える。

1.  **プロジェクトのセットアップ:**
    -   まずは`create-next-app`でプロジェクトの雛形を作る。TypeScript, Tailwind, `src/`, App Routerは全部Yesだ。
2.  **ページの洗い出しとルーティング設計:**
    -   必要なページは3つ。トップ、About、記事詳細。
    -   トップページ: `src/app/page.tsx`が対応する。
    -   Aboutページ: `src/app/about/page.tsx`を作成すればOK。
    -   記事詳細ページ: URLは`/posts/1`, `/posts/2`のようにしたい。これは動的ルートだな。`src/app/posts/[id]/page.tsx`を作成しよう。
3.  **共通レイアウトの作成:**
    -   全ページでヘッダーとフッターを使いたい。これは`src/app/layout.tsx`で実装するのが定石だ。
    -   `Header`と`Footer`コンポーネントを`src/components`に作って、それを`RootLayout`で読み込もう。
4.  **トップページの実装:**
    -   記事の一覧を表示したい。まずはダミーのブログ投稿データを配列として用意しよう。
    -   そのデータを`map`でループさせて、各記事への`Link`コンポーネントを生成する。
5.  **記事詳細ページの実装:**
    -   `params`から記事IDを取得する。
    -   ダミーデータの中から、IDが一致する記事を探し出して表示する。
    -   もし存在しないIDがURLで指定されたら、「記事が見つかりません」と表示したい。Next.jsには`notFound()`という便利な関数があるから、それを使おう。
6.  **メタデータ（SEO）の設定:**
    -   サイト全体のタイトルは`layout.tsx`で設定する。`title.template`を使うと便利だ。
    -   記事詳細ページでは、記事のタイトルをページの`<title>`にしたい。`generateMetadata`関数を使って、`params.id`から記事データを取得して動的にタイトルを生成しよう。

--- 

### 🏃 実践: Step by Stepで実装しよう

#### Step 1: プロジェクトの作成

```bash
npx create-next-app@latest blog-tutorial
```

質問にはすべて推奨設定（Yes）で答えてください。作成後、`cd blog-tutorial`でディレクトリに移動します。

#### Step 2: 共通レイアウトの作成

まず、`src/components`フォルダを作成し、その中に`Header.tsx`と`Footer.tsx`を作成します。

```tsx
// src/components/Header.tsx
import Link from "next/link";

export default function Header() {
  return (
    <header className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between">
        <Link href="/" className="font-bold text-xl">My Blog</Link>
        <nav className="space-x-4">
          <Link href="/">Home</Link>
          <Link href="/about">About</Link>
        </nav>
      </div>
    </header>
  );
}
```

```tsx
// src/components/Footer.tsx
export default function Footer() {
  return (
    <footer className="bg-gray-800 text-white p-4 text-center mt-8">
      <p>© 2025 My Blog. All rights reserved.</p>
    </footer>
  );
}
```

次に、`src/app/layout.tsx`を編集して、これらのコンポーネントを組み込み、メタデータを設定します。

```tsx
// src/app/layout.tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: {
    default: "My Awesome Blog",
    template: "%s | My Awesome Blog",
  },
  description: "A simple blog created with Next.js",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body className={inter.className}>
        <div className="flex flex-col min-h-screen">
          <Header />
          <main className="flex-grow container mx-auto p-4">{children}</main>
          <Footer />
        </div>
      </body>
    </html>
  );
}
```

#### Step 3: トップページ（記事一覧）の作成

`src/app/page.tsx`を編集します。

```tsx
// src/app/page.tsx
import Link from "next/link";

// ダミーの投稿データ
const posts = [
  { id: "1", title: "Next.js入門", body: "..." },
  { id: "2", title: "TypeScriptの基本", body: "..." },
  { id: "3", title: "Tailwind CSSはいいぞ", body: "..." },
];

export default function HomePage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">記事一覧</h1>
      <ul className="space-y-2">
        {posts.map((post) => (
          <li key={post.id}>
            <Link href={`/posts/${post.id}`} className="text-blue-500 hover:underline">
              {post.title}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

#### Step 4: Aboutページの作成

`src/app/about/page.tsx`を作成します。

```tsx
// src/app/about/page.tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About",
};

export default function AboutPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">このサイトについて</h1>
      <p>これはNext.jsの学習のために作成されたブログです。</p>
    </div>
  );
}
```

#### Step 5: 記事詳細ページの作成

`src/app/posts/[id]/page.tsx`を作成します。

```tsx
// src/app/posts/[id]/page.tsx
import type { Metadata } from "next";
import { notFound } from "next/navigation";

// ダミーの投稿データ（実際はAPIなどから取得）
const posts = [
  { id: "1", title: "Next.js入門", body: "Next.jsはReactベースのフレームワークです。" },
  { id: "2", title: "TypeScriptの基本", body: "TypeScriptはJavaScriptに型を付けた言語です。" },
  { id: "3", title: "Tailwind CSSはいいぞ", body: "Tailwind CSSを使うとデザインが早くなります。" },
];

// メタデータを動的に生成
export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const post = posts.find((p) => p.id === params.id);
  if (!post) {
    return { title: "記事が見つかりません" };
  }
  return { title: post.title, description: post.body.slice(0, 120) };
}

export default function PostDetailPage({ params }: { params: { id: string } }) {
  const post = posts.find((p) => p.id === params.id);

  // 記事が見つからない場合は404ページを表示
  if (!post) {
    notFound();
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">{post.title}</h1>
      <p>{post.body}</p>
    </div>
  );
}
```

これで完成です！`npm run dev`で開発サーバーを起動し、`http://localhost:3000`にアクセスして、各ページが正しく表示され、リンクが機能することを確認してください。`/posts/4`のように存在しないIDにアクセスすると、Next.jsのデフォルトの404ページが表示されるはずです。

--- 

✨ **まとめ**

-   `app`ディレクトリのフォルダ構造を操作するだけで、直感的にルーティングを構築できた。
-   `layout.tsx`に共通コンポーネントを配置することで、一貫したUIを簡単に実現できた。
-   `Link`コンポーネントにより、リロードのない高速なページ遷移が実現できた。
-   動的ルート`[id]`と`params` Propsを使って、URLに応じたコンテンツの出し分けができた。
-   `generateMetadata`関数を使い、動的なデータに基づいた`<title>`タグの生成に成功した。
