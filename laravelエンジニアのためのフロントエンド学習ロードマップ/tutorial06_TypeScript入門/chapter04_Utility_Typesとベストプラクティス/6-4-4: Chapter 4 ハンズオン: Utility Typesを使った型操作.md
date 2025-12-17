# 6-4-4: 実践 🚀 チャプターハンズオン: Utility Typesを使った型操作

## 🎯 課題

このチャプターで学んだUtility Typesを駆使して、Todoアプリケーションで必要となる様々な型を、一つの基本となる型から効率的に作成してみましょう。

DRY（Don't Repeat Yourself）の原則に従い、型の定義を再利用することの重要性を体感することが目的です。

### 基準となる型

すべての課題は、以下の`Todo`インターフェースを元にして作成します。

```typescript
interface Todo {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  createdAt: Date;
}
```

### 完成要件

1.  **`Pick<T, K>` を使った型定義**
    -   Todoの一覧表示用に、`id`, `title`, `completed` のみを持つ `TodoPreview` 型を作成してください。

2.  **`Omit<T, K>` を使った型定義**
    -   新しいTodoを作成する際のAPIペイロードとして、`id` と `createdAt`（サーバー側で自動生成される）を除外した `TodoCreation` 型を作成してください。

3.  **`Partial<T>` を使った型定義**
    -   Todoを更新する際には、任意のプロパティ（`title`, `description`, `completed`）を更新できるものとします。`id`と`createdAt`は更新対象外です。この更新用ペイロードを表す `TodoUpdate` 型を作成してください。（ヒント: `Omit` と `Partial` を組み合わせます）

4.  **`Record<K, T>` を使った型定義**
    -   Todoを完了済み（`'done'`）と未完了（`'pending'`）にグループ分けして保持するオブジェクトの型 `GroupedTodos` を作成してください。キーは `'done'` または `'pending'` で、値は `TodoPreview` の配列 (`TodoPreview[]`) とします。

## 🛠️ 手順

1.  まず、基準となる `Todo` インターフェースをコードに記述します。
2.  `Pick` を使って `TodoPreview` 型を定義します。
3.  `Omit` を使って `TodoCreation` 型を定義します。
4.  `Omit` と `Partial` を組み合わせて `TodoUpdate` 型を定義します。
5.  `Record` を使って `GroupedTodos` 型を定義します。
6.  それぞれの型が正しく定義できているか、ダミーの変数に型注釈を付けて確認してみましょう。

## 🏆 解答例

```typescript
// 基準となるTodoインターフェース
interface Todo {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  createdAt: Date;
}

// 1. `Pick` を使って一覧表示用の型を作成
type TodoPreview = Pick<Todo, 'id' | 'title' | 'completed'>;

// 動作確認
const todoPreview: TodoPreview = {
  id: 1,
  title: 'TypeScriptを学ぶ',
  completed: false,
  // description: 'Utility Typesは便利' // エラー: Object literal may only specify known properties
};
console.log('TodoPreview:', todoPreview);


// 2. `Omit` を使って新規作成用の型を作成
type TodoCreation = Omit<Todo, 'id' | 'createdAt'>;

// 動作確認
const newTodo: TodoCreation = {
  title: 'ハンズオンを完了する',
  description: 'Utility Typesの課題を解く',
  completed: false,
  // id: 2 // エラー: 'id' は TodoCreation 型に存在しない
};
console.log('\nTodoCreation:', newTodo);


// 3. `Partial` と `Omit` を組み合わせて更新用の型を作成
type TodoUpdate = Partial<Omit<Todo, 'id' | 'createdAt'>>;

// 動作確認
const updatePayload: TodoUpdate = {
  description: 'より詳細な説明を追記',
  completed: true,
};
console.log('\nTodoUpdate:', updatePayload);


// 4. `Record` を使ってグループ化されたTodoの型を作成
type TodoStatus = 'done' | 'pending';
type GroupedTodos = Record<TodoStatus, TodoPreview[]>;

// 動作確認
const groupedTodos: GroupedTodos = {
  done: [
    { id: 2, title: 'Reactの学習', completed: true },
  ],
  pending: [
    { id: 1, title: 'TypeScriptを学ぶ', completed: false },
    { id: 3, title: 'GitHubにプッシュする', completed: false },
  ],
  // in_progress: [] // エラー: 'in_progress' は TodoStatus 型にない
};
console.log('\nGroupedTodos:', groupedTodos);

/*
--- 期待される出力 ---

TodoPreview: { id: 1, title: 'TypeScriptを学ぶ', completed: false }

TodoCreation: { title: 'ハンズオンを完了する', description: 'Utility Typesの課題を解く', completed: false }

TodoUpdate: { description: 'より詳細な説明を追記', completed: true }

GroupedTodos: {
  done: [ { id: 2, title: 'Reactの学習', completed: true } ],
  pending: [
    { id: 1, title: 'TypeScriptを学ぶ', completed: false },
    { id: 3, title: 'GitHubにプッシュする', completed: false }
  ]
}

*/
```

### 💡 コードのポイント

このハンズオンの最大のポイントは、`Todo` という**単一の信頼できる情報源（Single Source of Truth）**から、アプリケーションの様々な場面で必要とされる型を、重複なく効率的に生成している点です。

もし将来、`Todo` インターフェースに `dueDate: Date` というプロパティが追加されたとしても、`TodoCreation` や `TodoUpdate` の型定義は自動的に `dueDate` を含むようになり、手動で修正する必要はありません。これがUtility Typesを使う大きなメリットであり、メンテナンス性の高いコードに繋がります。
