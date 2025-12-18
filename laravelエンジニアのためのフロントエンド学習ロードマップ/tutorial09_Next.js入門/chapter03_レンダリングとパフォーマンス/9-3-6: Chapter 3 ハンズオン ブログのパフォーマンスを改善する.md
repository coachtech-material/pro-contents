
# 9-3-6: Chapter 3 ハンズオン: ブログのパフォーマンスを改善する

## 🎯 このハンズオンの目的

この章で学んだレンダリング、キャッシュ、パフォーマンス最適化の知識を総動員して、Chapter 2で作成したブログアプリケーションのパフォーマンスを実際に改善します。また、意図的にHydration Mismatchエラーを発生させ、その解決プロセスを体験します。

## 準備

Chapter 2のハンズオンで作成したブログプロジェクトのコードを準備してください。

```bash
# Chapter 2のプロジェクトディレクトリに移動
cd my-next-blog

# 開発サーバーを起動
npm run dev
```

## Step 1: 現状のパフォーマンスを測定する

最適化の前に、まずは現状のパフォーマンスを把握しましょう。ChromeのLighthouseを使って測定します。

1.  `npm run build` と `npm start` を実行して、本番モードでアプリケーションを起動します。
2.  Chromeで `http://localhost:3000` にアクセスします。
3.  開発者ツールを開き（`Ctrl+Shift+I` または `Cmd+Option+I`）、「Lighthouse」タブを選択します。
4.  「Analyze page load」ボタンをクリックして、レポートが生成されるのを待ちます。

特に「Performance」のスコアと、LCP、CLSといったCore Web Vitalsの数値を確認しておきましょう。記事詳細ページ（例: `/posts/1`）についても同様に測定しておくと、改善の度合いが分かりやすくなります。

## Step 2: 画像の最適化 (`next/image`)

記事詳細ページでは、現在通常の`<img>`タグで画像を表示しています。これを`next/image`に置き換えて、画像の最適化を行います。

`app/posts/[id]/page.tsx` を開き、`<img>`タグを以下のように修正します。

```tsx
// app/posts/[id]/page.tsx

import Image from 'next/image'; // Imageをインポート

// ... (既存のコード)

export default async function PostDetailPage({ params }: { params: { id: string } }) {
  const post = await getPost(params.id);

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-4xl font-bold mb-4">{post.title}</h1>
      
      {/* ↓ ここから修正 ↓ */}
      <div className="relative w-full h-96 mb-4">
        <Image 
          src={`https://picsum.photos/seed/${post.id}/1200/800`}
          alt={post.title}
          fill
          style={{ objectFit: 'cover' }}
          priority // LCPになる可能性が高いのでpriority属性を追加
        />
      </div>
      {/* ↑ ここまで修正 ↑ */}

      <p className="text-gray-700 leading-relaxed">{post.body}</p>
    </div>
  );
}
```

**変更点:**

-   `next/image`から`Image`コンポーネントをインポートします。
-   `<img>`を`<Image>`に置き換えます。
-   レスポンシブな画像サイズに対応するため、`fill`プロパティを使い、親要素に`relative`とサイズを指定します。
-   `style={{ objectFit: 'cover' }}` で画像の表示方法を調整します。
-   ページの主要コンテンツであるため、`priority`属性を追加して、この画像を優先的に読み込むように指定します。

## Step 3: キャッシュ戦略の導入 (ISR)

現在、私たちのブログはリクエストごとにレンダリングされています（動的レンダリング）。しかし、ブログ記事はそれほど頻繁に更新されるわけではありません。そこで、ISR（インクリメンタル静的再生成）を導入して、パフォーマンスとコンテンツの鮮度を両立させます。

### 記事一覧ページのISR化

`app/page.tsx` を開き、`getPosts`関数内の`fetch`に`revalidate`オプションを追加します。

```tsx
// app/page.tsx

async function getPosts() {
  const res = await fetch('https://jsonplaceholder.typicode.com/posts', {
    // 60秒ごとにキャッシュを再検証
    next: { revalidate: 60 }, 
  });
  // ...
}

