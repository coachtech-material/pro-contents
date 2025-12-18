
# Col-3-1: React Server Components (RSC) のアーキテクチャ

## 🎯 このセクションで学ぶこと

-   React Server Components (RSC) が解決する課題を理解する。
-   Server Components と Client Components の役割と違いを明確に区別する。
-   RSCのアーキテクチャと、SSRとの違いを理解する。
-   Next.js App Router における RSC の基本ルールを学ぶ。

## 導入: なぜRSCが生まれたのか？

これまでのレンダリング戦略（CSR, SSR, SSG）は、**「どこで（クライアント or サーバー）HTMLを生成するか」** という問いに対する答えでした。しかし、これらのアプローチには共通の課題がありました。

1.  **JavaScriptバンドルサイズの肥大化**: アプリケーションがリッチになるほど、クライアントに送信するJavaScriptの量が増え、初期ロードとインタラクティブになるまでの時間（TTI）が長くなる。
2.  **サーバーとクライアントの断絶**: クライアントでデータを表示するためには、必ずAPIエンドポイントを作成し、`fetch`でデータを取得する必要がある。これにより、開発者は常にクライアントとサーバーの両方を意識する必要があった。

**React Server Components (RSC)** は、これらの課題を解決するためにReactチームが提案した新しいアーキテクチャです。これは単なるレンダリング戦略ではなく、Reactアプリケーションの作り方を根本から変えるパラダイムシフトです。[1]

## Server Components vs Client Components

RSCのアーキテクチャでは、コンポーネントは2種類に大別されます。

1.  **Server Components (サーバーコンポーネント)**
2.  **Client Components (クライアントコンポーネント)**

Next.jsのApp Routerでは、**デフォルトですべてのコンポーネントがServer Components**として扱われます。

### Server Components

サーバーコンポーネントは、その名の通り**サーバーでのみ**実行されるコンポーネントです。そのコードはクライアントに送信されません。

**特徴:**

-   **サーバーサイドの資源に直接アクセス可能**: データベース、ファイルシステム、社内APIなど、サーバー側のリソースに直接アクセスできます。`fetch`を介さずに、直接DBクライアントを叩くようなコードが書けます。
-   **ゼロバンドルサイズ**: コンポーネント自体のコードや、そこで使われているライブラリ（例: DBクライアント、Markdownパーサー）はクライアントに送られないため、JavaScriptバンドルサイズを削減できます。
-   **状態（State）やライフサイクルが使えない**: `useState`や`useEffect`、`onClick`のようなインタラクティブな機能は使えません。これらはクライアントサイドで実行される必要があるためです。
-   **レンダリングはビルド時またはリクエスト時**: サーバー上でレンダリングされ、その結果（HTMLではない、特別なフォーマット）がクライアントに送られます。

```jsx
// app/page.tsx (これはサーバーコンポーネント)
import db from './lib/db'; // サーバーサイドのDBクライアント

// async/await がコンポーネントで直接使える！
async function Page() {
  const posts = await db.post.findMany(); // 直接DBにクエリ

  return (
    <main>
      <h1>Posts</h1>
      <ul>
        {posts.map(post => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </main>
  );
}

export default Page;
```

### Client Components

クライアントコンポーネントは、従来のReactコンポーネントと同じように、クライアントサイドでレンダリングされ、インタラクティブ性を持つコンポーネントです。

**特徴:**

-   **インタラクティブな機能が使える**: `useState`, `useEffect`, `onClick`などのフックやイベントハンドラが使えます。
-   **ブラウザAPIにアクセス可能**: `window`や`localStorage`など、ブラウザ環境に依存するAPIが使えます。
-   **`"use client"` ディレクティブ**: ファイルの先頭に`"use client";`と記述することで、そのファイル内のすべてのコンポーネントがクライアントコンポーネントとして扱われます。

