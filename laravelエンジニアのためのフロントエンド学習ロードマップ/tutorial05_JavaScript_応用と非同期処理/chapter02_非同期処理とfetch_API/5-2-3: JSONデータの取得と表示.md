# 5-2-3: JSONデータの取得と表示

## 🎯 このセクションで学ぶこと

- `fetch` で取得したJSONデータをDOMに反映させて、Webページに表示できるようになる
- データの配列をループ処理して、複数の要素を動的に生成する方法を習得する

## 導入

前のセクションで、`fetch` を使ってJSONデータをJavaScriptのオブジェクトとして取得する方法を学びました。このセクションでは、取得したデータを実際にWebページに表示する方法を学びます。

## 詳細解説

### データを表示する流れ

1. **データを取得する**: `fetch` と `async/await` を使ってAPIからデータを取得する。
2. **DOM要素を生成する**: 取得したデータをもとに、表示したいHTML要素（`<li>` や `<div>` など）を `document.createElement` で作成する。
3. **DOMに要素を追加する**: 作成した要素を、`appendChild` を使って既存のDOMツリーに追加する。

### 実装例：ユーザーリストの表示

JSONPlaceholderからユーザーのリストを取得し、`<ul>` タグの中に `<li>` 要素として表示する例を見てみましょう。

**HTML (`index.html`)**
```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>User List</title>
</head>
<body>
  <h1>User List</h1>
  <ul id="user-list"></ul>

  <script src="app.js"></script>
</body>
</html>
```

**JavaScript (`app.js`)**
```javascript
async function displayUsers() {
  // ユーザーリストを表示するul要素を取得
  const userList = document.querySelector("#user-list");

  // 1. データを取得する
  const response = await fetch("https://jsonplaceholder.typicode.com/users");
  const users = await response.json();

  // 2. 取得したユーザーデータの配列をループ処理
  users.forEach(user => {
    // 3. 各ユーザーごとにli要素を生成
    const listItem = document.createElement("li");
    listItem.textContent = user.name;

    // 4. ul要素にli要素を追加
    userList.appendChild(listItem);
  });
}

displayUsers();
```

このコードを実行すると、APIから取得した10人分のユーザー名がリストとしてページに表示されます。

## 💡 TIP

- `forEach` の代わりに `map` と `join` を使ってHTML文字列を一度に生成し、`innerHTML` に代入する方法もあります。大量のデータを扱う場合は、こちらのほうがパフォーマンスが良いことがあります。

## ✨ まとめ

- `fetch` で取得したデータ（配列）を `forEach` でループ処理する
- ループの中で `document.createElement` を使って表示用のDOM要素を作成する
- `appendChild` で作成した要素をDOMに追加してページに反映させる
