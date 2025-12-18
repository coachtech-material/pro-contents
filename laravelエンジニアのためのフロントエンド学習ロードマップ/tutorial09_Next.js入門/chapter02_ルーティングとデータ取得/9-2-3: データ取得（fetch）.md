# 9-2-3: データ取得（fetch）

## 🎯 このセクションで学ぶこと

-   Server Componentsで`async/await`を使ってデータを直接取得する方法を学ぶ
-   Next.jsが拡張した`fetch` APIの強力なキャッシュ機能を理解する
-   データのキャッシュ戦略（静的、動的）を制御する方法を習得する
-   キャッシュされたデータを更新するための再検証（Revalidation）の仕組みを学ぶ

## 導入

Next.js App Routerの最も革新的な機能の一つが、データ取得の方法です。Server Componentsの導入により、Reactコンポーネント内で直接`async/await`を使ってデータを取得できるようになりました。これにより、`useEffect`や`useState`、あるいは`TanStack Query`のようなクライアントサイドのデータフェッチライブラリを使わずに、シンプルかつ直感的にデータを扱うことができます。

さらに、Next.jsはWeb標準の`fetch` APIを独自に拡張し、リクエストごとに詳細なキャッシュ戦略を定義できるようにしています。これにより、パフォーマンスとデータの鮮度を柔軟にコントロールすることが可能になります。

## 詳細解説

### 🔑 Server Componentsでのデータ取得

Server Componentsはサーバーサイドで実行されるため、コンポーネント自体を`async`関数として定義できます。これにより、コンポーネントのレンダリングプロセスの一部として、ごく自然にデータ取得を組み込めます。

```tsx
// app/posts/page.tsx

interface Post {
  id: number;
  title: string;
}

// ページコンポーネントをasync関数として定義
async function PostsPage() {
  // データを直接fetch
  const res = await fetch('https://jsonplaceholder.typicode.com/posts', {
    // Next.jsのキャッシュオプション (後述)
    cache: 'force-cache', 
  });

  if (!res.ok) {
    throw new Error('Failed to fetch data');
  }

  const posts: Post[] = await res.json();

  return (
    <main>
      <h1>Posts</h1>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </main>
  );
}

export default PostsPage;
```

このコードは、`useEffect`を使った従来のデータ取得方法に比べて、はるかにシンプルで宣言的です。ローディング状態を別途管理する必要もありません。Next.jsがデータの取得が完了するまでページのレンダリングを待機してくれるからです。（ローディングUIについては次のセクションで学びます）

### 📚 キャッシュ戦略

Next.jsは、`fetch` APIの`options`オブジェクトを拡張し、サーバーサイドでのキャッシュ動作を制御できるようにしています。`cache`オプションと`next.revalidate`オプションがその中心です。

#### デフォルトの動作: 静的データフェッチ (`cache: 'force-cache'`)

`fetch`を呼び出す際にキャッシュオプションを指定しない場合、デフォルトで`cache: 'force-cache'`が適用されます。これは、**ビルド時に一度だけデータを取得し、その結果を永続的にキャッシュする**という動作を意味します。同じリクエストが再度発生しても、ネットワークリクエストは走らず、キャッシュされたデータが即座に返されます。

これは、ブログ記事や製品情報など、頻繁に更新されないコンテンツに最適で、ページのパフォーマンスを最大化します（実質的なSSG: Static Site Generation）。

#### キャッシュの無効化: 動的データフェッチ (`cache: 'no-store'`)

常に最新のデータを表示したい場合、例えばユーザーごとのダッシュボードや株価情報のようなページでは、キャッシュを無効化する必要があります。そのためには`cache: 'no-store'`オプションを指定します。

```tsx
async function DashboardPage() {
  const res = await fetch('https://api.example.com/user/dashboard', {
    cache: 'no-store', // リクエストごとに常に最新のデータを取得
  });
  // ...
}
```

このオプションを指定すると、ページへのリクエストがあるたびに、サーバーサイドでデータが再取得されます。これは、SSR (Server-Side Rendering) と同じ動作になります。

### ♻️ データの再検証 (Revalidation)

「ビルド時に静的に生成しつつも、定期的にデータを更新したい」というニーズも多くあります。例えば、ニュースサイトの記事一覧などです。このようなケースのために、Next.jsは**再検証 (Revalidation)** の仕組みを提供しています。

#### 時間ベースの再検証 (Time-based Revalidation)

`fetch`の`next.revalidate`オプションに秒数を指定することで、指定した時間が経過した後に最初のリクエストがあったタイミングで、バックグラウンドでデータが再取得されます。その間、ユーザーには古い（キャッシュされた）データが表示され、再取得が完了するとキャッシュが更新されます。

これは**ISR (Incremental Static Regeneration)**として知られる強力な機能です。

```tsx
async function NewsPage() {
  const res = await fetch('https://api.example.com/news', {
    next: { 
      revalidate: 60, // 60秒ごとにデータを再検証
    }, 
  });
  // ...
}
```

この設定により、ビルド時にページが生成された後も、最大60秒の鮮度を保ちつつ、静的ページのように高速な表示を実現できます。

#### オンデマンド再検証 (On-demand Revalidation)

時間ベースではなく、特定のイベント（例: CMSで記事を更新した、データベースの内容を変更した）をトリガーにキャッシュを能動的にクリアしたい場合もあります。これを**オンデマンド再検証**と呼びます。

これは、`revalidatePath`や`revalidateTag`といった関数をAPIルートやサーバーアクション内で呼び出すことで実現します。これにより、ヘッドレスCMSのWebhookなどと連携して、コンテンツの更新を即座に本番環境に反映させることが可能になります。（詳細は発展的な内容のため、ここでは紹介に留めます）

### キャッシュ戦略の選択

| キャッシュオプション | 説明 | ユースケース | レンダリング方式 |
| :--- | :--- | :--- | :--- |
| `cache: 'force-cache'` (デフォルト) | ビルド時にデータを取得し、永続的にキャッシュする。 | ブログ記事、製品ページ、ドキュメント | SSG |
| `next: { revalidate: number }` | 指定した秒数ごとにデータを再検証する。 | ニュース記事、イベント一覧 | ISR |
| `cache: 'no-store'` | リクエストごとに常にデータを再取得する。 | ユーザーダッシュボード、ショッピングカート | SSR |

## ✨ まとめ

-   Server Componentsでは、コンポーネントを`async`関数にすることで、`useEffect`なしで直接データを取得できる。
-   Next.jsは`fetch` APIを拡張し、`cache`オプションと`next.revalidate`オプションでキャッシュ戦略を細かく制御できる。
-   デフォルト (`force-cache`) ではデータは永続的にキャッシュされ、パフォーマンスが最大化される (SSG)。
-   `cache: 'no-store'`を指定すると、リクエストごとにデータが再取得される (SSR)。
-   `next: { revalidate: 60 }`のように指定すると、時間ベースの再検証 (ISR) が可能になり、静的サイトのパフォーマンスと動的コンテンツの鮮度を両立できる。
-   これらの機能を理解し使い分けることが、Next.jsアプリケーションのパフォーマンスを最適化する上で非常に重要である。
