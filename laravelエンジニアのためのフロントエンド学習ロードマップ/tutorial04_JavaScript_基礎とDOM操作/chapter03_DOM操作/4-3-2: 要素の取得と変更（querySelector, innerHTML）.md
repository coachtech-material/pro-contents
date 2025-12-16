# 4-3-2: 要素の取得と変更（querySelector, innerHTML）

## 🎯 このセクションで学ぶこと

- `querySelector` を使ってDOMから特定の要素を取得できるようになる
- `innerHTML` プロパティを使って要素の内容を書き換えられるようになる
- `textContent` と `innerHTML` の違いを理解する

## 導入

DOMを操作する第一歩は、操作したいHTML要素をJavaScriptで取得することです。`querySelector` メソッドを使うと、CSSセレクタと同じ記法で簡単に要素を取得できます。

## 詳細解説

### `querySelector` と `querySelectorAll`

- **`document.querySelector()`**: CSSセレクタに一致する**最初の要素**を1つだけ返します。
- **`document.querySelectorAll()`**: CSSセレクタに一致する**すべての要素**を `NodeList`（配列のようなオブジェクト）として返します。

```javascript
// IDで要素を取得
const mainTitle = document.querySelector("#main-title");

// クラスで最初の要素を取得
const firstItem = document.querySelector(".list-item");

// クラスで全ての要素を取得
const allItems = document.querySelectorAll(".list-item");

// allItemsはNodeListなので、forEachでループ処理できる
allItems.forEach(item => {
  console.log(item.textContent);
});
```

### `innerHTML` と `textContent`

要素を取得したら、その内容を読み取ったり書き換えたりできます。

- **`innerHTML`**: 要素内のHTMLタグを含めた内容を取得・設定します。
- **`textContent`**: 要素内のテキストコンテンツだけを取得・設定します。

```javascript
const content = document.querySelector("#content");

// 内容を書き換える
content.innerHTML = "<h2>新しいタイトル</h2><p>これは新しい段落です。</p>";

// テキストだけを取得
console.log(content.textContent);
// "新しいタイトルこれは新しい段落です。"
```

## 💡 TIP

- ユーザーからの入力を `innerHTML` で設定すると、悪意のあるスクリプトが埋め込まれる**クロスサイトスクリプティング（XSS）**の脆弱性につながる可能性があります。安全のため、テキストを扱う場合は `textContent` を使うのが基本です。

## ✨ まとめ

- `querySelector` はCSSセレクタで要素を取得する
- `innerHTML` はHTMLタグを含めて内容を操作する
- `textContent` はテキストだけを安全に操作する
