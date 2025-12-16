# Tutorial 7: React基礎

## Chapter 2: Propsによるデータ受け渡し

### Chapter 2 ハンズオン: Propsを使ってコンポーネントを動的にする

🎯 **このハンズオンで達成すること**

-   Chapter 1で作成した`UserProfile`コンポーネントを、Propsを受け取れるようにリファクタリングする。
-   `children` Propsを活用した汎用的な`Card`コンポーネントを作成し、レイアウトの共通化を体験する。
-   Propsの型定義（`type`）、分割代入、オプショナルなProps（`?`）、デフォルト値を実践で使えるようになる。

--- 

🖼️ **完成イメージ**

汎用的な`Card`コンポーネントを作成し、その中にPropsで動的に内容が変わる`UserProfile`コンポーネントを配置します。一部のユーザーには追加情報（`bio`）も表示します。

![完成イメージ](https://placehold.jp/800x500.png?text=Card%20Component%0A---%0A名前:%20山田%20太郎%0A趣味:%20プログラミング%0A自己紹介:%20Reactを勉強中です！%0A---%0A%0ACard%20Component%0A---%0A名前:%20鈴木%20花子%0A趣味:%20読書%0A---)

--- 

### 🧠 先輩エンジニアの思考プロセス

「Chapter 1で作った自己紹介ページを、Propsを使って動的にしてみて」と言われたら、こう考える。

1.  **`UserProfile`のリファクタリング:** 今の`UserProfile`は名前と趣味がハードコードされている。これを外から渡せるようにするのが最初の仕事だ。
    -   `UserProfile.tsx`を開いて、まずはPropsの型`UserProfileProps`を定義しよう。`name`と`hobby`は必須（`string`）だな。自己紹介文`bio`は、いる人といない人がいそうだから、オプショナル（`bio?: string`）にしておこう。
    -   コンポーネントの引数を`({ name, hobby, bio }: UserProfileProps)`のように分割代入で受け取る。`bio`は存在する場合のみ`p`タグを表示するように、`{bio && <p>自己紹介: {bio}</p>}`という条件付きレンダリングを使うのがスマートだ。
2.  **`Card`コンポーネントの作成:** プロフィールを囲んでいる枠線スタイルは、他の場所でも使えそうだ。これを`Card`コンポーネントとして切り出そう。
    -   `components/Card.tsx`を作成する。このコンポーネントの役割は、渡された中身（`children`）を特定のスタイルを持つ`div`で囲むことだけだ。
    -   Propsの型は`{ children: React.ReactNode }`。受け取った`children`を`div`の中にそのままレンダリングする。
3.  **`App`コンポーネントの修正:** 親コンポーネントで、新しい`UserProfile`と`Card`を組み立てる。
    -   `App.tsx`を開く。まず、`Card`コンポーネントをインポートする。
    -   既存の`<UserProfile />`を`<Card><UserProfile ... /></Card>`の形で囲む。
    -   `UserProfile`コンポーネントに、`name`, `hobby`, `bio`の各Propsを渡していく。一人には`bio`を渡し、もう一人には渡さない、というパターンを試して、オプショナルPropsの動作を確認しよう。
4.  **スタイルの移動:** `UserProfile`に直接適用していたスタイル（`user-profile`クラス）は、`Card`コンポーネントの責務になった。`index.css`のクラス名を`.card`に変更し、`UserProfile.tsx`からは`className`の記述を削除する。これで責務の分離が完了だ。

--- 

### 🏃 実践: Step by Stepでリファクタリングしよう

（Chapter 1のハンズオンが完了している状態からスタートします）

#### Step 1: `UserProfile`コンポーネントをProps対応にする

`src/components/UserProfile.tsx`を以下のように書き換えます。

```tsx
// src/components/UserProfile.tsx

// 1. Propsの型を定義
type UserProfileProps = {
  name: string;
  hobby: string;
  // bioは任意（オプショナル）
  bio?: string;
};

// 2. 分割代入でPropsを受け取る
function UserProfile({ name, hobby, bio }: UserProfileProps) {
  return (
    // classNameは後で削除する
    <div className="user-profile">
      {/* ハードコードされていた部分をPropsに置き換え */}
      <p>名前: {name}</p>
      <p>趣味: {hobby}</p>

      {/* 3. bioが存在する場合のみ、自己紹介を表示（条件付きレンダリング） */}
      {bio && <p>自己紹介: {bio}</p>}

      <hr />
    </div>
  );
}

export default UserProfile;
```

-   **`{bio && <p>...</p>}`**: これはReactでよく使われる**条件付きレンダリング**のテクニックです。`bio`が`undefined`や空文字列でない（truthyな）場合にのみ、`&&`の右側のJSXがレンダリングされます。

#### Step 2: 汎用的な`Card`コンポーネントを作成する

`src/components`ディレクトリに`Card.tsx`を新規作成します。

```tsx
// src/components/Card.tsx

import React from "react";

// childrenを受け取るための型定義
type CardProps = {
  children: React.ReactNode;
};

function Card({ children }: CardProps) {
  // user-profileからcardにクラス名を変更
  return <div className="card">{children}</div>;
}

export default Card;
```

#### Step 3: `App.tsx`で新しいコンポーネントを組み立てる

`src/App.tsx`を編集し、`Card`コンポーネントを使って`UserProfile`をラップします。また、`UserProfile`にPropsを渡します。

```tsx
// src/App.tsx

import WelcomeMessage from "./components/WelcomeMessage";
import UserProfile from "./components/UserProfile";
// Cardコンポーネントをインポート
import Card from "./components/Card";

function App() {
  return (
    <>
      <WelcomeMessage />

      {/* CardコンポーネントでUserProfileをラップ */}
      <Card>
        <UserProfile 
          name="山田 太郎" 
          hobby="プログラミング" 
          bio="Reactを勉強中です！"
        />
      </Card>

      <Card>
        <UserProfile 
          name="鈴木 花子" 
          hobby="読書" 
        />
      </Card>
    </>
  );
}

export default App;
```

#### Step 4: スタイルの整理

最後に、スタイルの責務を`UserProfile`から`Card`に移します。

1.  `src/index.css`のクラス名を`.user-profile`から`.card`に変更します。
    ```css
    /* src/index.css */
    .card {
      border: 1px solid #ccc;
      padding: 16px;
      margin-top: 16px;
      border-radius: 8px;
    }
    ```
2.  `src/components/UserProfile.tsx`から`className="user-profile"`の記述を削除します。
    ```tsx
    // src/components/UserProfile.tsx
    // ...
    // classNameを削除
    <div>
      {/* ... */}
    </div>
    // ...
    ```

これでリファクタリングは完了です！ブラウザで確認すると、山田さんのプロフィールには自己紹介が表示され、鈴木さんのプロフィールには表示されていないことが確認できます。

--- 

✨ **まとめ**

-   ハードコードされた値をPropsに置き換えることで、コンポーネントは動的で再利用可能な部品になった。
-   Propsの型定義で`?`を使うことで、必須ではないオプショナルなPropsを安全に扱うことができる。
-   `children` Propsを使うことで、コンポーネントのレイアウトとコンテンツを分離し、`Card`のような汎用的なラッパーコンポーネントを作成できる。
-   コンポーネントの責務を明確にし、スタイルなどの関心事を適切なコンポーネントに移動させることで、コードの見通しが良くなった。

📝 **学習のポイント**

-   [ ] `UserProfile`コンポーネントに、`age?: number`というオプショナルなPropsを追加し、渡された場合のみ「年齢: {age}歳」と表示するように改修してみましょう。
-   [ ] `App.tsx`で、`Card`コンポーネントの中に`UserProfile`ではなく、自由なテキストや`h2`タグなどを入れてみて、`Card`が汎用的に使えることを確認してみましょう。
-   [ ] もし`UserProfile`の`bio`にデフォルト値を設定したい場合、どこをどのように変更すればよいでしょうか？（例: `bio = 'よろしくお願いします。'`）
