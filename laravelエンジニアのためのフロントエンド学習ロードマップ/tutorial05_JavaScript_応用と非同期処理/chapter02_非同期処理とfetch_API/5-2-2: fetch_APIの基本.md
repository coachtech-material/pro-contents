# 5-2-2: fetch APIの基本

## 🎯 このセクションで学ぶこと

- `fetch` API を使って、外部のサーバーからデータを取得できるようになる
- `fetch` が返す `Response` オブジェクトの役割を理解する

## 導入

現代のWebアプリケーションでは、サーバーと通信して動的にデータを取得・表示することが不可欠です。`fetch` APIは、HTTPリクエストを簡単に行うための、モダンで強力な標準APIです。

このセクションでは、ダミーデータを返す **JSONPlaceholder** というサービスを使って、`fetch` の基本的な使い方を学びます。

## 詳細解説

### `fetch` の基本構文

`fetch` 関数は、引数にリクエストを送信したいURLを指定します。`fetch` は **Promise** を返し、そのPromiseはHTTPレスポンスを表す `Response` オブジェクトで解決されます。

```javascript
async function fetchData() {
  // JSONPlaceholderの投稿(posts)を1件取得する
  const response = await fetch('https://jsonplaceholder.typicode.com/posts/1');
  
  console.log(response);
  // Response { type: "cors", url: "...", status: 200, ok: true, ... }
}

fetchData();
```

`await fetch(...)` を実行すると、サーバーからのレスポンスヘッダーが到着した時点で `Response` オブジェクトが返されます。この時点では、まだレスポンスボディ（データ本体）のダウンロードは完了していません。

### `Response` オブジェクト

`Response` オブジェクトには、レスポンスに関する情報（ステータスコード、ヘッダーなど）が含まれています。

- **`response.status`**: HTTPステータスコード（例: `200`, `404`）
- **`response.ok`**: ステータスコードが成功（200-299）の範囲内であれば `true`

### レスポンスボディの取得

レスポンスボディを実際に取得するには、`Response` オブジェクトが提供するメソッドを使います。これらのメソッドもPromiseを返します。

- **`response.json()`**: レスポンスをJSONとして解釈する
- **`response.text()`**: レスポンスをプレーンテキストとして解釈する

```javascript
async function fetchData() {
  const response = await fetch('https://jsonplaceholder.typicode.com/posts/1');
  
  // レスポンスが成功したか確認
  if (!response.ok) {
    console.error('データの取得に失敗しました');
    return;
  }

  // レスポンスボディをJSONとして取得
  const post = await response.json();
  console.log(post);
  // { userId: 1, id: 1, title: "...", body: "..." }
}

fetchData();
```

`await response.json()` とすることで、レスポンスボディのダウンロードとJSONへのパースが完了するのを待ち、その結果を `post` 変数に格納しています。

## 💡 TIP

- `fetch` はデフォルトで `GET` リクエストを送信します。`POST` や `PUT` などのリクエストを送信する場合は、第二引数に設定オブジェクトを渡します。

## ✨ まとめ

- `fetch(url)` でHTTPリクエストを送信する
- `fetch` は `Response` オブジェクトで解決されるPromiseを返す
- `response.json()` でレスポンスボディをJSONとして取得する
として取得する
