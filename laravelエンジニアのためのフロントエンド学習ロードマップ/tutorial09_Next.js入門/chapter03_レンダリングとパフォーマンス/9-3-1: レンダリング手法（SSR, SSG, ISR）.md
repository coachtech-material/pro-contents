# 9-3-1: レンダリング手法（SSR, SSG, ISR）

## 🎯 このセクションで学ぶこと

-   モダンなWebアプリケーションにおける主要なレンダリング手法、SSR, SSG, ISRの概念を理解する
-   Next.js App Routerにおいて、これらのレンダリング手法がデータ取得時のキャッシュ戦略とどのように結びついているかを学ぶ
-   各レンダリング手法のメリット・デメリットを比較し、どのようなコンテンツにどの手法が適しているかを判断できるようになる

## 導入

Next.jsは、単なるReactフレームワークではなく、**ハイブリッドフレームワーク**としての側面を強く持っています。これは、ページやコンポーネントごとに最適なレンダリング手法を選択し、組み合わせることができるという意味です。

以前のチャプターで、データ取得時のキャッシュ戦略（`force-cache`, `no-store`, `revalidate`）について学びました。実は、これらのキャッシュ戦略が、Next.jsにおけるレンダリング手法そのものを決定しています。App Routerでは、レンダリングとデータ取得が密接に統合されているのです。

このセクションでは、伝統的なレンダリング手法である**SSR (Server-Side Rendering)**, **SSG (Static Site Generation)**、そしてNext.jsが普及させた**ISR (Incremental Static Regeneration)**が、App Routerのデータフェッチとどのように対応しているのかを整理し、理解を深めます。

## 詳細解説

Next.js App Routerでは、ルート（ページ）のレンダリング方法は、そのルート内で使用される`fetch`リクエストのキャッシュオプションによって決まります。動的な関数（`cookies()`, `headers()`など）や動的な`fetch`（`cache: 'no-store'`）を使用しない限り、ルートはデフォルトで静的にレンダリングされます。

### 靜的サイト生成 (SSG - Static Site Generation)

SSGは、**ビルド時に**すべてのページをHTMLファイルとして事前に生成しておく手法です。生成されたHTMLはCDNにキャッシュされ、ユーザーからのリクエストに対して即座に配信されるため、非常に高速です。

**App Routerでの実現方法:**

-   `fetch`リクエストでキャッシュオプションを指定しない（デフォルトの`cache: 'force-cache'`が適用される）。
-   または、明示的に`cache: 'force-cache'`を指定する。

```tsx
// このページはビルド時に静的生成される (SSG)
async function AboutPage() {
  // デフォルトで 'force-cache' が適用される
  const res = await fetch("https://api.example.com/team-members");
  const members = await res.json();

  return <div>{/* ... */}</div>;
}
```

-   **メリット**: 非常に高速（CDNから配信）、サーバー負荷が低い、セキュリティが高い。
-   **デメリット**: ビルド後にコンテンツが更新されても、再ビルドするまで内容は変わらない。
-   **適したコンテンツ**: ブログ記事、ドキュメント、マーケティングページ、製品紹介ページなど、更新頻度が低いコンテンツ。

### サーバーサイドレンダリング (SSR - Server-Side Rendering)

SSRは、**ユーザーからのリクエストごとに**、サーバーサイドでHTMLを生成する手法です。常に最新のデータを含んだページを生成できるため、動的なコンテンツに適しています。

**App Routerでの実現方法:**

-   `fetch`リクエストで`cache: 'no-store'`を指定する。
-   `cookies()`や`headers()`のような動的な関数をページ内で使用する。（これらを使用すると、Next.jsはそのページがリクエストごとに動的にレンダリングされる必要があると判断します）

```tsx
import { cookies } from "next/headers";

// このページはリクエストごとにサーバーサイドレンダリングされる (SSR)
async function DashboardPage() {
  const cookieStore = cookies();
  const token = cookieStore.get("token");

  // 'no-store' を指定するか、動的な関数(cookies)を使う
  const res = await fetch("https://api.example.com/user/dashboard", {
    headers: { Authorization: `Bearer ${token.value}` },
    cache: "no-store",
  });
  const data = await res.json();

  return <div>{/* ... */}</div>;
}
```

-   **メリット**: 常に最新のデータを表示できる、ユーザーごとにパーソナライズされたコンテンツを提供できる。
-   **デメリット**: リクエストごとにサーバーでの計算が必要なため、SSGより表示が遅くなる可能性がある、サーバー負荷が高い。
-   **適したコンテンツ**: ユーザーダッシュボード、SNSのフィード、検索結果ページなど、動的でパーソナライズが必要なコンテンツ。

### インクリメンタル静的再生成 (ISR - Incremental Static Regeneration)

ISRは、SSGとSSRの「いいとこ取り」をしたような手法です。基本的にはビルド時に静的ページを生成しますが、**指定した時間が経過した後にアクセスがあった場合、バックグラウンドでページを再生成**します。

**App Routerでの実現方法:**

-   `fetch`リクエストで`next: { revalidate: <秒数> }`オプションを指定する。

```tsx
// このページはISRでレンダリングされる
async function NewsPage() {
  const res = await fetch("https://api.example.com/news", {
    next: { revalidate: 60 }, // 60秒ごとに再検証
  });
  const news = await res.json();

  return <div>{/* ... */}</div>;
}
```

-   **メリット**: SSGの高速表示を維持しつつ、定期的にコンテンツを自動更新できる。サーバー負荷を抑えつつ、ある程度の鮮度を保てる。
-   **デメリット**: データがリアルタイムに更新されるわけではない（最大で指定した秒数分の遅延がある）。
-   **適したコンテンツ**: ニュースサイト、ECサイトの商品一覧、イベント情報ページなど、 شبهリアルタイムな更新が求められるコンテンツ。

### まとめ表

| 手法 | レンダリングタイミング | App Routerでの実現方法 | メリット | デメリット | ユースケース |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SSG** | ビルド時 | `fetch` (デフォルト) | 非常に高速、低負荷 | ビルドまで更新不可 | ブログ、ドキュメント |
| **SSR** | リクエストごと | `fetch` with `cache: 'no-store'` | 常に最新、パーソナライズ | 比較的低速、高負荷 | ダッシュボード、SNS |
| **ISR** | ビルド時 + 定期的に再生成 | `fetch` with `next: { revalidate: n }` | 高速性と鮮度の両立 | リアルタイムではない | ニュース、ECサイト |

## ✨ まとめ

-   Next.js App Routerでは、ページのレンダリング手法はデータ取得時の**キャッシュ戦略**によって決定される。
-   **SSG**は、デフォルトの`fetch`キャッシュ（`force-cache`）によって実現され、最高のパフォーマンスを提供する。
-   **SSR**は、`fetch`で`cache: 'no-store'`を指定するか、`cookies()`のような動的関数を使うことで実現され、常に最新のデータを表示する。
-   **ISR**は、`fetch`で`next: { revalidate: n }`を指定することで実現され、静的なパフォーマンスとデータの鮮度を両立させる。
-   コンテンツの特性（更新頻度、パーソナライズの要否）に応じてこれらのレンダリング手法を適切に選択し、ページ単位で組み合わせることが、Next.jsアプリケーションのパフォーマンスを最大化する鍵となる。
