# 5-3-3: Loading/Error/Empty状態の管理

## 🎯 このセクションで学ぶこと

- 非同期処理におけるUIの3つの主要な状態（ローディング、エラー、データ有り/無し）を理解する
- ユーザー体験を向上させるために、これらの状態をUIに適切に反映させる方法を習得する

## 導入

APIからデータを取得する際、データがすぐに手に入るわけではありません。通信には時間がかかりますし、失敗することもあります。また、成功してもデータが1件も存在しない場合もあります。

優れたUIは、こうした様々な状況をユーザーに明確に伝えます。このセクションでは、非同期処理における代表的な3つの状態、「**ローディング（Loading）**」「**エラー（Error）**」「**データが空（Empty）**」を管理する実践的なパターンを学びます。これは、実務でWebアプリケーションを構築する上で、ほぼ必須となる非常に重要な考え方です。

## 詳細解説

### なぜ状態管理が重要なのか？

- **ユーザー体験の向上**: 画面が固まったように見えると、ユーザーは不安になります。ローディング表示を出すことで、「今、処理中である」ことを伝え、安心感を与えます。
- **明確なフィードバック**: エラーが発生した際に、その旨を伝えなければ、ユーザーは何が起こったのか理解できません。適切なエラーメッセージは、ユーザーが次のアクションを取る手助けになります。
- **エッジケースへの対応**: データが0件の場合と、データがまだ読み込まれていない状態は、明確に区別して表示する必要があります。「データがありません」というメッセージは、システムが正常に動作した結果であることを示します。

### 状態管理の実装パターン

状態に応じて表示を切り替えるための、シンプルで効果的な実装パターンを見ていきましょう。

**HTML (`index.html`)**

まず、各状態に対応するUI要素をあらかじめHTMLに用意しておきます。

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>State Management Example</title>
  <style>
    /* 最初はデータリスト以外を非表示にしておく */
    #loading, #error, #empty {
      display: none;
    }
  </style>
</head>
<body>
  <h1>User List</h1>

  <!-- データ表示エリア -->
  <ul id="user-list"></ul>

  <!-- ローディング表示 -->
  <div id="loading">データを読み込み中です...</div>

  <!-- エラー表示 -->
  <div id="error">エラーが発生しました。</div>

  <!-- データが空の場合の表示 -->
  <div id="empty">ユーザーデータが見つかりません。</div>

  <script src="app.js"></script>
</body>
</html>
```

**JavaScript (`app.js`)**

JavaScript側で、処理の進行状況に合わせてこれらの要素の表示・非表示を切り替えます。

```javascript
// 各UI要素を取得
const userList = document.querySelector("#user-list");
const loading = document.querySelector("#loading");
const error = document.querySelector("#error");
const empty = document.querySelector("#empty");

// UIの状態を更新するヘルパー関数
function showElement(element) {
  element.style.display = 'block';
}
function hideElement(element) {
  element.style.display = 'none';
}

async function fetchAndDisplayUsers() {
  // --- 1. ローディング状態 --- 
  showElement(loading);
  hideElement(userList);
  hideElement(error);
  hideElement(empty);

  try {
    const response = await fetch("https://jsonplaceholder.typicode.com/users");
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const users = await response.json();

    // --- 2. データ表示 or Empty状態 --- 
    hideElement(loading);

    if (users.length === 0) {
      // データが空の場合
      showElement(empty);
    } else {
      // データがある場合
      showElement(userList);
      users.forEach(user => {
        const listItem = document.createElement("li");
        listItem.textContent = user.name;
        userList.appendChild(listItem);
      });
    }

  } catch (e) {
    // --- 3. エラー状態 ---
    hideElement(loading);
    showElement(error);
    console.error('Fetch error:', e);
  }
}

// 実行
fetchAndDisplayUsers();
```

### コードのポイント

1.  **初期状態**: `fetch` を呼び出す直前に、まずローディング表示を `show` し、他の要素を `hide` します。これにより、処理が開始されたことをユーザーに伝えます。
2.  **成功時**: データ取得に成功したら、ローディング表示を `hide` します。
    -   取得したデータの件数（`users.length`）をチェックし、`0` であればEmpty表示を `show` します。
    -   データが1件以上あれば、データリストを表示します。
3.  **失敗時**: `catch` ブロックでエラーを捕捉したら、ローディング表示を `hide` し、エラー表示を `show` します。これにより、何らかの問題が発生したことをユーザーに伝えます。

## 💡 TIP

- このような状態管理は、後のチュートリアルで学ぶReactなどのUIライブラリ/フレームワークを使うと、より宣言的でシンプルに記述できます。しかし、ここで学んだ基本的な考え方は、どのような技術を使っても変わりません。

## ✨ まとめ

- 非同期処理を伴うUIでは、「ローディング」「エラー」「データ有り/無し」の状態を意識することが重要。
- 各状態に対応するUI要素をあらかじめ用意し、JavaScriptで表示・非表示を制御することで、堅牢でユーザーフレンドリーなアプリケーションを構築できる。
