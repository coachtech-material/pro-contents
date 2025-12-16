# 4-3-3: イベントリスナーの追加（addEventListener）

## 🎯 このセクションで学ぶこと

- `addEventListener` を使って、ユーザーのアクション（クリックなど）を検知できるようになる
- イベントオブジェクトから詳細な情報を取得できるようになる

## 導入

インタラクティブなWebページを作成するには、ユーザーの操作（イベント）に応じて処理を実行する必要があります。`addEventListener` メソッドを使うと、特定の要素で発生したイベントを監視し、対応する処理（イベントリスナー）を登録できます。

## 詳細解説

### `addEventListener` の基本構文

```javascript
const myButton = document.querySelector("#my-button");

function handleClick() {
  alert("ボタンがクリックされました！");
}

// ボタンがクリックされたらhandleClick関数を実行
myButton.addEventListener("click", handleClick);
```

`addEventListener` は、第一引数にイベントの種類（`"click"`, `"mouseover"`など）、第二引数に実行する関数を指定します。

### イベントオブジェクト

イベントリスナーとして登録された関数には、**イベントオブジェクト**が引数として渡されます。イベントオブジェクトには、発生したイベントに関する詳細な情報が含まれています。

```javascript
const input = document.querySelector("#my-input");

input.addEventListener("input", function(event) {
  // event.target はイベントが発生した要素（この場合はinput要素）
  // event.target.value はその要素の現在の値
  console.log("入力内容:", event.target.value);
});
```

## 💡 TIP

- `addEventListener` を使うと、1つのイベントに対して複数のイベントリスナーを登録できます。

## ✨ まとめ

- `addEventListener` でイベントを監視し、処理を登録する
- イベントリスナーにはイベントオブジェクトが渡され、詳細な情報を取得できる
