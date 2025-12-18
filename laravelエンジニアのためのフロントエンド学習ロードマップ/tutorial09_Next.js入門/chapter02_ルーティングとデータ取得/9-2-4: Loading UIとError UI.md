# 9-2-4: Loading UIとError UI

## 🎯 このセクションで学ぶこと

-   Next.js App Routerが提供する、規約に基づいたローディングUIとエラーUIの仕組みを理解する
-   `loading.tsx`ファイルを作成し、データ取得中に自動的に表示されるローディングUIを実装する方法を学ぶ
-   React Suspenseが裏側でどのように機能しているかを理解する
-   `error.tsx`ファイルを作成し、ルートセグメントで発生したエラーをハンドリングし、フォールバックUIを表示する方法を学ぶ
-   React Error Boundaryが裏側でどのように機能しているかを理解する

## 導入

前のセクションでは、Server Componentsでデータを取得する方法を学びました。データ取得には時間がかかるため、その間ユーザーに「読み込み中である」ことを示すフィードバックを提供することは、優れたUX（ユーザー体験）のために不可欠です。

同様に、データ取得の失敗やレンダリング中の予期せぬエラーが発生した場合に、アプリケーション全体がクラッシュするのではなく、適切なエラーメッセージを表示し、ユーザーが次のアクション（例: 再読み込み）を取れるようにすることも非常に重要です。

Next.js App Routerは、これらの一般的な要件に対して、**規約に基づいたファイル**（`loading.tsx`と`error.tsx`）を作成するだけで、Reactの高度な機能である**Suspense**と**Error Boundary**を簡単に利用できる仕組みを提供しています。

## 詳細解説

### ⏳ `loading.tsx` によるローディングUI

`loading.tsx`は、同じ階層にある`page.tsx`とその子コンポーネントがデータを取得している間、自動的に表示されるUIを定義するための規約ファイルです。

#### 使い方

データ取得を行う`page.tsx`と同じディレクトリに、`loading.tsx`という名前のファイルを作成するだけです。

```
app/
└── dashboard/
    ├── page.tsx      # データ取得を行うページ
    └── loading.tsx   # page.tsxのデータ取得中に表示されるUI
```

```tsx
// app/dashboard/loading.tsx

export default function Loading() {
  // スケルトンスクリーンやスピナーなど、任意のローディングUIを返す
  return <div>Loading dashboard data...</div>;
}
```

```tsx
// app/dashboard/page.tsx

async function DashboardPage() {
  // このデータ取得が完了するまで、Next.jsは
  // loading.tsx の内容を代わりに表示する
  await new Promise(resolve => setTimeout(resolve, 2000)); // 2秒待機をシミュレート
  const response = await fetch("https://api.example.com/dashboard");
  const data = await response.json();

  return <h1>Dashboard Data: {data.value}</h1>;
}

export default DashboardPage;
```

これだけで、`/dashboard`にアクセスすると、まず`loading.tsx`の内容が即座に表示され、`page.tsx`のデータ取得が完了した時点で、ページの内容が`page.tsx`のレンダリング結果に自動的に切り替わります。

#### 裏側の仕組み: React Suspense

この機能は、Reactの**Suspense**という機能に基づいています。Next.jsは、`loading.tsx`ファイルを見つけると、自動的に`page.tsx`を`<Suspense>`コンポーネントでラップし、`fallback` propに`loading.tsx`の内容を渡してくれます。

```tsx
// Next.jsが内部的に生成するコードのイメージ
<Suspense fallback={<Loading />}>
  <DashboardPage />
</Suspense>
```

`loading.tsx`は、この複雑な設定をファイル規約という形で抽象化し、開発者がSuspenseを意識することなく、簡単にローディングUIを実装できるようにしてくれているのです。

### 💣 `error.tsx` によるエラーUI

`error.tsx`は、ルートセグメント（同じ階層の`page.tsx`やその子コンポーネント）で予期せぬエラーが発生した際に、自動的に表示されるフォールバックUIを定義するための規約ファイルです。

#### 使い方

`loading.tsx`と同様に、エラーをキャッチしたいルートセグメントに`error.tsx`という名前のファイルを作成します。

```
app/
└── dashboard/
    ├── page.tsx
    ├── loading.tsx
    └── error.tsx     # page.tsxでエラーが発生した場合に表示されるUI
```

`error.tsx`コンポーネントは、**Client Componentである必要があります** (`"use client";`が必須)。これは、エラーが発生した後にユーザーが「再試行」するなどのインタラクションを可能にするためです。

```tsx
// app/dashboard/error.tsx
"use client"; // Error BoundaryはClient Componentである必要がある

import { useEffect } from "react";

interface ErrorProps {
  error: Error; // 発生したエラーオブジェクト
  reset: () => void; // セグメントを再レンダリングして再試行する関数
}

export default function Error({ error, reset }: ErrorProps) {
  useEffect(() => {
    // エラーをロギングサービスに送信するなどの処理
    console.error(error);
  }, [error]);

  return (
    <div>
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

`page.tsx`内でエラーがスローされると（例: `fetch`の失敗）、Next.jsは最も近い親階層にある`error.tsx`を探し、その内容でUIを置き換えます。`reset`関数を呼び出すことで、ユーザーはページを再読み込みすることなく、コンポーネントの再レンダリングを試みることができます。

#### 裏側の仕組み: React Error Boundary

この機能は、Reactの**Error Boundary**という機能に基づいています。Next.jsは、`error.tsx`ファイルを見つけると、自動的にルートセグメントをError Boundaryコンポーネントでラップします。

`error.tsx`は、アプリケーション全体がクラッシュするのを防ぎ、エラーが発生した部分だけをフォールバックUIに置き換えることで、アプリケーションの堅牢性を高めます。重要な点として、`error.tsx`は同じ階層の`layout.tsx`で発生したエラーはキャッチしません。これは、エラーUI自体を表示するための共通レイアウト（ナビゲーションなど）が、エラーによって壊れるのを防ぐためです。

## ✨ まとめ

-   Next.js App Routerでは、ファイル規約に従うだけで、高度なローディングUIとエラーハンドリングを簡単に実装できる。
-   `loading.tsx`を作成すると、同じ階層のページコンポーネントのデータ取得中に、その内容が**React Suspense**のフォールバックとして自動的に表示される。
-   `error.tsx`を作成すると、ページコンポーネントでエラーが発生した際に、その内容が**React Error Boundary**のフォールバックとして自動的に表示される。
-   `error.tsx`は`"use client";`ディレクティブが必須であり、エラー内容の表示や再試行のための`reset`関数といったインタラクティブな機能を提供できる。
-   これらの規約を活用することで、UXとアプリケーションの堅牢性を手軽に向上させることができる。
