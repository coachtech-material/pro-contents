# 9-1-4: Server ComponentsとClient Components

## 🎯 このセクションで学ぶこと

- Next.js (App Router) の中核的な概念である、Server ComponentsとClient Componentsの違いを理解する
- Server Componentsの役割と利点（データフェッチ、セキュリティ、パフォーマンス）を学ぶ
- Client Componentsの役割と、インタラクティブなUIを構築するためにいつ必要になるかを学ぶ
- 両者の制約と、どのように連携して動作するのかを理解する
- どちらのコンポーネントを選択すべきかの判断基準を習得する

## 導入

Next.js 13で導入されたApp Routerは、Reactのアーキテクチャに大きなパラダイムシフトをもたらしました。その中心にあるのが、**Server Components**と**Client Components**という2種類のコンポーネントモデルです。

これまでのReact開発（およびNext.jsのPages Router）では、基本的にすべてのコンポーネントはクライアントサイドでレンダリングされ、インタラクティブになるのが当たり前でした。しかしApp Routerでは、**デフォルトですべてのコンポーネントがServer Components**として扱われます。これは、パフォーマンス、データフェッチ、セキュリティを向上させるための重要な変更点です。

このセクションでは、これら2つのコンポーネントモデルが何であり、どのように機能し、どのように使い分けるべきかを詳しく見ていきましょう。

## 詳細解説

### 🔑 Server Components

Server Componentsは、その名の通り、**サーバーサイドでのみレンダリングされる**コンポーネントです。レンダリング結果のHTMLがクライアントに送信され、クライアントサイドのJavaScriptバンドルには一切含まれません。これにより、クライアントに送信するJavaScriptの量を大幅に削減でき、初期表示パフォーマンスが向上します。

**App Routerでは、すべてのコンポーネントがデフォルトでServer Componentsです。**

#### Server Componentsの主な特徴と利点

1.  **データフェッチ**: サーバー上で直接データを取得できます。`async/await`をコンポーネントで直接使えるため、`useEffect`やデータフェッチライブラリなしで、シンプルにデータを取得できます。

    ```tsx
    // app/page.tsx (Server Component)
    async function HomePage() {
      const res = await fetch("https://api.example.com/posts");
      const posts = await res.json();

      return (
        <ul>
          {posts.map(post => <li key={post.id}>{post.title}</li>)}
        </ul>
      );
    }
    ```

2.  **セキュリティ**: APIキーやデータベース接続情報などの機密情報を、クライアントに漏洩することなく安全にサーバーサイドで利用できます。

3.  **パフォーマンス**: クライアントに送信されるJavaScriptがゼロであるため、初期ロードが高速です。また、サーバーに近い場所でデータを取得するため、データフェッチのレイテンシも削減できます。

4.  **バックエンドリソースへの直接アクセス**: データベース、ファイルシステム、外部APIなどに直接アクセスできます。

#### Server Componentsの制約

Server Componentsはサーバーで一度レンダリングされるだけなので、クライアントサイドでのインタラクティブな機能を持つことはできません。

-   **Hooksが使えない**: `useState`, `useEffect`, `useContext` などのクライアントサイドで状態を管理するためのフックは使用できません。
-   **イベントハンドラが使えない**: `onClick`, `onChange` などのブラウザイベントを処理する関数は使用できません。

### 🧩 Client Components

Client Componentsは、従来のReactコンポーネントと同じように、クライアントサイドでレンダリングされ、インタラクティブな機能を持つことができるコンポーネントです。`useState`や`useEffect`といったフックや、イベントハンドラを使いたい場合は、Client Componentsを選択する必要があります。

コンポーネントをClient Componentにするには、ファイルの先頭に **`"use client";`** というディレクティブを記述します。

```tsx
// src/components/Counter.tsx
"use client"; // このディレクティブでClient Componentになる

import { useState } from "react";

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

#### Client Componentsの主な特徴

1.  **インタラクティビティ**: `useState`, `useEffect`などのフックや、`onClick`などのイベントハンドラを使って、ユーザー操作に応じた動的なUIを構築できます。
2.  **ブラウザAPIへのアクセス**: `window`, `localStorage`などのブラウザ固有のAPIにアクセスできます。
3.  **状態管理ライブラリの利用**: `Zustand`, `Redux`などのクライアントサイドの状態管理ライブラリを利用できます。

#### Client Componentsの制約

-   `async/await`を直接コンポーネントで使ってデータをフェッチすることはできません（`useEffect`内やイベントハンドラ内でのフェッチは可能）。
-   サーバーサイドの機密情報やリソースに直接アクセスすることはできません。

### Server ComponentsとClient Componentsの連携

Next.jsの強力な点は、これら2つのコンポーネントをシームレスに組み合わせられることです。

-   Server ComponentsはClient Componentsをインポートして利用できます。
-   **ただし、Client Componentsの中にServer Componentsを`children`や`props`として渡すことはできますが、直接インポートすることはできません。** これは、Client Componentsが一度クライアントサイドのコードになってしまうと、サーバーサイドの機能は呼び出せないためです。

```tsx
// app/page.tsx (Server Component)
import { Counter } from "../components/Counter"; // Client Componentをインポート

async function ServerSideData() {
  const res = await fetch("https://...", { cache: "no-store" });
  const data = await res.json();
  return <p>Server Data: {data.someValue}</p>;
}

export default function Page() {
  return (
    <div>
      <h1>Server and Client Components</h1>
      
      {/* Server ComponentがClient Componentをレンダリング */}
      <Counter />

      {/* Client ComponentにServer Componentをchildrenとして渡す */}
      <SomeClientComponent>
        <ServerSideData />
      </SomeClientComponent>
    </div>
  );
}
```

### どちらを使うべきか？

Next.jsの公式ドキュメントでは、以下の考え方を推奨しています。

> **可能な限りServer Componentsを使い、インタラクティビティが必要な部分だけをClient Componentsにする。**

つまり、まずはすべてをServer Componentsとして構築し始め、`useState`や`onClick`が必要になったコンポーネント（およびその子コンポーネント）を`"use client";`で切り出していく、というアプローチです。インタラクティブな機能をできるだけ末端の小さなコンポーネント（葉っぱのコンポーネント）に押し込めることで、クライアントに送るJavaScriptの量を最小限に抑えることができます。

| 機能 | Server Components | Client Components |
| :--- | :---: | :---: |
| データフェッチ (`async/await`) | ✅ | ❌ |
| バックエンドリソースへの直接アクセス | ✅ | ❌ |
| 機密情報の保持 | ✅ | ❌ |
| `useState`, `useEffect`などのフック | ❌ | ✅ |
| イベントハンドラ (`onClick`など) | ❌ | ✅ |
| ブラウザ専用APIの利用 | ❌ | ✅ |
| **デフォルト** | ✅ | ❌ |

## ✨ まとめ

-   Next.js App Routerでは、コンポーネントは**Server Components**と**Client Components**の2種類に大別される。
-   **デフォルトはServer Components**であり、サーバーでのみレンダリングされ、JavaScriptバンドルに含まれないため高速。
-   Server Componentsは、`async/await`によるデータフェッチや、バックエンドリソースへの安全なアクセスに最適である。
-   インタラクティブな機能（フックやイベントハンドラ）が必要な場合は、ファイルの先頭に`"use client";`を記述して**Client Components**にする。
-   基本戦略は「**できるだけServer Componentsを使い、インタラクティビティが必要な最小限の単位をClient Componentsとして切り出す**」こと。
-   この新しいモデルを理解し、適切に使い分けることが、モダンなNext.jsアプリケーションのパフォーマンスと開発体験を最大化する鍵となる。
