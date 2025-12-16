# Tutorial 5: JavaScript応用と非同期処理

## Chapter 3: 非同期処理の基礎

### Chapter 3 ハンズオン: ユーザー情報をAPIから取得する

🎯 **このハンズオンで達成すること**

-   `fetch` APIを使い、外部のAPIサーバーからデータを取得する方法を習得する。
-   `fetch`が返すPromiseを、`async/await`を使ってエレガントに処理できるようになる。
-   API通信における成功と失敗のケースを、`try...catch`を使って適切にハンドリングできるようになる。
-   取得したデータをDOM操作でWebページに表示する、というフロントエンド開発の王道パターンを体験する。

--- 

🖼️ **完成イメージ**

ボタンをクリックすると、ダミーのAPIサーバーからユーザー情報を取得し、その名前とメールアドレスをWebページ上に表示します。APIの取得に失敗した場合は、エラーメッセージを表示します。

**成功時:**
![成功時のイメージ](https://placehold.jp/600x200.png?text=Success!%0AUser:%20Leanne%20Graham%0AEmail:%20Sincere@april.biz)

**失敗時:**
![失敗時のイメージ](https://placehold.jp/600x200.png?text=Error!%0Aデータの取得に失敗しました)

--- 

### 🧠 先輩エンジニアの思考プロセス

「ボタンを押したらAPIを叩いて、結果を画面に出して」というタスクは、フロントエンド開発の典型です。このタスクを分解すると、以下のようになります。

1.  **トリガー:** まず、どのタイミングで処理を開始するか？ → 「ボタンがクリックされたとき」だな。`addEventListener`を使おう。
2.  **非同期処理:** 次に、どうやって外部のAPIと通信するか？ → `fetch` APIを使うのが標準だ。`fetch`はPromiseを返すから、`async/await`で待つのが一番キレイに書けるな。
3.  **データ変換:** `fetch`が成功したら、レスポンスが返ってくる。でもこれは生データだから、使いやすいようにJSON形式に変換する必要がある。`response.json()`もPromiseを返すから、これも`await`しよう。
4.  **成功時の処理:** JSONデータが手に入ったら、その中から必要な情報（名前、メール）を取り出して、DOM操作でHTML要素に中身をセットして表示すればOK。
5.  **失敗時の処理:** もし`fetch`や`response.json()`の途中で何か問題が起きたら？ → 通信エラーやサーバーエラーだな。`try...catch`で全体を囲っておいて、`catch`ブロックでエラーメッセージを表示するようにすれば、ユーザーにも親切だ。

この思考プロセスを、そのままコードに落とし込んでいきましょう。

--- 

### 🏃 実践: Step by StepでAPI通信を実装しよう

#### Step 1: HTMLの準備

ボタンと、結果を表示するための`div`要素を用意します。

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>API Fetch Hands-on</title>
</head>
<body>
  <h1>ユーザー情報</h1>
  <button id="fetch-button">ユーザー情報を取得</button>
  <div id="user-info"></div>

  <script src="script.js"></script>
</body>
</html>
```

#### Step 2: JavaScriptの骨格と`fetch` API

`script.js`を作成し、DOM要素の取得とイベントリスナーの設定を行います。今回は、ダミーデータを提供してくれる[JSONPlaceholder](https://jsonplaceholder.typicode.com/)というサービスを使います。

```javascript
// script.js

const fetchButton = document.getElementById("fetch-button");
const userInfoDiv = document.getElementById("user-info");

// APIのエンドポイントURL
const API_URL = "https://jsonplaceholder.typicode.com/users/1";

const fetchUser = async () => {
  // ここにAPI通信のロジックを書いていく
};

fetchButton.addEventListener("click", fetchUser);
```

`fetch` APIは、引数にURLを取るだけで、そのURLに対してHTTPリクエストを送信してくれます。そして、レスポンスに関する情報を持つ**Responseオブジェクト**で解決されるPromiseを返します。

#### Step 3: `async/await`でAPIからデータを取得する

`fetchUser`関数の中身を実装します。`try...catch`で全体を囲むのが定石です。

```javascript
// script.js

// ... (省略)

const fetchUser = async () => {
  userInfoDiv.innerHTML = "ローディング中..."; // ユーザーへのフィードバック

  try {
    // 1. APIにリクエストを送信し、レスポンスを待つ
    const response = await fetch(API_URL);

    // 2. レスポンスが正常かどうかをチェック
    if (!response.ok) {
      // response.okがfalseの場合（404や500エラーなど）、エラーを投げる
      throw new Error(`HTTPエラー: ${response.status}`);
    }

    // 3. レスポンスのボディをJSONとして解析するのを待つ
    const user = await response.json();

    // 4. 成功時の処理：取得したデータを画面に表示
    userInfoDiv.innerHTML = `
      <p><strong>名前:</strong> ${user.name}</p>
      <p><strong>Email:</strong> ${user.email}</p>
    `;

  } catch (error) {
    // 5. 失敗時の処理：エラーメッセージを画面に表示
    console.error("データの取得に失敗しました", error);
    userInfoDiv.innerHTML = `<p style="color: red;">データの取得に失敗しました</p>`;
  }
};

fetchButton.addEventListener("click", fetchUser);
```

-   **コードリーディング**
    1.  `await fetch(API_URL)`: サーバーからの最初の応答（ヘッダーなど）が返ってくるまで待ちます。
    2.  `if (!response.ok)`: `fetch`は、404 Not Foundや500 Internal Server ErrorのようなHTTPエラーが発生しても、Promiseを`reject`しません。通信自体は成功したとみなすためです。そのため、`response.ok`プロパティ（ステータスコードが200番台なら`true`）を自分でチェックし、問題があれば`throw new Error()`で意図的にエラーを発生させ、`catch`ブロックに処理を移すのがベストプラクティスです。
    3.  `await response.json()`: レスポンスのボディ（本体）のダウンロードと、それをJSONとして解析する非同期処理を待ちます。これが完了すると、JavaScriptのオブジェクト（`user`）が手に入ります。
    4.  成功すれば、`user`オブジェクトを使ってHTMLを組み立て、`innerHTML`で表示します。
    5.  `fetch`自体が失敗した場合（ネットワーク接続がないなど）や、`throw new Error()`で投げたエラーは、`catch`ブロックで捕捉されます。

--- 

✨ **まとめ**

-   `fetch(URL)`は、外部APIと通信するための標準的な関数であり、**Promiseを返す**。
-   `async/await`と`try...catch`を組み合わせることで、API通信の成功・失敗を伴う一連の処理を、非常にクリーンで読みやすく記述できる。
-   `fetch`のPromiseは、サーバーがエラー（404, 500など）を返しても`reject`されない。`response.ok`をチェックして、明示的にエラーを`throw`するのが堅牢な実装のコツ。
-   「イベント発火 → `async`関数呼び出し → `try...catch`で`await fetch` → 成功ならDOM更新、失敗ならエラー表示」は、フロントエンド開発における最も基本的かつ重要なパターンである。

📝 **学習のポイント**

-   [ ] `API_URL`の末尾の数字を`999`のように存在しないIDに変えて実行してみてください。`catch`ブロックで設定したエラーメッセージが正しく表示されることを確認しましょう。
-   [ ] `response.json()`は何を返すのでしょうか？また、なぜここでも`await`が必要なのでしょうか？
-   [ ] 今回のハンズオンのコードを、`async/await`を使わずに、`.then()`と`.catch()`だけで書き換えてみてください。どちらの書き方の方が読みやすいと感じますか？
