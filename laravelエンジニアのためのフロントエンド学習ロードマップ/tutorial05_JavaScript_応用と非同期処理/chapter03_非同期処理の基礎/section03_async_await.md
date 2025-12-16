# Tutorial 5: JavaScript応用と非同期処理

## Chapter 3: 非同期処理の基礎

### Section 3: async/await

🎯 **このセクションで学ぶこと**

-   `async/await`を使い、Promiseを扱う非同期処理を、まるで**同期処理のように**直感的に記述できるようになる。
-   `async`関数とは何か、常にPromiseを返す関数であることを理解する。
-   `await`キーワードが使える場所と、その役割を理解する。
-   `try...catch`構文を使い、`async/await`におけるエラーハンドリングを行う方法を習得する。

--- 

### イントロダクション：非同期処理の「最終形態」

Promiseと`.then()`チェーンは、コールバック地獄を解決する画期的な方法でした。しかし、チェーンが長くなると、やはりコードがネストしているように見え、少し読みにくくなることがあります。

```javascript
// .then()チェーンの例
step1()
  .then(result1 => step2(result1))
  .then(result2 => step3(result2))
  .then(result3 => {
    // ...
  })
  .catch(error => console.error(error));
```

このPromiseベースの非同期処理を、さらに直感的で、まるで**普通の同期処理のコードのように**書けるようにする構文が、ES2017で導入された`async/await`です。

`async/await`は、Promiseの上に成り立っている「シンタックスシュガー（糖衣構文）」です。つまり、内部的にはPromiseが動いていますが、それをより人間に分かりやすい書き方で覆い隠してくれているのです。現代のJavaScriptにおける非同期処理の記述方法は、この`async/await`がデファクトスタンダードとなっています。

--- 

### ⚙️ `async/await`の基本構文

`async/await`は、2つのキーワードの組み合わせで使います。

1.  **`async`**: 関数を「非同期関数」にする
    -   `function`やアロー関数の前に`async`を付けると、その関数は**非同期関数**になります。
    -   非同期関数は、常に**Promiseを返す**という重要な特徴があります。（たとえ`return`で普通の値を返しても、自動的にその値で解決されるPromiseにラップされます）

2.  **`await`**: Promiseの結果が出るまで「待つ」
    -   `await`は、**`async`関数の中でのみ**使用できます。
    -   `await`の後ろにはPromiseオブジェクトを置きます。
    -   `await`は、そのPromiseが`fulfilled`（成功）になるまで、関数の実行を**一時停止**し、結果が返ってきたら、その**成功した値**を返します。

**例：**
```javascript
// 2秒後に"美味しいパスタ"を返すPromise
const getDish = new Promise((resolve) => {
  setTimeout(() => {
    resolve("美味しいパスタ");
  }, 2000);
});

// async/awaitを使った書き方
const main = async () => {
  console.log("パスタを注文しました。");

  // getDishのPromiseが解決されるまで、ここで処理が「待機」する
  const dish = await getDish;

  // 2秒後、上の行が完了してから、ここが実行される
  console.log(`受け取ったもの: ${dish}`);
};

main();

// 出力:
// パスタを注文しました。
// (2秒後)
// 受け取ったもの: 美味しいパスタ
```

`.then()`を使ったコードと比べてみてください。非同期処理の結果を、まるで同期処理のように、変数`dish`に直接代入できています。コードの流れが上から下へ、非常に自然で読みやすいことがわかります。

--- 

### ⚙️ エラーハンドリング：`try...catch`

`async/await`構文では、`.catch()`メソッドを使いません。代わりに、通常の同期処理と同じように、`try...catch`構文を使ってエラーを捕捉します。

-   **`try`ブロック**: Promiseが成功する可能性のある、`await`を含むコードをこの中に書きます。
-   **`catch`ブロック**: `try`ブロック内で`await`したPromiseが`rejected`（失敗）になった場合、または他の同期的なエラーが発生した場合に、このブロックが実行されます。引数にはエラーオブジェクトが渡されます。

**例：**
```javascript
// 2秒後に失敗するPromise
const getDish = new Promise((resolve, reject) => {
  setTimeout(() => {
    reject("パスタが品切れでした");
  }, 2000);
});

const main = async () => {
  console.log("パスタを注文しました。");
  try {
    const dish = await getDish; // ここでPromiseがrejectされる
    console.log(`受け取ったもの: ${dish}`); // この行は実行されない
  } catch (error) {
    // Promiseのreject理由がerrorに渡され、catchブロックが実行される
    console.error(`エラー: ${error}`);
  }
};

main();

// 出力:
// パスタを注文しました。
// (2秒後)
// エラー: パスタが品切れでした
```

`try...catch`は、非同期的なエラー（Promiseの失敗）も、同期的なエラーも、同じ構文で一元的に扱えるというメリットがあります。

--- 

✨ **まとめ**

-   `async/await`は、Promiseベースの非同期処理を、同期処理のような見た目で直感的に書くためのシンタックスシュガーである。
-   `async`を付けた関数は**非同期関数**となり、必ず**Promiseを返す**。
-   `await`は**`async`関数の中でのみ**使え、Promiseの結果が返るまで処理を一時停止し、成功した値を返す。
-   `async/await`におけるエラーハンドリングは、`.catch()`ではなく、同期処理と同じ**`try...catch`構文**を使用する。

📝 **学習のポイント**

-   [ ] `async/await`は、何の問題を解決するために導入されたのでしょうか？`.then()`チェーンと比較したメリットを説明してください。
-   [ ] `await`キーワードが使えるのは、どのような場所ですか？
-   [ ] 前のセクションで使った「成功するPromise」と「失敗するPromise」の両方を、`async/await`と`try...catch`を使って書き直してみてください。
