# 9-1-2: なぜNext.jsなのか

## 🎯 この章で学ぶこと

- Next.jsの特徴と利点を理解する
- ReactとNext.jsの違いを理解する
- Next.jsが解決する課題を理解する

## はじめに

Next.jsは、Vercel社が開発したReactベースのフレームワークです。Reactは優れたUIライブラリですが、本番環境で必要な多くの機能（ルーティング、サーバーサイドレンダリング、ビルド最適化など）を自分で設定する必要があります。Next.jsは、これらの機能を標準で提供し、開発者が本質的な機能開発に集中できるようにします。

## Reactだけでは足りない理由

Reactは「UIを構築するためのライブラリ」であり、フレームワークではありません。そのため、本番環境で必要な以下の機能は、追加のライブラリや設定が必要です。

| 機能 | Reactのみ | Next.js |
|------|-----------|---------|
| ルーティング | React Routerなどの追加が必要 | 標準搭載（ファイルベース） |
| サーバーサイドレンダリング | 複雑な設定が必要 | 標準搭載 |
| 静的サイト生成 | 追加ツールが必要 | 標準搭載 |
| コード分割 | 手動設定が必要 | 自動で最適化 |
| 画像最適化 | 追加ライブラリが必要 | 標準搭載（next/image） |
| SEO対策 | 手動で実装 | Metadata APIで簡単に設定 |

## Next.jsの主な特徴

### 1. App Router（ファイルベースルーティング）

Next.jsでは、`app`ディレクトリ内のフォルダ構造がそのままURLのルートになります。

```
app/
├── page.tsx          → /
├── about/
│   └── page.tsx      → /about
└── blog/
    ├── page.tsx      → /blog
    └── [slug]/
        └── page.tsx  → /blog/:slug
```

### 2. Server Components

Next.js 13以降、React Server Components（RSC）がデフォルトで有効になっています。Server Componentsはサーバー上でのみ実行され、JavaScriptバンドルに含まれないため、パフォーマンスが向上します。

```typescript
// Server Component（デフォルト）
async function BlogList() {
  const posts = await fetch('https://api.example.com/posts');
  return <ul>{/* ... */}</ul>;
}
```

### 3. 複数のレンダリング戦略

Next.jsは、ページごとに最適なレンダリング戦略を選択できます。

| 戦略 | 説明 | ユースケース |
|------|------|-------------|
| SSR（Server-Side Rendering） | リクエストごとにサーバーでHTMLを生成 | ユーザー固有のコンテンツ |
| SSG（Static Site Generation） | ビルド時にHTMLを生成 | ブログ、ドキュメント |
| ISR（Incremental Static Regeneration） | 静的生成 + 定期的な再生成 | ECサイトの商品ページ |

### 4. 組み込みの最適化機能

Next.jsには、パフォーマンスを向上させるための機能が組み込まれています。

- **next/image**: 画像の自動最適化（WebP変換、遅延読み込み）
- **next/font**: フォントの最適化（レイアウトシフト防止）
- **next/link**: プリフェッチによる高速なページ遷移

## Laravelエンジニアにとってのメリット

LaravelでWeb開発をしてきたエンジニアにとって、Next.jsは馴染みやすい概念が多くあります。

| Laravel | Next.js |
|---------|---------|
| ルーティング（routes/web.php） | ファイルベースルーティング（app/） |
| Bladeテンプレート | React/JSX |
| ミドルウェア | middleware.ts |
| APIルート | Route Handlers（app/api/） |
| Eloquent ORM | Server Componentsでの直接DB接続 |

## ✨ まとめ

Next.jsは、Reactの機能を拡張し、本番環境で必要な機能を標準で提供するフレームワークです。ファイルベースルーティング、Server Components、複数のレンダリング戦略など、モダンなWebアプリケーション開発に必要な機能が揃っています。

次のセクションでは、Next.jsプロジェクトのセットアップ方法を学んでいきましょう。
