# Tutorial 8: React応用

## Chapter 1: `useEffect`による副作用の管理

### Chapter 1 ハンズオン: APIからユーザー情報を取得する

🎯 **このハンズオンで達成すること**

-   コンポーネントのマウント時に、`useEffect`を使ってAPIからデータを取得する方法を習得する。
-   取得したデータをStateで管理し、UIに表示する流れを実装できるようになる。
-   ローディング中とエラー発生時のUIを条件付きレンダリングで表示できるようになる。
-   `useEffect`のクリーンアップ関数を使って、APIリクエストのキャンセル処理を実装し、Strict Modeの2回実行に正しく対応できるようになる。

--- 

🖼️ **完成イメージ**

コンポーネントが表示されると、「Loading...」と表示され、APIから取得したユーザー名が表示されます。IDを変更するボタンを押すと、再度APIリクエストが走り、別のユーザー名が表示されます。

![完成イメージ](https://placehold.jp/800x400.png?text=ユーザー情報%0A---%0AUser%20ID:%201%0A%0A...Loading...%0A%0A---%0A↓%0A---%0AUser%20ID:%201%0A%0A名前:%20Leanne%20Graham%0A%0A[次のユーザーへ])

--- 

### 🧠 先輩エンジニアの思考プロセス

「ユーザーIDを指定して、そのユーザー情報をAPIから取ってきて表示するコンポーネント作って」と言われたら、こう考える。

1.  **必要なStateは何か？:**
    -   取得したユーザー情報を保持するStateが必要だ。`user`という名前にしよう。初期値は`null`だな。
    -   API通信中であることを示すStateも必要だ。`loading`という`boolean`のStateにしよう。初期値は`true`だ。
    -   エラーが発生したことを示すStateも欲しい。`error`というStateで、エラーメッセージ（`string`）か`null`を保持するようにしよう。
    -   表示するユーザーIDを管理するStateも必要だ。`userId`という`number`のStateにしよう。初期値は`1`だ。
2.  **副作用（API通信）のタイミング:**
    -   API通信は副作用だから、`useEffect`の中で行う。
    -   実行タイミングは？
        -   まず、コンポーネントが最初に表示されたときに実行したい。
        -   そして、`userId` Stateが変更されたときにも再実行したい。
    -   ということは、`useEffect`の依存配列は`[userId]`にすれば完璧だ。
3.  **API通信処理の実装:**
    -   `useEffect`の中で`async/await`を使いたいが、`useEffect`の第一引数に直接`async`は付けられない（クリーンアップ関数を返せなくなるため）。なので、`useEffect`の内部で`async`関数を定義して、それを呼び出す形にしよう。
    -   `try...catch`ブロックでエラーハンドリングをしっかり行う。`loading` Stateの更新も忘れずに。通信開始時に`setLoading(true)`、終了時（成功・失敗問わず）に`setLoading(false)`を呼ぶ。
    -   今回はダミーAPIとして`JSONPlaceholder`を使おう。`https://jsonplaceholder.typicode.com/users/{userId}`というエンドポイントだ。
4.  **クリーンアップ処理の実装:**
    -   Strict Modeでの2回実行問題に対応するため、リクエストのキャンセル処理を入れるのがプロだ。
    -   `AbortController`を作成し、`fetch`の`signal`に渡す。
    -   `useEffect`のクリーンアップ関数で`controller.abort()`を呼び出す。これで、`userId`が素早く変更されたときや、コンポーネントがアンマウントされたときに、古いリクエストがキャンセルされる。
5.  **UIの条件付きレンダリング:**
    -   `loading`が`true`の間は、「Loading...」と表示する。
    -   `error`が存在する場合は、エラーメッセージを表示する。
    -   `user`が正常に取得できたら、ユーザー名を表示する。
    -   これらを三項演算子や`&&`を使って書けば、スッキリするな。

--- 

### 🏃 実践: Step by Stepで実装しよう

#### Step 1: コンポーネントの雛形作成

`src/components`に`UserInfo.tsx`というファイルを作成します。

```tsx
// src/components/UserInfo.tsx
import { useState, useEffect } from "react";

// APIから返ってくるユーザーデータの型
type User = {
  id: number;
  name: string;
  username: string;
  email: string;
};

function UserInfo() {
  // ここにStateとuseEffectを実装していく

  return (
    <div>
      <h2>ユーザー情報</h2>
      {/* ここにUIを実装していく */}
    </div>
  );
}

export default UserInfo;
```

そして、`src/App.tsx`でこのコンポーネントを呼び出します。

```tsx
// src/App.tsx
import UserInfo from "./components/UserInfo";

function App() {
  return <UserInfo />;
}

export default App;
```

#### Step 2: Stateの宣言

`UserInfo.tsx`に必要なStateを宣言します。

```tsx
// ...
function UserInfo() {
  const [userId, setUserId] = useState(1);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // ...
}
// ...
```

#### Step 3: `useEffect`でのAPI通信とクリーンアップの実装

`useEffect`を使って、`userId`が変更されたときにAPI通信を行うロジックを実装します。

```tsx
// ...
useEffect(() => {
  // AbortControllerでクリーンアップを実装
  const controller = new AbortController();

  const fetchUser = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `https://jsonplaceholder.typicode.com/users/${userId}`,
        { signal: controller.signal } // signalを渡す
      );

      if (!response.ok) {
        throw new Error("ユーザー情報の取得に失敗しました。");
      }

      const data = await response.json();
      setUser(data);
    } catch (err) {
      if (err.name === "AbortError") {
        console.log("Fetch aborted");
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  fetchUser();

  // クリーンアップ関数
  return () => {
    controller.abort();
  };
}, [userId]); // userIdに依存
// ...
```

#### Step 4: UIの条件付きレンダリング

取得したStateに基づいて、表示するUIを動的に変更します。

```tsx
// ...
function UserInfo() {
  // ... (StateとuseEffectの実装)

  const handleNextUser = () => {
    setUserId(id => id + 1);
  };

  return (
    <div>
      <h2>ユーザー情報</h2>
      <p>User ID: {userId}</p>

      {/* 条件付きレンダリング */}
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {user && (
        <div>
          <p><strong>名前:</strong> {user.name}</p>
          <p><strong>ユーザー名:</strong> {user.username}</p>
          <p><strong>Email:</strong> {user.email}</p>
        </div>
      )}

      <button onClick={handleNextUser} disabled={loading}>
        {loading ? "読み込み中..." : "次のユーザーへ"}
      </button>
    </div>
  );
}
// ...
```

これで完成です！ブラウザで動作を確認してみましょう。「次のユーザーへ」ボタンを素早く連続でクリックしても、コンソールに "Fetch aborted" と表示され、最後のIDのリクエストだけが正常に完了することが確認できるはずです。これがクリーンアップの力です。

--- 

✨ **まとめ**

-   `useEffect`の依存配列に`[userId]`を指定することで、`userId`の変更をトリガーに副作用を再実行できる。
-   `loading`や`error`といったStateを用意することで、API通信の状態に応じたUIをユーザーに提示できる。
-   `AbortController`を使い、`useEffect`のクリーンアップで`fetch`をキャンセルすることで、Strict Modeの2回実行や、不要になったリクエストの後始末を安全に行うことができる。
-   `try...catch...finally`ブロックを使うと、成功・失敗にかかわらず実行したい処理（例: `setLoading(false)`）を確実に記述できる。
