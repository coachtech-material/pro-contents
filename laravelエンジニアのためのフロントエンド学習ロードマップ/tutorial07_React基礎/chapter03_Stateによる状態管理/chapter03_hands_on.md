# Tutorial 7: React基礎

## Chapter 3: Stateによる状態管理

### Chapter 3 ハンズオン: 簡単なTODOリストアプリの作成

🎯 **このハンズオンで達成すること**

-   `useState`を使って、インタラクティブなコンポーネントを作成できるようになる。
-   フォーム入力とStateを連携させる**制御コンポーネント**を実装できるようになる。
-   配列のStateを、**イミュータブル**に追加・削除・更新する方法を実践で習得する。
-   イベントハンドリング、条件付きレンダリング、リストレンダリング（`map`）といった、これまでに学んだ知識を総動員して、一つのアプリケーションを完成させる。

--- 

🖼️ **完成イメージ**

入力フォームにテキストを入れて「追加」ボタンを押すと、TODOリストに項目が追加されます。各TODO項目の「削除」ボタンを押すと、その項目がリストから削除されます。

![完成イメージ](https://placehold.jp/800x600.png?text=TODOリスト%0A%0A[____テキスト入力欄____] [追加]%0A%0A・Reactを学ぶ [削除]%0A・寝る [削除]%0A・買い物に行く [削除])

--- 

### 🧠 先輩エンジニアの思考プロセス

「簡単なTODOアプリ作って」と言われたら、こう考える。

1.  **コンポーネント設計:** まずはUIを部品に分解する。
    -   アプリケーション全体を管理する`TodoApp`コンポーネントが必要だな。
    -   TODOを入力するフォーム部分は`TodoForm`コンポーネントとして切り出せそうだ。
    -   TODOの一覧を表示する部分は`TodoList`コンポーネントにしよう。
    -   `TodoList`の中の各項目は、`TodoItem`コンポーネントとして独立させると、削除ボタンのロジックをカプセル化できて綺麗になりそうだ。
2.  **Stateの置き場所:** 次に、アプリケーションの状態（データ）は何か、そしてそれはどこに置くべきか考える。
    -   このアプリの最も重要なデータは「TODOのリスト（配列）」だ。このリストは`TodoForm`（追加のため）と`TodoList`（表示・削除のため）の両方からアクセスする必要がある。ということは、これらの親である`TodoApp`コンポーネントにStateとして置くのが正解だ（**リフティング・ステート・アップ**）。
    -   入力フォームの現在のテキストもStateで管理する必要がある。これは`TodoForm`コンポーネント内だけで完結するから、`TodoForm`自身のStateとして持てばいい。
3.  **データフロー（Propsの設計）:** Stateを親に置いたので、子にどうやって情報を渡すか、子からどうやって親のStateを変更してもらうか決める。
    -   `TodoApp` → `TodoList`: TODOリストの配列 (`todos`) をPropsで渡す。
    -   `TodoApp` → `TodoForm`: TODOを追加する関数 (`addTodo`) をPropsで渡す。
    -   `TodoApp` → `TodoList` → `TodoItem`: TODOを削除する関数 (`deleteTodo`) と、個々のTODOの情報 (`todo`) をPropsで渡す。
4.  **実装（ボトムアップ）:** 小さな部品から作っていくのが確実だ。
    -   `TodoItem.tsx`: `todo`と`onDelete`をPropsで受け取り、TODOのテキストと削除ボタンを表示する。ボタンが押されたら`onDelete(todo.id)`を呼ぶ。
    -   `TodoList.tsx`: `todos`と`onDelete`をPropsで受け取り、`todos.map()`で各TODOを`TodoItem`コンポーネントに変換してリスト表示する。
    -   `TodoForm.tsx`: `onAdd`をPropsで受け取る。入力テキスト用の`text` Stateを持つ。フォームが送信されたら、`onAdd(text)`を呼び出し、`text` Stateを空にする。
    -   `TodoApp.tsx`: `todos` Stateと、`addTodo`, `deleteTodo`関数を定義する。そして、`TodoForm`と`TodoList`を配置し、必要なPropsを渡す。これで完成だ。

--- 

### 🏃 実践: Step by StepでTODOアプリを作ろう

#### Step 1: ファイルの準備

`src/components`ディレクトリに、以下の4つのファイルを新規作成します。

-   `TodoApp.tsx` (アプリケーション全体)
-   `TodoForm.tsx` (入力フォーム)
-   `TodoList.tsx` (TODOリスト)
-   `TodoItem.tsx` (TODOリストの各項目)

そして、`src/App.tsx`の中身を、`TodoApp`コンポーネントを呼び出すだけのシンプルなものに書き換えます。

```tsx
// src/App.tsx
import TodoApp from "./components/TodoApp";

function App() {
  return <TodoApp />;
}

export default App;
```

#### Step 2: `TodoItem`コンポーネントの実装

まずは一番小さい部品から作ります。

```tsx
// src/components/TodoItem.tsx

// このコンポーネントが受け取るPropsの型
type TodoItemProps = {
  todo: { id: number; text: string };
  onDelete: (id: number) => void; // idを受け取り何も返さない関数の型
};

function TodoItem({ todo, onDelete }: TodoItemProps) {
  return (
    <li>
      {todo.text}
      {/* ボタンクリックで、親から渡されたonDelete関数を呼び出す */}
      <button onClick={() => onDelete(todo.id)} style={{ marginLeft: 8 }}>
        削除
      </button>
    </li>
  );
}

export default TodoItem;
```

#### Step 3: `TodoList`コンポーネントの実装

次に、`TodoItem`をリスト表示するコンポーネントです。

```tsx
// src/components/TodoList.tsx
import TodoItem from "./TodoItem";

// このコンポーネントが受け取るPropsの型
type TodoListProps = {
  todos: { id: number; text: string }[]; // TODOオブジェクトの配列
  onDelete: (id: number) => void;
};

function TodoList({ todos, onDelete }: TodoListProps) {
  return (
    <ul>
      {/* 配列をmapでループ処理し、各要素をTodoItemコンポーネントに変換 */}
      {todos.map((todo) => (
        // リストレンダリングでは、各要素に一意な`key` propsを渡す必要がある
        <TodoItem key={todo.id} todo={todo} onDelete={onDelete} />
      ))}
    </ul>
  );
}

export default TodoList;
```

-   **`key={todo.id}`**: Reactがリストの各項目を効率的に識別・更新するために、配列を`map`でレンダリングする際には、各要素にユニークな`key`というPropsを渡す必要があります。通常は、データが持つIDを使います。

#### Step 4: `TodoForm`コンポーネントの実装

TODOを追加するためのフォームです。制御コンポーネントのパターンを使います。

```tsx
// src/components/TodoForm.tsx
import { useState } from "react";

type TodoFormProps = {
  onAdd: (text: string) => void;
};

function TodoForm({ onAdd }: TodoFormProps) {
  // フォームの入力値を管理するState
  const [text, setText] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault(); // フォーム送信によるページリロードを防ぐ
    if (!text.trim()) return; // 空文字の場合は何もしない

    onAdd(text); // 親から渡されたonAdd関数を呼び出す
    setText(""); // 入力フォームを空にする
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        type="text" 
        value={text} 
        onChange={(e) => setText(e.target.value)} 
      />
      <button type="submit">追加</button>
    </form>
  );
}

export default TodoForm;
```

#### Step 5: `TodoApp`コンポーネントで全体を組み立てる

最後に、すべての部品をまとめ、Stateとロジックを実装します。

```tsx
// src/components/TodoApp.tsx
import { useState } from "react";
import TodoList from "./TodoList";
import TodoForm from "./TodoForm";

// TODOの型を定義しておくと便利
type Todo = { id: number; text: string };

function TodoApp() {
  // アプリケーションのメインState
  const [todos, setTodos] = useState<Todo[]>([
    { id: 1, text: "Reactを学ぶ" },
    { id: 2, text: "寝る" },
  ]);

  // TODOを追加する関数
  const addTodo = (text: string) => {
    const newTodo = { id: Date.now(), text };
    // イミュータブルに追加
    setTodos([...todos, newTodo]);
  };

  // TODOを削除する関数
  const deleteTodo = (id: number) => {
    // イミュータブルに削除
    setTodos(todos.filter((todo) => todo.id !== id));
  };

  return (
    <div>
      <h1>TODOリスト</h1>
      {/* State更新用の関数をPropsとして渡す */}
      <TodoForm onAdd={addTodo} />
      <TodoList todos={todos} onDelete={deleteTodo} />
    </div>
  );
}

export default TodoApp;
```

-   **`useState<Todo[]>`**: `useState`にジェネリクスで型を渡すことで、`todos`が`Todo`の配列であることを明示できます。

これでTODOアプリの完成です！ブラウザで動作を確認してみましょう。

--- 

✨ **まとめ**

-   複数のコンポーネントで共有されるStateは、それらの最も近い共通の親に配置する（**リフティング・ステート・アップ**）。
-   親は、Stateの値をPropsとして子に渡し、Stateを更新する関数もPropsとして子に渡す。
-   子は、受け取った関数をイベントハンドラ内で呼び出すことで、親のStateを間接的に更新する。
-   配列を`map`でレンダリングする際は、パフォーマンスのためにユニークな`key` Propsを渡す必要がある。
-   配列のStateの追加・削除は、スプレッド構文や`filter`メソッドを使ってイミュータブルに行う。
