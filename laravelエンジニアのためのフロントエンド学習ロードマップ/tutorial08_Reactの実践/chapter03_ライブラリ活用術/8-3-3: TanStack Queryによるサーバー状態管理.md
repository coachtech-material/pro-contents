# 8-3-3: TanStack Queryによるサーバー状態管理

## 🎯 このセクションで学ぶこと

-   クライアント状態とサーバー状態の違いを理解する
-   `useEffect` を使ったデータフェッチの課題（キャッシュ、再フェッチなど）を認識する
-   `TanStack Query`（旧 `React Query`）が解決する課題と、その強力な機能を学ぶ
-   `useQuery` を使ってサーバーからデータを取得し、キャッシュする方法を習得する
-   `useMutation` を使ってサーバー上のデータを更新（作成、更新、削除）する方法を学ぶ

## 導入

これまで、`useState` や `useReducer` を使ってコンポーネントの状態を管理してきました。これらは**クライアント状態（Client State）**と呼ばれ、UIの開閉状態やフォームの入力値など、フロントエンドアプリケーション内で完結する状態を指します。

しかし、現代のWebアプリケーションの多くは、APIサーバーから取得したデータを扱います。このデータは、**サーバー状態（Server State）**と呼ばれ、クライアント状態とは根本的に異なる特性を持っています。

-   **所有権がない**: データはサーバー上にあり、フロントエンドはそれを「借りて」表示しているにすぎない。
-   **非同期性**: データの取得には時間がかかる。
-   **陳腐化**: 他のユーザーやバックグラウンドプロセスによって、データはいつでも変更される可能性がある。

`useEffect` と `useState` を使ってサーバー状態を管理しようとすると、ローディング/エラー状態の管理、キャッシュ、データの再フェッチ、バックグラウンド更新など、考慮すべきことが非常に多く、コードはすぐに複雑化してしまいます。

この複雑な「サーバー状態管理」を、宣言的かつ効率的に行うためのライブラリが **`TanStack Query`** です。`TanStack Query` は、データフェッチを驚くほどシンプルにし、キャッシュ、再検証、楽観的更新といった高度な機能を簡単に実装できるようにしてくれます。

## 詳細解説

### 🔑 TanStack Queryの基本

`TanStack Query` を使うには、まずアプリケーションのルートを `QueryClientProvider` でラップし、`QueryClient` のインスタンスを渡します。

```bash
npm install @tanstack/react-query
```

```tsx
// main.tsx or App.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import App from './App';

// QueryClientのインスタンスを作成
const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>
);
```

### `useQuery`: データの取得

サーバーからデータを取得（`GET`リクエスト）するには `useQuery` フックを使います。`useQuery` は、データフェッチに関するあらゆる状態（`data`, `isLoading`, `isError`など）を返してくれます。

```tsx
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

interface Todo {
  id: number;
  title: string;
  completed: boolean;
}

// データをフェッチする非同期関数
const fetchTodos = async (): Promise<Todo[]> => {
  const { data } = await axios.get('https://jsonplaceholder.typicode.com/todos');
  return data;
};

function TodoList() {
  const { data, error, isLoading } = useQuery({
    queryKey: ['todos'], // ① クエリキー
    queryFn: fetchTodos,  // ② クエリ関数
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>An error has occurred: {error.message}</div>;

  return (
    <ul>
      {data?.map(todo => (
        <li key={todo.id}>{todo.title}</li>
      ))}
    </ul>
  );
}
```

#### コードのポイント

1.  **`queryKey`**: クエリ（APIリクエスト）を一意に識別するためのキーです。配列で指定し、このキーに基づいて`TanStack Query`はデータをキャッシュします。例えば、特定のTODOを取得する場合は `['todos', todoId]` のようにします。
2.  **`queryFn`**: データを実際にフェッチする非同期関数を指定します。この関数はPromiseを返す必要があります。

`useQuery` を使うだけで、`useEffect` で自前実装した場合に比べて以下のメリットがあります。

-   **自動キャッシュ**: 一度取得したデータは `queryKey` に紐づけてキャッシュされ、同じキーで再度 `useQuery` が呼ばれた場合、キャッシュから即座にデータが返されます。
-   **自動再フェッチ**: ウィンドウがフォーカスされた時、ネットワークが再接続した時などに、データが古い（stale）と判断されれば自動的に再フェッチが走ります。
-   **ローディング/エラー状態の管理**: `isLoading`, `isError`, `error` といった状態を自動で管理してくれます。

### `useMutation`: データの更新

データの作成（`POST`）、更新（`PUT`/`PATCH`）、削除（`DELETE`）といった、サーバーの状態を変更する操作には `useMutation` フックを使います。

```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';

// 新しいTODOを作成する非同期関数
const createTodo = async (newTodo: { title: string }): Promise<Todo> => {
  const { data } = await axios.post('https://jsonplaceholder.typicode.com/todos', newTodo);
  return data;
};

function AddTodoForm() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: createTodo, // ① ミューテーション関数
    onSuccess: () => {      // ② 成功時のコールバック
      // 'todos'クエリを無効化し、再フェッチをトリガーする
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });

  const handleAddTodo = () => {
    mutation.mutate({ title: 'New Todo' }); // ③ ミューテーションの実行
  };

  return (
    <div>
      <button onClick={handleAddTodo} disabled={mutation.isPending}>
        {mutation.isPending ? 'Adding...' : 'Add Todo'}
      </button>
      {mutation.isError && <div>Error: {mutation.error.message}</div>}
    </div>
  );
}
```

#### コードのポイント

1.  **`mutationFn`**: サーバーの状態を変更する非同期関数を指定します。
2.  **`onSuccess`**: ミューテーションが成功した後に実行されるコールバックです。ここで `queryClient.invalidateQueries` を呼び出すのが重要なパターンです。これにより、`TanStack Query` は指定された `queryKey`（この場合は `['todos']`）を持つクエリが古くなったと判断し、関連するコンポーネントがアクティブになったときに自動で再フェッチを行います。結果として、TODOリストが最新の状態に更新されます。
3.  **`mutation.mutate()`**: この関数を呼び出すことで、実際にミューテーションを実行します。引数には `mutationFn` に渡すデータを指定します。

## ✨ まとめ

-   サーバーから取得するデータ（**サーバー状態**）は、UIの状態（**クライアント状態**）とは異なり、キャッシュや再検証といった複雑な管理が必要である。
-   `TanStack Query` は、このサーバー状態管理を専門に扱うライブラリで、データフェッチのコードを劇的に簡素化し、多くのベストプラクティスを自動で提供してくれる。
-   データの取得には **`useQuery`** を使い、`queryKey` でキャッシュを管理する。
-   データの作成・更新・削除には **`useMutation`** を使い、成功時に `queryClient.invalidateQueries` を呼び出して関連データを再フェッチするのが定石パターン。
-   `TanStack Query` を導入することで、開発者は複雑な非同期処理のボイラープレートコードから解放され、アプリケーションのコアロジックに集中できる。
