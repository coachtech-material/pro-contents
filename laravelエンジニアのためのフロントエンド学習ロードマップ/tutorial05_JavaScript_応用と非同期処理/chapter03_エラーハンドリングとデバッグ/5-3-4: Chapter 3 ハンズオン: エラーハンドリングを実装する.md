# 5-3-4: 実践 🚀 チャプターハンズオン

## 🎯 課題

**Chapter 2で作成した「ブログ投稿一覧ページ」に、このチャプターで学んだエラーハンドリングと状態管理を実装しましょう。**

### 完成要件

1.  **ローディング表示**: APIからデータを取得している最中は、「読み込み中...」というテキストが表示されること。
2.  **エラー表示**: APIからのデータ取得に失敗した場合（例: オフライン、URLの間違い）、「エラーが発生しました。時間をおいて再読み込みしてください。」というテキストが表示されること。
3.  **Empty表示**: データ取得に成功したものの、投稿が1件もなかった場合、「投稿がありません。」と表示されること。
4.  **データ表示**: データ取得に成功し、投稿が1件以上ある場合は、これまで通り投稿の一覧がカード形式で表示されること。

## 🛠️ 手順

1.  **HTMLの準備**: Chapter 2で作成した `index.html` に、ローディング、エラー、Empty状態を表示するための要素（例: `<div id="loading">`, `<div id="error">`, `<div id="empty">`）を追加します。CSSでこれらの要素を初期状態では非表示（`display: none;`）にしておきます。

2.  **JavaScriptの準備**: `app.js` の `fetchPosts` 関数を修正します。

3.  **状態管理の実装**: `fetch` を呼び出す前に、ローディング要素を表示し、他の要素（リスト、エラー、Empty）を非表示にします。

4.  **エラーハンドリングの実装**: `fetch` を含む非同期処理全体を `try...catch` ブロックで囲みます。
    -   `catch` ブロックでは、ローディング要素を非表示にし、エラー要素を表示するようにします。

5.  **成功時の処理**: `try` ブロック内で、データ取得に成功した後の処理を実装します。
    -   まずローディング要素を非表示にします。
    -   取得した `posts` 配列の `length` を確認します。
    -   `length` が `0` ならば、Empty要素を表示します。
    -   `length` が `1` 以上ならば、リスト要素を表示し、投稿データを描画します。

## 🏆 解答例

**HTML (`index.html`)**
```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>Blog Posts with State Handling</title>
  <style>
    .post-card { border: 1px solid #ccc; border-radius: 8px; padding: 16px; margin-bottom: 10px; }
    /* 初期状態では状態表示用の要素を隠す */
    #loading, #error, #empty {
      display: none;
      font-size: 1.2em;
      color: #555;
    }
    #error { color: red; }
  </style>
</head>
<body>
  <h1>Blog Posts</h1>

  <!-- コンテナ -->
  <div id="posts-container"></div>
  
  <!-- 状態表示 -->
  <div id="loading">読み込み中...</div>
  <div id="error">エラーが発生しました。時間をおいて再読み込みしてください。</div>
  <div id="empty">投稿がありません。</div>

  <script src="app.js"></script>
</body>
</html>
```

**JavaScript (`app.js`)**
```javascript
// UI要素を取得
const postsContainer = document.querySelector("#posts-container");
const loading = document.querySelector("#loading");
const error = document.querySelector("#error");
const empty = document.querySelector("#empty");

// 要素の表示・非表示を管理する関数
function show(element) { element.style.display = 'block'; }
function hide(element) { element.style.display = 'none'; }

async function fetchPosts() {
  // 1. 初期化：ローディング表示
  show(loading);
  hide(postsContainer);
  hide(error);
  hide(empty);

  try {
    const response = await fetch("https://jsonplaceholder.typicode.com/posts");

    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }

    const posts = await response.json();
    
    // 成功したのでローディングを非表示
    hide(loading);

    // 2. 成功時の状態分岐
    if (posts.length === 0) {
      // データが空の場合
      show(empty);
    } else {
      // データがある場合
      show(postsContainer);
      postsContainer.innerHTML = ''; // コンテナをクリア
      posts.forEach(post => {
        const card = document.createElement("div");
        card.className = "post-card";
        card.innerHTML = `<h2>${post.title}</h2><p>${post.body}</p>`;
        postsContainer.appendChild(card);
      });
    }

  } catch (e) {
    // 3. エラー発生時の状態
    hide(loading);
    show(error);
    console.error('投稿の取得に失敗しました:', e);
  }
}

// 実行
fetchPosts();
```
