# 8-2-4: Chapter 2 ハンズオン: useFetchフックを作成する

## 🎯 このハンズオンの目的

このハンズオンでは、データ取得のロジックをカプセル化した`useFetch`カスタムフックを作成します。ローディング状態、エラーハンドリング、データの取得を一つのフックにまとめることで、コンポーネントをシンプルに保つ方法を学びます。

## 準備

Chapter 1で作成したReactプロジェクトを使用するか、新しいプロジェクトを作成してください。

```bash
# 新しいプロジェクトを作成する場合
npx create-react-app custom-hooks-practice --template typescript
cd custom-hooks-practice
npm start
```

## Step 1: 基本的なuseFetchフックの作成

まず、シンプルな`useFetch`フックを作成します。

`src/hooks/useFetch.ts`ファイルを作成します。

```typescript
import { useState, useEffect } from 'react';

// フックの戻り値の型定義
interface UseFetchResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

export function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const json = await response.json() as T;
        setData(json);
      } catch (e) {
        setError(e instanceof Error ? e : new Error('Unknown error'));
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
}
```

## Step 2: useFetchフックを使ったコンポーネントの作成

作成したフックを使って、ユーザー一覧を表示するコンポーネントを作成します。

`src/components/UserList.tsx`を作成します。

```typescript
import { useFetch } from '../hooks/useFetch';

// APIから取得するユーザーの型
interface User {
  id: number;
  name: string;
  email: string;
  company: {
    name: string;
  };
}

export function UserList() {
  const { data, loading, error } = useFetch<User[]>(
    'https://jsonplaceholder.typicode.com/users'
  );

  if (loading) {
    return <div className="loading">読み込み中...</div>;
  }

  if (error) {
    return <div className="error">エラー: {error.message}</div>;
  }

  if (!data || data.length === 0) {
    return <div className="empty">ユーザーが見つかりません</div>;
  }

  return (
    <div className="user-list">
      <h2>ユーザー一覧</h2>
      <ul>
        {data.map((user) => (
          <li key={user.id}>
            <strong>{user.name}</strong>
            <p>Email: {user.email}</p>
            <p>Company: {user.company.name}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## Step 3: 再取得機能の追加

データを手動で再取得できる機能を追加します。

`src/hooks/useFetch.ts`を更新します。

```typescript
import { useState, useEffect, useCallback } from 'react';

interface UseFetchResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void; // 再取得関数を追加
}

export function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const json = await response.json() as T;
      setData(json);
    } catch (e) {
      setError(e instanceof Error ? e : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const refetch = useCallback(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch };
}
```

## Step 4: 再取得ボタンの追加

`src/components/UserList.tsx`に再取得ボタンを追加します。

```typescript
import { useFetch } from '../hooks/useFetch';

interface User {
  id: number;
  name: string;
  email: string;
  company: {
    name: string;
  };
}

export function UserList() {
  const { data, loading, error, refetch } = useFetch<User[]>(
    'https://jsonplaceholder.typicode.com/users'
  );

  return (
    <div className="user-list">
      <div className="header">
        <h2>ユーザー一覧</h2>
        <button onClick={refetch} disabled={loading}>
          {loading ? '読み込み中...' : '再取得'}
        </button>
      </div>

      {loading && <div className="loading">読み込み中...</div>}
      
      {error && <div className="error">エラー: {error.message}</div>}
      
      {!loading && !error && data && (
        <ul>
          {data.map((user) => (
            <li key={user.id}>
              <strong>{user.name}</strong>
              <p>Email: {user.email}</p>
              <p>Company: {user.company.name}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

## Step 5: App.tsxの更新

`src/App.tsx`を更新して、UserListコンポーネントを表示します。

```typescript
import { UserList } from './components/UserList';
import './App.css';

function App() {
  return (
    <div className="App">
      <h1>カスタムフック練習</h1>
      <UserList />
    </div>
  );
}

export default App;
```

## Step 6: スタイルの追加

`src/App.css`にスタイルを追加します。

```css
.App {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.user-list .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.user-list ul {
  list-style: none;
  padding: 0;
}

.user-list li {
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
}

.user-list li strong {
  font-size: 1.2em;
}

.user-list li p {
  margin: 5px 0;
  color: #666;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error {
  color: red;
  padding: 20px;
  background-color: #fee;
  border-radius: 8px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}
```

## ✨ まとめ

このハンズオンでは、以下のことを実践しました。

- ジェネリクスを使った型安全な`useFetch`フックの作成
- ローディング、エラー、データの3つの状態管理
- `useCallback`を使った再取得機能の実装
- カスタムフックを使ったコンポーネントの簡潔な実装

`useFetch`フックを使うことで、データ取得のロジックがコンポーネントから分離され、コードの再利用性と可読性が向上しました。実際のプロジェクトでは、TanStack Queryのようなライブラリを使うことが多いですが、カスタムフックの基本的な考え方を理解することは非常に重要です。

次のチャプターでは、React Hook FormやZodなど、実務でよく使うライブラリについて学んでいきましょう。
