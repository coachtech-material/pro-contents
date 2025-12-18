# 9-3-5: 実践 🚀 Chapter 3 ハンズオン: ブログのパフォーマンスを改善する（Hydration Errorの体験を含む）

## 🎯 このハンズオンの目的

このチャプターで学んだパフォーマンス最適化のテクニックと、Hydration Mismatchエラーの対処法を実践的に習得します。Chapter 2で作成したブログアプリケーションをベースに、以下の改善を加えます。

-   **Hydration Mismatchの体験と修正**: 意図的にエラーを発生させ、`useEffect`を使って正しく修正する。
-   **画像最適化**: `next/image`を使って、記事にアイキャッチ画像を追加し、最適化する。
-   **フォント最適化**: `next/font`を使って、アプリケーション全体のフォントを最適化する。
-   **動的インポート**: コメント欄など、初期表示に不要なコンポーネントを`next/dynamic`で遅延読み込みする。

このハンズオンを通して、Next.jsが提供する強力な最適化機能を実際に適用し、その効果を体感します。

## 事前準備

-   Chapter 2のハンズオンで作成したブログアプリケーションのコード。
-   画像は、[Unsplash](https://unsplash.com/) などのフリー素材サイトから好きなものを選んで使うか、ダミー画像生成サービス（例: `https://picsum.photos/800/400`）を利用します。

## ハンズオン

### ステップ1: Hydration Mismatchを体験し、修正する

まず、記事詳細ページに「この記事はXX秒前に表示されました」というような、クライアントサイドでのみ正確に計算できる情報を表示してみましょう。これにより、Hydration Mismatchがどのように発生し、どう修正するのかを学びます。

1.  `app/blog/[id]/page.tsx`を開き、コンポーネントの先頭で現在時刻を取得するコードを追加します。

    ```tsx
    // app/blog/[id]/page.tsx

    // ... (imports)

    // ... (getPost function)

    export default async function PostDetailPage({ params }: { params: { id: string } }) {
      const post: Post = await getPost(params.id);
      const renderedAt = new Date().toLocaleTimeString(); // サーバーとクライアントで値が異なる

      return (
        <div>
          <h1>{post.title}</h1>
          <p>{post.body}</p>
          <p style={{ color: "gray" }}>Rendered at: {renderedAt}</p> {/* ミスマッチの原因 */}
        </div>
      );
    }
    ```

2.  開発サーバーを起動し、いずれかの記事ページにアクセスします。ブラウザのコンソールにHydration Mismatchエラーが表示されることを確認してください。

3.  このエラーを修正します。`useEffect`を使って、クライアントサイドでのみ時刻をレンダリングするように変更します。このコンポーネントは`async`なので、時刻表示部分を別のClient Componentに切り出す必要があります。

    a. `app/blog/[id]/`に`RenderedTime.tsx`というファイルを作成します。

    ```tsx
    // app/blog/[id]/RenderedTime.tsx
    "use client";

    import { useState, useEffect } from "react";

    export default function RenderedTime() {
      const [time, setTime] = useState("");

      useEffect(() => {
        // マウント後にクライアントサイドでのみ実行
        setTime(new Date().toLocaleTimeString());
      }, []);

      if (!time) {
        return <p style={{ color: "gray" }}>Rendered at: calculating...</p>;
      }

      return <p style={{ color: "gray" }}>Rendered at: {time}</p>;
    }
    ```

    b. `app/blog/[id]/page.tsx`を修正し、新しいコンポーネントをインポートして使います。

    ```tsx
    // app/blog/[id]/page.tsx
    import RenderedTime from "./RenderedTime";

    // ... (getPost function)

    export default async function PostDetailPage({ params }: { params: { id: string } }) {
      const post: Post = await getPost(params.id);

      return (
        <div>
          <h1>{post.title}</h1>
          <p>{post.body}</p>
          <RenderedTime /> {/* Client Componentを呼び出す */}
        </div>
      );
    }
    ```

4.  再度ページにアクセスし、コンソールからエラーが消え、時刻が正しく表示されることを確認します。

### ステップ2: `next/image`でアイキャッチ画像を追加する

記事詳細ページにアイキャッチ画像を追加します。

1.  `app/blog/[id]/page.tsx`を修正し、`<Image>`コンポーネントを追加します。画像のURLは、ダミー画像サービスを使い、記事IDに基づいて異なる画像が表示されるようにしてみましょう。

    ```tsx
    // app/blog/[id]/page.tsx
    import Image from "next/image";
    import RenderedTime from "./RenderedTime";

    // ... (interface Post, getPost function)

    export default async function PostDetailPage({ params }: { params: { id: string } }) {
      const post: Post = await getPost(params.id);

      return (
        <div>
          <h1>{post.title}</h1>
          <div style={{ margin: "20px 0" }}>
            <Image
              src={`https://picsum.photos/seed/${post.id}/800/400`}
              alt={post.title}
              width={800}
              height={400}
              priority // LCPになる可能性が高い画像にはpriority属性をつける
            />
          </div>
          <p>{post.body}</p>
          <RenderedTime />
        </div>
      );
    }
    ```

2.  `next.config.mjs`ファイルに、外部ドメインの画像を利用するための設定を追加します。

    ```js
    // next.config.mjs
    /** @type {import("next").NextConfig} */
    const nextConfig = {
      images: {
        remotePatterns: [
          {
            protocol: "https",
            hostname: "picsum.photos",
          },
        ],
      },
    };

    export default nextConfig;
    ```

3.  開発サーバーを再起動し、記事ページに画像が最適化されて表示されることを確認します。ブラウザの開発者ツールでネットワークタブを開き、画像がWebP形式で配信されていることや、サイズが適切になっていることを確認してみましょう。

### ステップ3: `next/font`でフォントを最適化する

アプリケーション全体のフォントを`next/font`を使って最適化します。

1.  `app/layout.tsx`を開き、Google Fontsから好きなフォント（例: `Noto Sans JP`）をインポートして適用します。

    ```tsx
    // app/layout.tsx
    import { Noto_Sans_JP } from "next/font/google";
    import "./globals.css";

    const notoSansJP = Noto_Sans_JP({
      subsets: ["latin"],
      weight: ["400", "700"],
      display: "swap",
    });

    export const metadata = {
      title: "My Blog",
      description: "A blog created with Next.js",
    };

    export default function RootLayout({ children }: { children: React.ReactNode }) {
      return (
        <html lang="ja" className={notoSansJP.className}>
          <body>{children}</body>
        </html>
      );
    }
    ```

2.  ページにアクセスし、フォントが適用されていることを確認します。開発者ツールで`<html>`要素を見ると、`next/font`によって生成されたクラス名とスタイルが適用されていることがわかります。

### ステップ4: `next/dynamic`でコメント欄を遅延読み込みする

記事詳細ページに、初期表示には不要な「コメント欄」コンポーネントを追加し、動的に読み込むようにします。

1.  `app/blog/[id]/`に`Comments.tsx`というファイルを作成します。これは重いコンポーネントであると仮定し、`setTimeout`で読み込みをシミュレートします。

    ```tsx
    // app/blog/[id]/Comments.tsx
    export default async function Comments() {
      // 重い処理をシミュレート
      await new Promise((resolve) => setTimeout(resolve, 2000));

      return <div>This is a heavy comments section.</div>;
    }
    ```

2.  `app/blog/[id]/page.tsx`を修正し、`next/dynamic`を使って`Comments`コンポーネントを遅延読み込みします。

    ```tsx
    // app/blog/[id]/page.tsx
    import Image from "next/image";
    import dynamic from "next/dynamic";
    import RenderedTime from "./RenderedTime";

    // Commentsコンポーネントを動的にインポート
    const Comments = dynamic(() => import("./Comments"), {
      loading: () => <p>Loading comments...</p>,
    });

    // ... (interface Post, getPost function)

    export default async function PostDetailPage({ params }: { params: { id: string } }) {
      const post: Post = await getPost(params.id);

      return (
        <div>
          {/* ... (title, image, body) */}
          <RenderedTime />
          <hr style={{ margin: "20px 0" }} />
          <Comments />
        </div>
      );
    }
    ```

3.  記事ページにアクセスします。ページの主要なコンテンツ（タイトル、画像、本文）がまず表示され、その後に「Loading comments...」と表示され、2秒後に「This is a heavy comments section.」に切り替わることを確認します。これにより、重いコンポーネントが初期表示をブロックしていないことがわかります。

## ✨ まとめ

このハンズオンを通じて、Next.jsのパフォーマンス最適化機能を一通り実践しました。

-   Hydration Mismatchエラーを意図的に発生させ、Client Componentに処理を分離することで正しく修正しました。
-   `next/image`を導入し、外部画像を最適化された形で配信しました。
-   `next/font`を使い、数行のコードでWebフォントを最適化し、レイアウトシフトを防ぎました。
-   `next/dynamic`を利用して、重いコンポーネントを遅延読み込みし、初期表示のパフォーマンスを改善しました。

これらのテクニックは、実際のプロジェクトでアプリケーションの品質を向上させるために頻繁に利用されます。それぞれの機能がどのような問題を解決し、どのように使うのかを実践的に理解できたはずです。
