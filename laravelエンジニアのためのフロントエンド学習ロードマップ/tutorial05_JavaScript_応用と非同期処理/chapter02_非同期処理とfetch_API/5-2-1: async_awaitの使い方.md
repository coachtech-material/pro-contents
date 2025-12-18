# 5-2-1: async/awaitの使い方

## 🎯 このセクションで学ぶこと

- `async/await` を使って、Promiseベースの非同期処理を同期処理のように直感的に書けるようになる
- `async` 関数が常にPromiseを返すことを理解する

## 導入

Chapter 1では `Promise` と `.then()` を使った非同期処理を学びましたが、処理が複雑になるとチェーンが長くなり、読みにくくなることがあります。

`async/await` は、この問題を解決し、非同期処理をまるで同期処理のようにシンプルに記述するための構文です。ES2017で導入されました。

## 1. async関数の基本

関数を `async` として宣言すると、その関数は常に **Promise** を返すようになります。

```javascript
// async関数は常にPromiseを返す
async function greet() {
  return "こんにちは";
}

// 以下と同じ意味
function greet() {
  return Promise.resolve("こんにちは");
}

// 使い方
greet().then((message) => {
  console.log(message); // "こんにちは"
});
```

## 2. await演算子

`await` は `async` 関数の中でのみ使用でき、Promiseが解決されるまで関数の実行を一時停止します。Promiseが解決されると、その結果を返します。

これにより、`.then()` を使わずに、Promiseの結果を直接変数に代入できます。

```javascript
// Promiseを返す関数
function fetchData() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ name: "太郎", age: 25 });
    }, 1000);
  });
}

// then を使った書き方
fetchData().then((data) => {
  console.log(data);
});

// async/await を使った書き方
async function getData() {
  const data = await fetchData(); // Promiseが解決されるまで待つ
  console.log(data);
}

getData();
```

## 3. Promiseチェーンとの比較

Chapter 1で学んだPromiseチェーンを、async/awaitで書き直してみましょう。

```javascript
// Promiseチェーン版
getUser(1)
  .then((user) => {
    console.log("ユーザー:", user.name);
    return getPosts(user.id);
  })
  .then((posts) => {
    console.log("投稿数:", posts.length);
    return getComments(posts[0].id);
  })
  .then((comments) => {
    console.log("コメント数:", comments.length);
  })
  .catch((error) => {
    console.error("エラー:", error);
  });

// async/await版（より直感的！）
async function fetchAllData() {
  try {
    const user = await getUser(1);
    console.log("ユーザー:", user.name);
    
    const posts = await getPosts(user.id);
    console.log("投稿数:", posts.length);
    
    const comments = await getComments(posts[0].id);
    console.log("コメント数:", comments.length);
  } catch (error) {
    console.error("エラー:", error);
  }
}

fetchAllData();
```

async/await版は、同期処理のように上から下へ順番に読めるため、非常に直感的です。

## 4. エラーハンドリング

async/awaitでは、`try/catch`を使ってエラーを処理します。

```javascript
async function fetchUser(id) {
  try {
    const response = await fetch(`https://api.example.com/users/${id}`);
    
    if (!response.ok) {
      throw new Error("ユーザーが見つかりません");
    }
    
    const user = await response.json();
    return user;
  } catch (error) {
    console.error("エラー:", error.message);
    return null;
  }
}
```

## 5. 並列実行

複数の非同期処理を並列で実行したい場合は、`Promise.all`と組み合わせます。

```javascript
// 順次実行（遅い）
async function sequential() {
  const user1 = await getUser(1); // 1秒待つ
  const user2 = await getUser(2); // さらに1秒待つ
  const user3 = await getUser(3); // さらに1秒待つ
  // 合計3秒
}

// 並列実行（速い）
async function parallel() {
  const [user1, user2, user3] = await Promise.all([
    getUser(1),
    getUser(2),
    getUser(3)
  ]);
  // 合計1秒（最も遅い処理の時間）
}
```

## 💡 TIP

- `await` は `async` 関数の中、もしくはモジュールのトップレベルでしか使えません。通常の関数内で使うと構文エラーになります。
- `await`を使うと処理が「待機」するため、並列実行したい場合は`Promise.all`を使いましょう。

## ✨ まとめ

| 項目 | 説明 |
|------|------|
| `async` | 関数がPromiseを返すことを示す |
| `await` | `async`関数内でPromiseの結果を待つ |
| エラー処理 | `try/catch`を使用 |
| 並列実行 | `Promise.all`と組み合わせる |

`async/await`を使うことで、非同期処理が同期処理のようにシンプルに書けます。次のセクションでは、実際のAPI通信に使う`fetch API`について学んでいきましょう。
