# 8-3-5: 実践 🚀 Chapter 3 ハンズオン: 高機能なフォームを作成する

## 🎯 このハンズオンの目的

このチャプターで学んだライブラリを総動員し、実務レベルの高機能なユーザー登録フォームを作成します。具体的には、以下の技術を統合します。

-   **フォーム管理**: `React Hook Form`
-   **バリデーション**: `Zod`
-   **サーバー状態管理 (データ送信)**: `TanStack Query`

このハンズオンを通して、モダンなReact開発におけるライブラリ活用のエコシステムを体感し、宣言的で堅牢なコンポーネントを構築するスキルを習得します。

## 事前準備

以下のライブラリをインストールしてください。

```bash
npm install react-hook-form @hookform/resolvers zod @tanstack/react-query axios
```

また、アプリケーションのルートが`QueryClientProvider`でラップされていることを確認してください。

```tsx
// main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import App from './App';

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>
);
```

## ハンズオン

### ステップ1: バリデーションスキーマと型の定義 (Zod)

まず、`Zod`を使ってフォームのバリデーションスキーマを定義します。ここでのポイントは、パスワードと確認用パスワードが一致するかを検証する相関バリデーションを`.refine()`を使って実装することです。

```typescript
// src/components/RegisterForm.tsx
import { z } from 'zod';

const RegisterSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'], // エラーメッセージをconfirmPasswordフィールドに関連付ける
});

// Zodスキーマから型を推論
type RegisterFormInput = z.infer<typeof RegisterSchema>;
```

### ステップ2: データ送信ロジックの定義 (TanStack Query)

次に、フォームのデータをサーバーに送信するためのロジックを`TanStack Query`の`useMutation`を使って定義します。今回はダミーのAPIエンドポイントとして`jsonplaceholder`を使用します。

```typescript
// src/api/userApi.ts
import axios from 'axios';
import { RegisterFormInput } from '../components/RegisterForm'; // 型をインポート

// 送信するデータからconfirmPasswordを除外する
export type UserCreationPayload = Omit<RegisterFormInput, 'confirmPassword'>;

export const createUser = async (userData: UserCreationPayload) => {
  const { data } = await axios.post('https://jsonplaceholder.typicode.com/users', userData);
  // 実際のAPIでは作成されたユーザー情報が返ってくる
  return data;
};
```

### ステップ3: フォームコンポーネントの実装 (React Hook Form)

最後に、これらを統合してフォームコンポーネントを構築します。

```tsx
// src/components/RegisterForm.tsx
import React from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation } from '@tanstack/react-query';
import { z } from 'zod';
import { createUser, UserCreationPayload } from '../api/userApi';

// (ステップ1で定義したスキーマと型)
const RegisterSchema = z.object({ ... });
type RegisterFormInput = z.infer<typeof RegisterSchema>;

export function RegisterForm() {
  // React Hook Formの設定
  const { 
    register, 
    handleSubmit, 
    formState: { errors, isSubmitting }, // isSubmittingを追加
    reset, // フォームをリセットする関数
  } = useForm<RegisterFormInput>({
    resolver: zodResolver(RegisterSchema),
  });

  // TanStack QueryのuseMutationの設定
  const mutation = useMutation({
    mutationFn: createUser,
    onSuccess: (data) => {
      console.log('User created successfully:', data);
      alert('User registration successful!');
      reset(); // 成功したらフォームをリセット
    },
    onError: (error) => {
      console.error('Failed to create user:', error);
      alert(`Error: ${error.message}`);
    },
  });

  // フォーム送信時の処理
  const onSubmit: SubmitHandler<RegisterFormInput> = (data) => {
    // confirmPasswordを除外してAPIに渡す
    const { confirmPassword, ...payload } = data;
    mutation.mutate(payload);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <h2>User Registration</h2>

      <div>
        <label htmlFor="username">Username</label>
        <input id="username" {...register('username')} />
        {errors.username && <p style={{ color: 'red' }}>{errors.username.message}</p>}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input id="email" type="email" {...register('email')} />
        {errors.email && <p style={{ color: 'red' }}>{errors.email.message}</p>}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input id="password" type="password" {...register('password')} />
        {errors.password && <p style={{ color: 'red' }}>{errors.password.message}</p>}
      </div>

      <div>
        <label htmlFor="confirmPassword">Confirm Password</label>
        <input id="confirmPassword" type="password" {...register('confirmPassword')} />
        {errors.confirmPassword && <p style={{ color: 'red' }}>{errors.confirmPassword.message}</p>}
      </div>

      {/* サーバーからのエラーを表示 */}
      {mutation.isError && (
        <p style={{ color: 'red' }}>{mutation.error.message}</p>
      )}

      <button type="submit" disabled={isSubmitting || mutation.isPending}>
        {isSubmitting || mutation.isPending ? 'Registering...' : 'Register'}
      </button>
    </form>
  );
}
```

#### コードのポイント

-   **責務の分離**: `Zod`がバリデーション、`React Hook Form`がUIの状態管理、`TanStack Query`がサーバーとの通信、というように、各ライブラリがそれぞれの責務を綺麗に分担しています。
-   **型安全性**: `Zod`から推論された`RegisterFormInput`型が、`useForm`, `SubmitHandler`, `createUser` APIの引数まで一気通貫で利用されており、型安全性が担保されています。
-   **送信状態の管理**: `useForm`の`isSubmitting`や`useMutation`の`isPending`を使って、フォーム送信中のボタンを無効化し、ユーザーにフィードバックを提供しています。
-   **エラーハンドリング**: バリデーションエラー（クライアントサイド）は`formState.errors`で、API通信エラー（サーバーサイド）は`mutation.isError`で、それぞれ適切にハンドリングしています。
-   **成功時の処理**: `useMutation`の`onSuccess`コールバック内でフォームを`reset()`することで、UXを向上させています。

## ✨ まとめ

このハンズオンでは、現代のReact開発における強力なライブラリ群を組み合わせることで、いかに効率的かつ堅牢なフォームを構築できるかを学びました。

-   バリデーションロジックは`Zod`スキーマに集約。
-   フォームのUI状態管理は`React Hook Form`に一任。
-   非同期なデータ送信とサーバー状態の管理は`TanStack Query`が担当。

この「三位一体」のパターンは、実務における多くのフォーム実装シーンで応用できる非常に強力なものです。それぞれのライブラリの役割を理解し、適切に組み合わせることで、開発者はボイラープレートコードから解放され、より本質的なアプリケーションの機能開発に集中することができます。