// ...
```

### 記事詳細ページのISR化

同様に、`app/posts/[id]/page.tsx` の `getPost` 関数も修正します。

```tsx
// app/posts/[id]/page.tsx

async function getPost(id: string) {
  const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${id}`, {
    // 60秒ごとにキャッシュを再検証
    next: { revalidate: 60 },
  });
  // ...
}

// ...
```

これで、一度アクセスされたページは60秒間キャッシュされ、非常に高速に表示されるようになります。60秒経過後のアクセスで、バックグラウンドでデータが更新されます。

## Step 4: Hydration Mismatchの体験と修正

次に、意図的にHydration Mismatchエラーを発生させ、その解決方法を学びます。

1.  記事詳細ページに、現在の時刻を表示するコンポーネントを追加してみましょう。まず、`components`ディレクトリを作成し、その中に`CurrentTime.tsx`を作成します。

    ```tsx
    // components/CurrentTime.tsx
    export function CurrentTime() {
      const time = new Date().toLocaleTimeString();
      return <span className="text-sm text-gray-500">表示時刻: {time}</span>;
    }
    ```

2.  `app/posts/[id]/page.tsx`で、このコンポーネントをインポートして使います。

    ```tsx
    // app/posts/[id]/page.tsx
    import { CurrentTime } from '@/components/CurrentTime';

    // ...
    export default async function PostDetailPage({ params }: { params: { id: string } }) {
      // ...
      return (
        <div className="max-w-4xl mx-auto p-4">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-4xl font-bold">{post.title}</h1>
            <CurrentTime /> { /* ← 追加 */ }
          </div>
          {/* ... */}
        </div>
      );
    }
    ```

3.  開発サーバーで記事詳細ページにアクセスし、ブラウザの開発者コンソールを確認してください。`"Text content does not match server-rendered HTML."` というHydration Mismatchエラーが表示されるはずです。

**エラーの修正:**

このエラーは、サーバー（UTC）とクライアント（あなたのローカルタイムゾーン）で`new Date().toLocaleTimeString()`の結果が異なるために発生します。`useEffect`を使って、クライアントサイドでのみ時刻を生成するように修正しましょう。

`components/CurrentTime.tsx`を以下のように書き換えます。

```tsx
// components/CurrentTime.tsx
"use client"; // クライアントコンポーネントにすることを宣言

import { useState, useEffect } from 'react';

export function CurrentTime() {
  const [time, setTime] = useState('');

  // useEffectはクライアントサイドでのみ実行される
  useEffect(() => {
    setTime(new Date().toLocaleTimeString());
  }, []);

  // 初回レンダリング時、timeは空文字列。これはサーバーと同じ。
  // ハイドレーション後、useEffectが実行されて時刻が表示される。
  return <span className="text-sm text-gray-500">表示時刻: {time}</span>;
}
```

これでエラーが解消され、時刻が正しく表示されることを確認してください。

## Step 5: 改善後のパフォーマンスを測定する

すべての最適化が完了したら、Step 1と同様に、再度Lighthouseでパフォーマンスを測定してみましょう。

`npm run build` と `npm start` で本番モードで起動し、ホームページと記事詳細ページの両方でレポートを生成します。

「Performance」スコアが向上し、特にLCPとCLSの数値が改善されているはずです。また、ページ間の遷移が非常に高速になっていることも体感できるでしょう。

## ✨ まとめ

このハンズオンを通じて、以下の実践的なスキルを習得しました。

-   Lighthouseを使ったパフォーマンス測定
-   `next/image`による画像の最適化
-   ISR (`revalidate`) を使ったキャッシュ戦略の導入
-   Hydration Mismatchエラーのデバッグと修正方法

これらのテクニックは、あらゆるNext.jsプロジェクトで応用可能な非常に重要なものです。パフォーマンスは一度改善して終わりではなく、継続的に監視し、改善していくものであることを心に留めておきましょう。

これで、Next.jsのレンダリングとパフォーマンスに関する学習は完了です。お疲れ様でした！
