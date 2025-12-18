# 9-2-5: 実践 🚀 Chapter 2 ハンズオン: ブログを作成する

## 🎯 このハンズオンの目的

このチャプターで学んだApp Routerの主要な機能を総動員して、シンプルなブログアプリケーションを構築します。具体的には、以下の要素をすべて統合します。

-   **ファイルベースルーティング**: ブログのトップページ (`/blog`) を作成する。
-   **動的ルーティング**: 個別の記事ページ (`/blog/[slug]`) を作成する。
-   **データ取得**: `fetch`を使って、ダミーAPIからブログ記事のデータを取得する。
-   **Loading UI**: データ取得中に表示されるローディング状態を`loading.tsx`で実装する。
-   **Error UI**: データ取得失敗時に表示されるエラー状態を`error.tsx`で実装する。

このハンズオンを通して、Next.js App Routerにおける基本的なページの作成からデータ連携、状態管理までの一連の流れを実践的に習得します。

## 事前準備

-   Next.jsプロジェクトがセットアップされていること。
-   ダミーデータとして、[JSONPlaceholder](https://jsonplaceholder.typicode.com/) の `/posts` エンドポイントを利用します。

## ハンズオン

### ステップ1: ブログ一覧ページの作成

まず、すべてのブログ記事のタイトルを一覧表示するページ `/blog` を作成します。

1.  `app`ディレクトリ内に`blog`という名前のフォルダを作成します。
2.  `app/blog/`内に`page.tsx`ファイルを作成し、以下のコードを記述します。

```tsx
// app/blog/page.tsx
import Link from "next/link";

interface Post {
  id: number;
  title: string;
}

async function getPosts() {
  const res = await fetch("https://jsonplaceholder.typicode.com/posts", {
    // ISR: 60秒ごとに再検証
    next: { revalidate: 60 },
  });

  if (!res.ok) {
    throw new Error("Failed to fetch posts");
  }

  return res.json();
}

export default async function BlogPage() {
  const posts: Post[] = await getPosts();

  return (
    <div>
      <h1>Blog</h1>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <Link href={`/blog/${post.id}`}>{post.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

**ポイント**:
-   ページコンポーネントを`async`関数にし、直接データを`fetch`しています。
-   取得した記事一覧を`map`でループし、各記事へのリンクを`next/link`で作成しています。リンク先は`/blog/記事のID`という動的なパスになっています。
-   ISR（Incremental Static Regeneration）を有効にするため、`revalidate: 60`を設定しています。

### ステップ2: ローディングとエラーUIの追加

データ取得中とエラー発生時のUIを、`loading.tsx`と`error.tsx`を使って作成します。

1.  `app/blog/`内に`loading.tsx`を作成します。

```tsx
// app/blog/loading.tsx
export default function Loading() {
  return <div>Loading posts...</div>;
}
```

2.  `app/blog/`内に`error.tsx`を作成します。

```tsx
// app/blog/error.tsx
"use client";

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <h2>Something went wrong while fetching posts!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

これで、`/blog`にアクセスした際に、データ取得中は「Loading posts...」と表示され、APIリクエストが失敗した場合はエラーメッセージと再試行ボタンが表示されるようになります。

### ステップ3: ブログ記事詳細ページの作成

次に、動的ルーティングを使って、個別のブログ記事を表示するページ `/blog/[id]` を作成します。

1.  `app/blog/`内に`[id]`という名前のフォルダを作成します。（`[slug]`でも良いですが、今回はIDを使うので`[id]`とします）
2.  `app/blog/[id]/`内に`page.tsx`ファイルを作成し、以下のコードを記述します。

```tsx
// app/blog/[id]/page.tsx

interface Post {
  id: number;
  title: string;
  body: string;
}

async function getPost(id: string) {
  const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${id}`, {
    next: { revalidate: 60 },
  });

  if (!res.ok) {
    throw new Error("Failed to fetch post");
  }

  return res.json();
}

export default async function PostDetailPage({ params }: { params: { id: string } }) {
  const post: Post = await getPost(params.id);

  return (
    <div>
      <h1>{post.title}</h1>
      <p>{post.body}</p>
    </div>
  );
}
```

**ポイント**:
-   フォルダ名を`[id]`とすることで、URLの`/blog/`に続く部分が`id`というパラメータとしてコンポーネントに渡されます。
-   `params.id`を使って、特定のIDの記事データを取得するAPIを叩いています。

### ステップ4: 詳細ページのローディングとエラーUI

一覧ページと同様に、詳細ページにもローディングとエラーのUIを追加しましょう。

1.  `app/blog/[id]/`内に`loading.tsx`を作成します。

```tsx
// app/blog/[id]/loading.tsx
export default function Loading() {
  return <div>Loading single post...</div>;
}
```

2.  `app/blog/[id]/`内に`error.tsx`を作成します。

```tsx
// app/blog/[id]/error.tsx
"use client";

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <h2>Could not load the post.</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

### ステップ5: 動作確認

アプリケーションを起動し、以下のパスにアクセスして動作を確認してみましょう。

1.  `/blog`にアクセスします。
    -   一瞬「Loading posts...」と表示された後、ブログ記事のタイトル一覧が表示されるはずです。
2.  一覧からいずれかの記事タイトルをクリックします。
    -   `/blog/1`のようなURLに遷移します。
    -   一瞬「Loading single post...」と表示された後、記事のタイトルと本文が表示されるはずです。

## ✨ まとめ

このハンズオンを通じて、Next.js App Routerの基本的な機能を一通り体験しました。

-   `app/blog/page.tsx`で記事一覧ページを**ファイルベースで作成**しました。
-   `app/blog/[id]/page.tsx`で記事詳細ページを**動的ルーティングで作成**しました。
-   両方のページで、Server Components内での`async/await`を使った**データ取得**を行いました。
-   `loading.tsx`と`error.tsx`をそれぞれの階層に配置することで、**宣言的なローディング/エラーハンドリング**を実現しました。

これらの機能を組み合わせることで、非常に少ないコードで、パフォーマンスが高く、堅牢なWebアプリケーションを構築できることが体感できたはずです。この基本パターンは、あらゆる種類のデータ駆動型アプリケーションに応用できます。