```jsx
// components/Counter.tsx
"use client"; // この宣言が重要

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

## RSCとSSRの違い

この2つは混同されがちですが、根本的に異なります。

-   **SSR (Server-Side Rendering)**: サーバーでReactコンポーネントを実行し、**HTMLを生成**してクライアントに送る技術。クライアントでは、そのHTMLに対してハイドレーションが行われる。
-   **RSC (React Server Components)**: サーバーでServer Componentsを実行し、**UIを記述した特別なデータ形式（RSC Payload）を生成**してクライアントに送る技術。クライアントのReactがこのペイロードを解釈し、DOMを更新する。ハイドレーションは発生しない。

![RSC vs SSR](https://raw.githubusercontent.com/coachtech-material/pro-contents/main/laravel%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E3%83%95%E3%83%AD%E3%83%B3%E3%83%88%E3%82%A8%E3%83%B3%E3%83%89%E5%AD%A6%E7%BF%92%E3%83%AD%E3%83%BC%E3%83%89%E3%83%9E%E3%83%83%E3%83%97/images/column/rsc-vs-ssr.png)

Next.jsのApp Routerでは、RSCとSSRが組み合わさって動作します。まずサーバーでRSCが実行されてUIの骨格が作られ、次にその結果がサーバー上でHTMLにレンダリング（SSR）されて、クライアントに初期表示用のHTMLとして送られます。[2]

## コンポーネントの組み合わせルール

Server ComponentsとClient Componentsには、いくつかの組み合わせルールがあります。

1.  **Server ComponentsはClient Componentsをインポートして利用できる。**
    -   ただし、Server ComponentからClient Componentに渡せるpropsは、シリアライズ可能（文字列、数値、プレーンなオブジェクトなど）でなければならない。関数などを渡すことはできない。
2.  **Client ComponentsはServer Componentsをインポートして利用できない。**
    -   これは、Server Componentがサーバーでしか実行できないコード（例: DBアクセス）を含んでいる可能性があるためです。
    -   しかし、**Server Componentを`children`や`props`としてClient Componentに渡す**ことは可能です。このテクニックを「Server Component Interleaving」と呼び、レイアウトコンポーネントなどで活用されます。

```jsx
// Client Component (e.g., Layout.tsx)
"use client";

export function Layout({ children }) {
  return (
    <div>
      <nav>...</nav>
      <main>{children}</main> {/* ここにServer Componentが入る */}
    </div>
  );
}

// Server Component (e.g., app/page.tsx)
import { Layout } from '../components/Layout';
import { MyServerComponent } from '../components/MyServerComponent';

export default function Page() {
  return (
    <Layout>
      {/* Client Component に Server Component を渡している */}
      <MyServerComponent />
    </Layout>
  );
}
```

## ✨ まとめ

-   RSCは、JSバンドルサイズの削減と、サーバー/クライアント間のシームレスな連携を目的とした新しいアーキテクチャ。
-   コンポーネントは、デフォルトで**Server Components**となり、サーバーでのみ実行される。
-   インタラクティブ性が必要な場合は、`"use client";`を付けて**Client Components**にする。
-   Server ComponentsはDBアクセスなどが直接可能で、Client Componentsは`useState`などが利用可能。
-   RSCはSSRとは異なり、HTMLではなく特別なUI記述形式を生成する。
-   「可能な限りServer Componentsを使い、インタラクティブ性が必要な部分だけをClient Componentsとして切り出す」のが基本戦略となる。

この新しいアーキテクチャを使いこなす鍵は、次に学ぶ`Streaming`と`Suspense`にあります。

---

## 参考文献

[1] React. (2020, December 21). *Introducing Zero-Bundle-Size React Server Components*. Retrieved from https://react.dev/blog/2020/12/21/data-fetching-with-react-server-components

[2] Next.js. (n.d.). *Server Components*. Retrieved from https://nextjs.org/docs/app/building-your-application/rendering/server-components
