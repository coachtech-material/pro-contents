# Tutorial 9: Next.js

## Chapter 1: Next.jsの基本とルーティング

### Section 5: Metadata API (SEO設定)

🎯 **このセクションで学ぶこと**

-   Next.jsのMetadata APIを使って、ページの`<title>`や`<meta name="description">`を設定する方法を習得する。
-   静的なメタデータと、動的なメタデータの両方を設定できるようになる。
-   `generateMetadata`関数を使って、動的ルート（例: 記事ページ）ごとに異なるタイトルや説明を設定する方法を理解する。
-   OGP（Open Graph Protocol）を設定し、SNSで共有されたときの表示を制御できるようになる。

--- 

### イントロダクション：検索エンジンとSNSに愛されるページ作り

Webページにとって、`<head>`タグ内のメタデータは非常に重要です。ページのタイトル (`<title>`) や説明文 (`<meta name="description">`) は、検索エンジンの検索結果に表示され、クリック率に大きく影響します。また、OGP（Open Graph Protocol）と呼ばれるメタデータは、FacebookやTwitterなどでページが共有された際の、タイトル、説明、画像などを制御します。

LaravelのBladeでは`@section('title', '...')`のように設定していましたが、Next.jsのApp Routerでは、より洗練された**Metadata API**という仕組みが用意されています。

--- 

### 🚀 静的なメタデータの設定

`page.tsx`または`layout.tsx`ファイル内で、`metadata`という名前のオブジェクトを`export`することで、そのページのメタデータを定義できます。これは最も簡単な方法です。

#### 例：Aboutページのメタデータを設定する

`src/app/about/page.tsx`に、`metadata`オブジェクトを追加します。

```tsx
// src/app/about/page.tsx
import type { Metadata } from "next"; // Metadata型をインポート

// metadataオブジェクトをexportする
export const metadata: Metadata = {
  title: "会社概要 | My Awesome App",
  description: "私たちの会社の歴史と理念についてのページです。",
};

export default function AboutPage() {
  return (
    <main>
      <h1>About Us</h1>
      <p>このページは会社概要ページです。</p>
    </main>
  );
}
```

これだけで、`/about`ページを表示すると、ブラウザのタブに「会社概要 | My Awesome App」と表示され、ページのソースを見ると`<title>`と`<meta name="description">`が正しく設定されていることが確認できます。

**メタデータの継承:**
メタデータは、`layout.tsx`から`page.tsx`へと継承され、マージされます。例えば、`layout.tsx`でサイト全体のタイトルテンプレートを定義し、`page.tsx`で個別のタイトルを設定すると、それらが自動的に結合されます。

**例：ルートレイアウトでタイトルテンプレートを設定**

```tsx
// src/app/layout.tsx
export const metadata: Metadata = {
  title: {
    default: "My Awesome App", // デフォルトのタイトル
    template: "%s | My Awesome App", // ページタイトルを差し込むテンプレート
  },
  description: "最高のアプリへようこそ！",
};
```

この設定をしておくと、`/about`ページのタイトルは`metadata.title`で設定した「会社概要」が`%s`の部分に差し込まれ、「**会社概要 | My Awesome App**」と自動的になります。トップページなど、`title`が設定されていないページでは、`default`で指定した「My Awesome App」が表示されます。

--- 

### ⚙️ 動的なメタデータの設定 (`generateMetadata`)

ブログの記事ページのように、URLのパラメータ（記事IDなど）に基づいて動的にメタデータを生成したい場合は、`metadata`オブジェクトの代わりに`generateMetadata`という名前の**非同期関数**を`export`します。

#### 例：記事詳細ページの動的メタデータ

`src/app/posts/[id]/page.tsx`で、記事IDに応じたタイトルを設定してみましょう。

`generateMetadata`関数は、`page.tsx`コンポーネントと同じ`params`を受け取ります。これを使って、APIから記事のタイトルを取得し、メタデータを生成します。

```tsx
// src/app/posts/[id]/page.tsx
import type { Metadata } from "next";

// generateMetadata関数をexportする
export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  // paramsからIDを取得
  const id = params.id;

  // 本来はここでAPIを叩いて記事データを取得する
  // const post = await fetch(`https://api.example.com/posts/${id}`).then(res => res.json());
  const post = { title: `記事タイトル ${id}`, body: `記事${id}の本文です...` }; // ダミーデータ

  return {
    title: post.title,
    description: post.body.substring(0, 100), // 本文の先頭100文字をdescriptionに
  };
}

export default function PostDetailPage({ params }: { params: { id: string } }) {
  // ... ページコンポーネント本体
  return (
    <main>
      <h1>記事詳細ページ (ID: {params.id})</h1>
      {/* ... */}
    </main>
  );
}
```

**Next.jsの賢い挙動:**
注目すべきは、`generateMetadata`内での`fetch`と、ページコンポーネント内での`fetch`は、**自動的に重複が解消される**（deduplicated）という点です。同じURLへの`fetch`リクエストは、ビルドプロセス中に一度しか実行されないため、パフォーマンスの心配は不要です。

--- 

### 🌐 OGPの設定

SNSでの共有時の表示を制御するOGPも、`metadata`オブジェクトの`openGraph`プロパティで簡単に設定できます。

```tsx
// src/app/posts/[id]/page.tsx

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const id = params.id;
  const post = { title: `記事タイトル ${id}`, body: `記事${id}の本文です...` };

  return {
    title: post.title,
    description: post.body.substring(0, 100),
    // openGraphプロパティを追加
    openGraph: {
      title: post.title, // OGP用のタイトル
      description: post.body.substring(0, 100), // OGP用の説明
      url: `https://my-awesome-app.com/posts/${id}`, // 正規のURL
      siteName: "My Awesome App",
      images: [
        {
          url: "https://my-awesome-app.com/og-image.png", // OGP画像のURL
          width: 1200,
          height: 630,
        },
      ],
      locale: "ja_JP",
      type: "website",
    },
    // Twitter用の設定も可能
    twitter: {
      card: "summary_large_image",
      title: post.title,
      description: post.body.substring(0, 100),
      // ...
    },
  };
}
```

--- 

✨ **まとめ**

-   `page.tsx`や`layout.tsx`で`metadata`オブジェクトを`export`することで、静的なメタデータを設定できる。
-   `layout.tsx`で`title.template`を設定すると、サイト全体のタイトル形式を統一できる。
-   URLのパラメータに応じて動的にメタデータを生成するには、`generateMetadata`非同期関数を`export`する。
-   `generateMetadata`は`params`を受け取るため、APIから取得したデータに基づいて`<title>`などを設定できる。
-   OGPやTwitter Cardの設定も、`metadata`オブジェクト内の`openGraph`や`twitter`プロパティで行う。

📝 **学習のポイント**

-   [ ] `robots.txt`や`sitemap.xml`といった、SEOに重要な他のファイルは、Next.jsではどのように生成・配置するのがベストプラクティスか調べてみましょう。
-   [ ] `metadata`オブジェクトで設定できる項目は、`title`や`description`以外にどのようなものがあるか、Next.jsの公式ドキュメントで確認してみましょう。
-   [ ] Next.js 13.2から導入された「File-based Metadata」という機能を使うと、`favicon.ico`や`og-image.png`といったメタデータ関連のファイルを`app`ディレクトリに配置するだけで自動的に設定されます。その具体的な使い方を調べてみましょう。
