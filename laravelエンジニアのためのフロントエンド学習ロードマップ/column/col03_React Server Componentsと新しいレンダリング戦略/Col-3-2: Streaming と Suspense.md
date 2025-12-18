# Col-3-2: Streaming と Suspense

## 🎯 このセクションで学ぶこと

-   従来のレンダリングにおける「ウォーターフォール」問題とその影響を理解する。
-   Streaming と Suspense がどのようにしてこの問題を解決し、UXを向上させるかを学ぶ。
-   Next.js App Router での Streaming の実装方法を理解する。
-   `loading.tsx` ファイルの役割と Suspense の関係を学ぶ。

## 導入: データフェッチのウォーターフォール問題

従来のSSRでは、ページ全体のデータがすべて揃うまで、サーバーはHTMLのレンダリングを開始できませんでした。例えば、ダッシュボードページに「ユーザー情報」「最新ニュース」「友達リスト」の3つのコンポーネントがあり、それぞれが異なるAPIからデータを取得するとします。

この場合、最も遅いAPIリクエストが完了するまで、サーバーは何もクライアントに送信できません。これが「ウォーターフォール」問題です。たった一つの遅いデータソースが、ページ全体の表示をブロックしてしまうのです。これにより、TTFB（Time to First Byte）が悪化し、ユーザーは白い画面を長く見ることになります。[1]

**React Server Components (RSC) と Streaming** は、この問題を解決するための強力な組み合わせです。

## Streaming とは？

Streaming（ストリーミング）とは、サーバーがレンダリングしたUIを、準備ができた部分から順次クライアントに送信する技術です。これにより、ページ全体が完成するのを待つことなく、ユーザーはすぐにUIの一部を見ることができます。

Next.js App Routerでは、RSCと組み合わせることで、サーバーコンポーネントのレンダリング結果をチャンク（断片）に分割し、ストリーミングで配信します。これにより、以下のような体験が実現します。

1.  まず、静的なUI（ヘッダー、フッター、レイアウトなど）を含んだ初期HTMLが即座にクライアントに送信され、描画される。
2.  次に、データ取得を必要としないサーバーコンポーネントのレンダリング結果が送られてきて、対応する部分が描画される。
3.  最後に、時間のかかるデータ取得が完了したサーバーコンポーネントのレンダリング結果が送られてきて、ページの最後のピースが埋まる。

この仕組みにより、TTFBが劇的に改善され、ユーザーの体感速度が向上します。

![Streamingの概念図](https://raw.githubusercontent.com/coachtech-material/pro-contents/main/laravel%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E3%83%95%E3%83%AD%E3%83%B3%E3%83%88%E3%82%A8%E3%83%B3%E3%83%89%E5%AD%A6%E7%BF%92%E3%83%AD%E3%83%BC%E3%83%89%E3%83%9E%E3%83%83%E3%83%97/images/column/streaming-flow.png)

## Suspense: ローディング状態を宣言的に管理する

Streamingを実現するための重要なピースが、Reactに組み込まれた**`<Suspense>`**コンポーネントです。

`<Suspense>`は、子コンポーネントのレンダリング（特にデータ取得などの非同期処理）が完了するまで、代わりに**フォールバックUI（例: ローディングスピナー）**を表示することができます。[2]

```jsx
import { Suspense } from 'react';
import { PostFeed, Weather } from './Components';

export default function Page() {
  return (
    <section>
      <h1>Dashboard</h1>
      <Suspense fallback={<p>Loading feed...</p>}>
        <PostFeed />
      </Suspense>
      <Suspense fallback={<p>Loading weather...</p>}>
        <Weather />
      </Suspense>
    </section>
  );
}
```

上記の例では、`<PostFeed />`と`<Weather />`はそれぞれ非同期でデータを取得するサーバーコンポーネントです。`Suspense`でラップすることにより、Next.jsはこれらのコンポーネントを独立してストリーミングできるようになります。

-   `<PostFeed />`のデータ取得が遅くても、`<Weather />`の準備が先にできれば、そちらが先に表示される。
-   それぞれのコンポーネントがロード中の間は、`fallback`で指定されたUIが表示される。

これにより、開発者は「どの部分が遅延する可能性があるか」を宣言的に指定し、UIの各パーツが独立してロードされることを可能にします。ウォーターフォール問題が解消され、UIの表示がブロックされなくなります。

## Next.js App Routerでの実践: `loading.tsx`

Next.jsのApp Routerでは、この`Suspense`の仕組みをさらに簡単に利用できるように、規約に基づいた特別なファイル**`loading.tsx`**が用意されています。

`app`ディレクトリ内の特定のルートセグメント（例: `app/dashboard/loading.tsx`）に`loading.tsx`というファイルを作成すると、Next.jsは自動的にそのコンポーネントを`Suspense`の`fallback`として設定します。そして、同じ階層にある`page.tsx`とその子コンポーネント全体を`Suspense`の`children`としてラップします。

**例:**

`app/dashboard/layout.tsx`:
```jsx
export default function DashboardLayout({ children }) {
  return (
    <section>
      <h1>Dashboard</h1>
      {children}
    </section>
  );
}
```

`app/dashboard/loading.tsx`:
```jsx
export default function Loading() {
  // ローディングスケルトンやスピナーを返す
  return <p>Loading dashboard data...</p>;
}
```

`app/dashboard/page.tsx`:
```jsx
async function getData() {
  await new Promise(resolve => setTimeout(resolve, 3000)); // 3秒待つ
  return { message: 'Hello, Dashboard!' };
}

export default async function DashboardPage() {
  const data = await getData();
  return <p>{data.message}</p>;
}
```

この場合、ユーザーが`/dashboard`にアクセスすると、

1.  まず`DashboardLayout`が表示される。
2.  `DashboardPage`のデータ取得が完了するまでの3秒間、`loading.tsx`の内容（`Loading dashboard data...`）が表示される。
3.  3秒後、データ取得が完了すると、`loading.tsx`の内容が`DashboardPage`のレンダリング結果に置き換わる。

このように、`loading.tsx`を使うことで、ファイル規約に基づいて簡単にページ単位でのストリーミングとローディングUIを実装できます。

## ✨ まとめ

-   **Streaming**は、UIを準備ができた部分から順次クライアントに送信する技術で、TTFBを改善し、体感速度を向上させる。
-   **Suspense**は、コンポーネントの非同期処理が終わるまでフォールバックUIを表示するためのReactの機能。
-   StreamingとSuspenseを組み合わせることで、データ取得のウォーターフォール問題を解決し、UIの表示がブロックされるのを防ぐ。
-   Next.jsのApp Routerでは、**`loading.tsx`**という規約ファイルを使うことで、ページ単位のストリーミングを簡単に実装できる。
-   これにより、遅いデータソースがあっても、ページの他の部分は素早く表示され、ユーザー体験が大幅に向上する。

次のセクションでは、これらの技術の集大成ともいえる、Next.js 14で導入された新しいレンダリングモデル「Partial Prerendering (PPR)」について学びます。

---

## 参考文献

[1] Next.js. (n.d.). *Streaming*. Retrieved from https://nextjs.org/docs/app/building-your-application/routing/loading-ui-and-streaming#streaming-with-suspense

[2] React. (n.d.). *Suspense*. Retrieved from https://react.dev/reference/react/Suspense
