# 5-2-4: 実践 🚀 チャプターハンズオン

## 🎯 課題

**JSONPlaceholder API を使って、ブログ投稿の一覧を表示するWebページを作成しましょう。**

### 完成イメージ

- ページには「Blog Posts」という見出しがある。
- APIから取得した投稿が、それぞれカード形式で表示される。
- 各カードには、投稿のタイトルと本文が表示される。

### 使用するAPIエンドポイント

- `https://jsonplaceholder.typicode.com/posts`

## 🛠️ 手順

1. **HTMLファイルの作成**: `index.html` を作成し、基本的な構造（`<h1>`, `<div>` など）を用意します。投稿カードを表示するためのコンテナとなる要素（例: `<div id="posts-container"></div>`）を配置してください。

2. **JavaScriptファイルの作成**: `app.js` を作成し、`index.html` から読み込みます。

3. **非同期関数の作成**: `fetchPosts` という `async` 関数を定義します。

4. **データの取得**: `fetchPosts` 関数の中で、`fetch` を使って上記のAPIエンドポイントから投稿データを取得します。

5. **DOM操作**: 取得した投稿データの配列をループ処理し、各投稿に対して以下の要素を生成してDOMに追加します。
   - 投稿全体を囲む `div` 要素（カード）
   - タイトルを表示する `h2` 要素
   - 本文を表示する `p` 要素

6. **スタイリング（任意）**: 簡単なCSSを書いて、カード形式のデザインを整えてみましょう。

## 🏆 解答例

**HTML (`index.html`)**
```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>Blog Posts</title>
  <style>
    #posts-container {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 20px;
    }
    .post-card {
      border: 1px solid #ccc;
      border-radius: 8px;
      padding: 16px;
    }
  </style>
</head>
<body>
  <h1>Blog Posts</h1>
  <div id="posts-container"></div>

  <script src="app.js"></script>
</body>
</html>
```

**JavaScript (`app.js`)**
```javascript
async function fetchPosts() {
  const postsContainer = document.querySelector("#posts-container");

  try {
    const response = await fetch("https://jsonplaceholder.typicode.com/posts");
    const posts = await response.json();

    posts.forEach(post => {
      // カード要素を作成
      const card = document.createElement("div");
      card.classList.add("post-card");

      // タイトル要素を作成
      const title = document.createElement("h2");
      title.textContent = post.title;

      // 本文要素を作成
      const body = document.createElement("p");
      body.textContent = post.body;

      // カードにタイトルと本文を追加
      card.appendChild(title);
      card.appendChild(body);

      // コンテナにカードを追加
      postsContainer.appendChild(card);
    });

  } catch (error) {
    console.error("投稿の取得に失敗しました:", error);
    postsContainer.textContent = "投稿の取得に失敗しました。";
  }
}

fetchPosts();
```
