# 9-1-5: Metadata API（SEO対応）

## 🎯 このセクションで学ぶこと

- Next.jsのMetadata APIを使ってSEO対策を行う方法を学ぶ
- 静的メタデータと動的メタデータの使い分けを理解する
- Open Graphタグの設定方法を学ぶ

## はじめに

SEO（検索エンジン最適化）において、適切なメタデータの設定は非常に重要です。Next.jsのApp Routerでは、**Metadata API**を使って、ページごとにタイトルや説明文、OGP画像などを簡単に設定できます。

Laravelの`@section('title')`や`@section('description')`に相当する機能ですが、Next.jsではより型安全で、動的な生成も容易です。

## 1. 静的メタデータ

ページのメタデータが固定の場合は、`metadata`オブジェクトをエクスポートします。

```typescript
// app/about/page.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: '会社概要',
  description: '私たちの会社について紹介します。',
};

export default function AboutPage() {
  return (
    <main>
      <h1>会社概要</h1>
      {/* ... */}
    </main>
  );
}
```

生成されるHTML:

```html
<head>
  <title>会社概要</title>
  <meta name="description" content="私たちの会社について紹介します。" />
</head>
```

## 2. レイアウトでの共通メタデータ

`layout.tsx`でメタデータを設定すると、そのレイアウト配下のすべてのページに適用されます。

```typescript
// app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    default: 'My Website',
    template: '%s | My Website', // 子ページのタイトルに追加される
  },
  description: 'Next.jsで作成したWebサイトです。',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
```

子ページで`title: '会社概要'`を設定すると、実際のタイトルは「会社概要 | My Website」になります。

## 3. 動的メタデータ

ブログ記事や商品ページなど、動的なコンテンツのメタデータを設定するには、`generateMetadata`関数を使います。

```typescript
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next';

interface Props {
  params: Promise<{ slug: string }>;
}

// 動的にメタデータを生成
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  
  // データベースやAPIから記事を取得
  const post = await fetch(`https://api.example.com/posts/${slug}`).then(
    (res) => res.json()
  );

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
    },
  };
}

export default async function BlogPost({ params }: Props) {
  const { slug } = await params;
  const post = await fetch(`https://api.example.com/posts/${slug}`).then(
    (res) => res.json()
  );

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}
```

## 4. Open Graph（OGP）の設定

SNSでシェアされたときの表示を設定するには、`openGraph`プロパティを使います。

```typescript
export const metadata: Metadata = {
  title: '素晴らしい記事',
  description: 'この記事では...',
  openGraph: {
    title: '素晴らしい記事',
    description: 'この記事では...',
    url: 'https://example.com/blog/great-article',
    siteName: 'My Website',
    images: [
      {
        url: 'https://example.com/og-image.png',
        width: 1200,
        height: 630,
        alt: '記事のサムネイル',
      },
    ],
    locale: 'ja_JP',
    type: 'article',
  },
  twitter: {
    card: 'summary_large_image',
    title: '素晴らしい記事',
    description: 'この記事では...',
    images: ['https://example.com/og-image.png'],
  },
};
```

## 5. その他のメタデータ

### robots（クローラー制御）

```typescript
export const metadata: Metadata = {
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
};
```

### icons（ファビコン）

```typescript
export const metadata: Metadata = {
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png',
  },
};
```

### canonical URL

```typescript
export const metadata: Metadata = {
  alternates: {
    canonical: 'https://example.com/blog/great-article',
  },
};
```

## 6. LaravelとNext.jsの比較

| 機能 | Laravel (Blade) | Next.js (Metadata API) |
|------|-----------------|------------------------|
| タイトル設定 | `@section('title', '...')` | `metadata.title` |
| 説明文設定 | `<meta name="description">` | `metadata.description` |
| 動的メタデータ | コントローラーから渡す | `generateMetadata()` |
| OGP設定 | 手動でタグを記述 | `metadata.openGraph` |
| 型安全性 | なし | TypeScriptで型チェック |

## 💡 TIP

- `generateMetadata`は`generateStaticParams`と組み合わせて、ビルド時に静的に生成することもできます。
- メタデータはServer Componentでのみ設定可能です（Client Componentでは使えません）。
- 同じデータを`generateMetadata`とページコンポーネントの両方で取得する場合、Next.jsが自動的にリクエストを重複排除（dedupe）してくれます。

## ✨ まとめ

Next.jsのMetadata APIを使うと、SEOに重要なメタデータを型安全に設定できます。静的なページには`metadata`オブジェクト、動的なページには`generateMetadata`関数を使い分けましょう。Open Graphの設定も簡単に行えるため、SNSでのシェア時の表示も最適化できます。

次のセクションでは、ハンズオンとしてNext.jsプロジェクトを作成し、ここまで学んだ内容を実践します。
