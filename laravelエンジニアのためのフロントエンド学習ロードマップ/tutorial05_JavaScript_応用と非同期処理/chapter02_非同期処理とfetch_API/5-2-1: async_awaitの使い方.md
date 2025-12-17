# 5-2-1: async/awaitの使い方

## 🎯 このセクションで学ぶこと

- `async/await` を使って、Promiseベースの非同期処理を同期処理のように直感的に書けるようになる
- `async` 関数が常にPromiseを返すことを理解する

## 導入

Tutorial 5の旧Chapter 3では `Promise` と `.then()` を使った非同期処理を学びましたが、処理が複雑になるとネストが深くなり、読みにくくなる（コールバック地獄）という問題がありました。

`async/await` は、この問題を解決し、非同期処理をまるで同期処理のようにシンプルに記述するための構文です。

## 詳細解説

### `async` 関数

関数を `async` として宣言すると、その関数は常に **Promise** を返すようになります。関数の前に `async` キーワードを置くだけです。

```javascript
async function myFunction() {
  return "Hello";
}

myFunction().then(alert); // "Hello"
```

### `await` 演算子

`await` は `async` 関数の中でのみ使用でき、Promiseが解決されるまで関数の実行を一時停止します。Promiseが解決されると、その結果を返します。

これにより、`.then()` を使わずに、Promiseの結果を直接変数に代入できます。

```javascript
// Promiseを返す関数の例
function resolveAfter2Seconds() {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve('resolved');
    }, 2000);
  });
}

async function asyncCall() {
  console.log('calling');
  const result = await resolveAfter2Seconds();
  console.log(result); // 2秒後に 'resolved' と表示される
}

asyncCall();
```

上記の `asyncCall` 関数は、`resolveAfter2Seconds` が完了するまで `await` の行で待機します。これにより、コードが上から下へ順番に実行されるように見え、非常に直感的になります。

## 💡 TIP

- `await` は `async` 関数の中、もしくはモジュールのトップレベルでしか使えません。通常の関数内で使うと構文エラーになります。

## ✨ まとめ

- `async` は関数がPromiseを返すことを示す
- `await` は `async` 関数内でPromiseの結果を待つために使う
- `async/await` を使うことで、非同期処理が同期処理のようにシンプルに書ける
ける
