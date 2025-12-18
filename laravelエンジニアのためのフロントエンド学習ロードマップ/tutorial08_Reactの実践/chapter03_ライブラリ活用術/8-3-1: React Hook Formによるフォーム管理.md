# 8-3-1: React Hook Formによるフォーム管理

## 🎯 このセクションで学ぶこと

- Reactにおけるフォーム管理の複雑さと、フォームライブラリの必要性を理解する
- `React Hook Form` の基本的な使い方（`useForm`, `register`, `handleSubmit`）を習得する
- Controlled Componentsとの違いを理解し、`React Hook Form` がパフォーマンスに優れる理由を学ぶ
- フォームの状態（`formState`）を監視し、エラーメッセージなどを表示する方法を学ぶ

## 導入

Reactの基本的なフォーム管理方法として「Controlled Components」を学びました。これは`useState`を使って入力値を管理する直感的な方法ですが、フォームが複雑になるにつれていくつかの課題が顕在化します。

-   **パフォーマンスの問題**: 一文字入力するたびにコンポーネントが再レンダリングされるため、大規模なフォームではパフォーマンスが低下する可能性がある。
-   **ボイラープレートコードの増加**: フォーム項目が増えるたびに、`useState`、`onChange`ハンドラ、`value`属性のセットが増えていき、コードが冗長になりがち。
-   **複雑なバリデーション**: 必須入力、文字数制限、メール形式など、複雑なバリデーションロジックを自前で実装するのは大変。

これらの課題を解決するために、Reactのエコシステムには多くの優れたフォーム管理ライブラリが存在します。その中でも、現在最も人気があり、デファクトスタンダードとされいるのが **`React Hook Form`** です。

`React Hook Form` は、パフォーマンス、柔軟性、そしてDX（開発者体験）に重点を置いて設計されており、シンプルかつ高機能なフォームを驚くほど簡単に構築できます。

## 詳細解説

### 🔑 React Hook Formの基本コンセプト

`React Hook Form` の最大の特徴は、**非制御コンポーネント（Uncontrolled Components）**のアプローチをベースにしている点です。Controlled Componentsが入力のたびにReactのStateを更新するのに対し、`React Hook Form` はフォーム要素への**参照（ref）**を使って入力を追跡します。これにより、ユーザーの入力中は不要な再レンダリングが発生せず、パフォーマンスが大幅に向上します。

### `useForm`フック

`React Hook Form` を使うには、まず `useForm` フックを呼び出します。このフックが、フォームの状態管理やバリデーションに必要なメソッドと状態を提供してくれます。

```bash
npm install react-hook-form
```

```tsx
import { useForm, SubmitHandler } from "react-hook-form";

// フォームのデータ型を定義
interface IFormInput {
  firstName: string;
  lastName: string;
  age: number;
}

function MyForm() {
  const { 
    register, 
    handleSubmit, 
    formState: { errors } 
  } = useForm<IFormInput>();

  // ...
}
```

`useForm` から分割代入で取り出す主要なものは以下の通りです。

-   **`register`**: フォームの入力要素を`React Hook Form`に「登録」するためのメソッド。このメソッドの戻り値を、`<input>`などの`props`として展開します。
-   **`handleSubmit`**: フォームの送信をハンドルする高階関数。自作の送信処理関数を引数として渡します。`handleSubmit`は、フォームのバリデーションを自動的に実行し、バリデーションが通った場合のみ、引数で渡された関数を呼び出します。
-   **`formState`**: フォームの状態（エラー、入力済みか、送信中かなど）を保持するオブジェクト。`formState.errors` には、バリデーションエラーの情報が格納されます。

### 実装例

```tsx
import React from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';

interface IFormInput {
  firstName: string;
  lastName: string;
  age: number;
}

function App() {
  const { 
    register, 
    handleSubmit, 
    formState: { errors } 
  } = useForm<IFormInput>();

  // バリデーションが成功した時に実行される関数
  const onSubmit: SubmitHandler<IFormInput> = data => {
    console.log(data);
    alert(`Hello, ${data.firstName} ${data.lastName}!`);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* 1. `register`で入力要素を登録 */}
      {/* 2. バリデーションルールを第2引数に指定 */}
      <div>
        <label>First Name</label>
        <input {...register("firstName", { required: true, maxLength: 20 })} />
        {/* 3. エラーがあればメッセージを表示 */}
        {errors.firstName && <p style={{ color: 'red' }}>First name is required.</p>}
      </div>

      <div>
        <label>Last Name</label>
        <input {...register("lastName", { pattern: /^[A-Za-z]+$/i })} />
        {errors.lastName && <p style={{ color: 'red' }}>Last name must be alphabet.</p>}
      </div>

      <div>
        <label>Age</label>
        <input type="number" {...register("age", { min: 18, max: 99 })} />
        {errors.age && <p style={{ color: 'red' }}>Age must be between 18 and 99.</p>}
      </div>

      <button type="submit">Submit</button>
    </form>
  );
}

export default App;
```

#### コードのポイント

1.  **`register("firstName", { ... })`**: 第一引数にフィールド名を指定し、入力要素を登録します。第二引数には、`required`（必須）、`maxLength`（最大長）、`pattern`（正規表現）、`min`/`max`（最小/最大値）などのバリデーションルールをオブジェクトで渡せます。
2.  **`{...register(...) }`**: `register`メソッドは、`onChange`, `onBlur`, `name`, `ref` といった、入力要素に必要な`props`をまとめて返します。これをスプレッド構文で展開することで、手動で`onChange`などを書く必要がなくなります。
3.  **`errors.firstName`**: `register`の第一引数で指定したフィールド名に対応するエラーオブジェクトが`formState.errors`に格納されます。エラーがあればこのオブジェクトが存在するので、条件付きレンダリングでエラーメッセージを表示できます。
4.  **`handleSubmit(onSubmit)`**: `form`の`onSubmit`には、`handleSubmit`でラップした自作の送信関数を渡します。これにより、送信ボタンが押されたときに、まずバリデーションが走り、成功した場合にのみ`onSubmit`関数がフォームのデータ（`data`）を引数に呼び出されます。

## ✨ まとめ

-   `React Hook Form` は、パフォーマンスと開発者体験に優れた、Reactのデファクトスタンダードなフォーム管理ライブラリである。
-   非制御コンポーネントのアプローチを採用しており、入力中の不要な再レンダリングを抑制する。
-   `useForm`フックから得られる **`register`**, **`handleSubmit`**, **`formState`** を使うのが基本。
-   `register`メソッドで入力要素を登録し、バリデーションルールを宣言的に記述できる。
-   `handleSubmit`が高階関数としてバリデーションと送信処理をラップしてくれるため、ボイラープレートコードを大幅に削減できる。
-   次のセクションで学ぶ`Zod`などのバリデーションライブラリと組み合わせることで、さらに強力で型安全なフォームを構築できる。
