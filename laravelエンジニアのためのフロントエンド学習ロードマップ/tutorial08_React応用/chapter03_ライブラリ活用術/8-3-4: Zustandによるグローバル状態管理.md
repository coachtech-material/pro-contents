# 8-3-4: Zustandによるグローバル状態管理

## 🎯 このセクションで学ぶこと

- グローバル状態管理の必要性と、Context APIの課題を理解する
- `Zustand`の基本的な考え方と、そのシンプルさ、パフォーマンスの利点を学ぶ
- `create` APIを使って、状態（State）とアクション（Action）を持つストアを作成する方法を習得する
- 作成したストアをReactコンポーネントで利用する方法を学ぶ
- ストア内で非同期処理を扱う方法を理解する

## 導入

Reactアプリケーションでは、コンポーネント間で状態を共有するために「Propsをバケツリレーする」方法や、「状態を親コンポーネントにリフトアップする」方法を学びました。しかし、アプリケーションが大規模になり、多くのコンポーネントが同じ状態を必要とする場合、これらの方法は非常に煩雑になります。

この問題を解決するReactの組み込み機能が**Context API**です。Contextは、コンポーネントツリーの深い階層にあるコンポーネントにも、Propsを介さずに状態を直接渡すことができます。

しかし、Context APIにも課題があります。特に、Contextの値が更新されると、そのContextを購読しているすべてのコンポーネントが**無条件に再レンダリング**されてしまうというパフォーマンス上の問題です。大規模なアプリケーションでは、これが原因で不要な再レンダリングが多発し、パフォーマンスのボトルネックになることがあります。

この「Contextの再レンダリング問題」を解決しつつ、よりシンプルで直感的なAPIを提供するグローバル状態管理ライブラリが **`Zustand`** です。

`Zustand`（ズースタンド、ドイツ語で「状態」の意味）は、Reduxのような複雑なボイラープレートコードを必要とせず、フックベースの非常にシンプルなAPIで強力な状態管理を実現します。Fluxアーキテクチャに影響を受けており、状態の更新が予測可能であるという特徴も持っています。

## 詳細解説

### 🔑 Zustandの基本コンセプト

`Zustand`の核心は、`create`という一つの関数です。この関数を使って、状態（State）と、その状態を更新するための関数（Action）をまとめた「**ストア**」を作成します。このストアはReactコンポーネントの外に存在するただのオブジェクトであり、Reactに依存しません。

そして、作成されたストアは自動的にフックを返します。コンポーネントはそのフックを使うだけで、ストアの状態にアクセスしたり、アクションを呼び出したりできます。

### `create` APIによるストアの作成

カウンターを管理するシンプルなストアを作成してみましょう。

```bash
npm install zustand
```

```typescript
// src/store/counterStore.ts
import { create } from 'zustand';

// ストアの型を定義
interface CounterState {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
}

// create関数でストアを作成
export const useCounterStore = create<CounterState>((set) => ({
  // ① 初期状態 (State)
  count: 0,
  
  // ② 状態を更新する関数 (Action)
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));
```

#### コードのポイント

1.  **初期状態**: `create`のコールバック関数は、ストアの初期状態をオブジェクトとして返します。`count: 0`が初期状態です。
2.  **アクション**: `increment`や`decrement`のような、状態を更新するためのメソッドを定義します。これらのメソッド内で`set`関数を呼び出すことで、状態を更新します。
3.  **`set`関数**: `set`関数は、`Zustand`から提供される、ストアの状態を安全に更新するための関数です。`setState`のように、現在の状態（`state`）を受け取って新しい状態を返す関数を渡すことで、イミュータブルな更新を簡単に行えます。

これだけで、グローバルにアクセス可能な`useCounterStore`フックが完成しました。`Provider`でコンポーネントをラップする必要は一切ありません。

### ストアの利用

作成したストアをコンポーネントで使うのは非常に簡単です。

```tsx
// src/components/Counter.tsx
import { useCounterStore } from '../store/counterStore';

function Counter() {
  // ストアから必要なstateとactionを取得
  const { count, increment, decrement } = useCounterStore();

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>Increment</button>
      <button onClick={decrement}>Decrement</button>
    </div>
  );
}
```

`useCounterStore()`を呼び出すだけで、ストアのすべての状態とアクションにアクセスできます。

#### パフォーマンスの最適化

`Zustand`の真価は、状態の一部だけを購読できる点にあります。これにより、不要な再レンダリングを避けることができます。

```tsx
// このコンポーネントは`count`が変更された時だけ再レンダリングされる
function CountDisplay() {
  const count = useCounterStore((state) => state.count);
  return <p>Count: {count}</p>;
}

// このコンポーネントは`reset`アクションしか使わないので、`count`が変更されても再レンダリングされない！
function ResetButton() {
  const reset = useCounterStore((state) => state.reset);
  return <button onClick={reset}>Reset</button>;
}
```

`useCounterStore`の引数にセレクター関数（`state => state.count`）を渡すことで、その値が変更されたときにのみコンポーネントが再レンダリングされるようになります。これは、Context APIにはない`Zustand`の大きな利点です。

### 非同期アクション

`Zustand`では、非同期処理も簡単に扱えます。アクション内で`async/await`を使うだけです。

```typescript
// src/store/todoStore.ts
import { create } from 'zustand';

interface Todo {
  id: number;
  title: string;
}

interface TodoState {
  todos: Todo[];
  fetchTodos: () => Promise<void>;
}

export const useTodoStore = create<TodoState>((set) => ({
  todos: [],
  fetchTodos: async () => {
    const response = await fetch('https://api.example.com/todos');
    const data = await response.json();
    set({ todos: data });
  },
}));
```

## ✨ まとめ

-   `Zustand`は、Context APIの再レンダリング問題を解決し、ボイラープレートコードを最小限に抑えた、シンプルで強力なグローバル状態管理ライブラリである。
-   `create`関数一つで、状態（State）とアクション（Action）を持つ「ストア」を簡単に作成できる。
-   `Provider`でラップする必要がなく、作成されたフックをコンポーネントで呼び出すだけで、どこからでも状態にアクセスできる。
-   セレクター関数を使うことで、状態の一部だけを購読し、不要な再レンダリングを抑制するパフォーマンス最適化が容易に行える。
-   `TanStack Query`が**サーバー状態**管理のデファクトスタンダードである一方、`Zustand`は**クライアント状態**のグローバル管理において、非常に有力な選択肢である。
