# 4-3-4: 実践 🚀 チャプターハンズオン: ToDoリストを作成する

## 🎯 このハンズオンの目的

- これまで学んだDOM操作の知識を総動員して、簡単なToDoリストアプリケーションを作成する
- ユーザーの入力に応じて動的にページを更新する処理を実装する

## 課題

以下の仕様を満たすToDoリストを作成してください。

### HTML

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>ToDo List</title>
</head>
<body>
  <h1>ToDo List</h1>
  <input type="text" id="todo-input" placeholder="新しいToDoを入力">
  <button id="add-button">追加</button>
  <ul id="todo-list"></ul>

  <script src="app.js"></script>
</body>
</html>
```

### JavaScript (`app.js`)

1. 必要なDOM要素（input, button, ul）を取得する
2. 「追加」ボタンがクリックされたら、以下の処理を行うイベントリスナーを登録する
   a. inputに入力されたテキストを取得する
   b. 新しい `<li>` 要素を作成する
   c. `<li>` 要素のテキストを a で取得したテキストに設定する
   d. `<ul>` 要素の子要素として `<li>` を追加する
   e. inputの中身を空にする

## 💻 解答例

```javascript
// app.js

// 1. DOM要素の取得
const todoInput = document.querySelector("#todo-input");
const addButton = document.querySelector("#add-button");
const todoList = document.querySelector("#todo-list");

// 2. イベントリスナーの登録
addButton.addEventListener("click", function() {
  // a. テキストの取得
  const todoText = todoInput.value;

  // 入力が空の場合は何もしない
  if (todoText === "") return;

  // b. li要素の作成
  const newTodoItem = document.createElement("li");

  // c. テキストの設定
  newTodoItem.textContent = todoText;

  // d. li要素の追加
  todoList.appendChild(newTodoItem);

  // e. inputを空にする
  todoInput.value = "";
});
```
