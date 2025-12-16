# Tutorial 7: React基礎

## Chapter 3: Stateによる状態管理

### Section 1: Stateと`useState`フック

🎯 **このセクションで学ぶこと**

-   コンポーネントが持つ「記憶」である **State** の概念を理解する。
-   PropsとStateの役割の違い（外部から渡される vs 内部で管理する）を説明できるようになる。
-   Reactの **フック (Hook)** の概念と、最も基本的なフックである **`useState`** の使い方を習得する。

--- 

### イントロダクション：インタラクティブなUIへ

Propsを使うことで、コンポーネントは静的なデータを表示できるようになりました。しかし、Webアプリケーションには、ユーザーの操作によって変化する要素が不可欠です。例えば、

-   クリックすると数が増えるカウンター
-   入力すると文字が反映されるテキストフィールド
-   「いいね！」ボタンを押すと色が変わる

このような「時間と共に変化するデータ」をコンポーネントに記憶させ、UIに反映させるための仕組みが **State** です。

Propsが「親から渡される、変更不可能な設定値」だとすれば、Stateは「**コンポーネント自身が内部で管理する、変更可能なデータ（記憶）**」と言うことができます。

--- 

### ⚙️ フック (Hook) とは？

Stateを関数コンポーネントで利用するためには、Reactが提供する特別な関数である **フック (Hook)** を使います。

フックは、関数コンポーネントに、Stateの保持やライフサイクル（後述）といったReactの機能を「引っ掛ける (hook into)」ための仕組みです。フックは、必ず`use`というプレフィックスで始まります（例: `useState`, `useEffect`）。

このセクションでは、最も基本的で重要なフックである **`useState`** を学びます。

--- 

### 🚀 `useState` の使い方

`useState`は、コンポーネントにState（状態）を追加するためのフックです。

`useState`を呼び出すと、**State変数**と、そのStateを更新するための**セッター関数**のペアが、配列として返ってきます。

**`useState`の基本構文:**

```tsx
import { useState } from 'react';

function MyComponent() {
  // useStateを呼び出し、配列の分割代入で変数とセッター関数を受け取る
  const [stateVariable, setFunction] = useState(initialValue);

  // ...
}
```

-   **`initialValue`**: Stateの初期値。コンポーネントが最初にレンダリングされるときに一度だけ使われます。
-   **`stateVariable`**: 現在のStateの値を保持する変数。この変数の値が変更されると、Reactはコンポーネントを再レンダリングします。
-   **`setFunction`**: Stateを更新するための関数。**Stateを直接変更することはできず、必ずこのセッター関数を使って更新します。**

**例：シンプルなカウンターコンポーネント**

```tsx
// Counter.tsx
import { useState } from 'react';

function Counter() {
  // 1. useStateを呼び出し、countというState変数を宣言
  //    初期値は 0
  const [count, setCount] = useState(0);

  // 2. ボタンがクリックされたときに呼ばれる関数
  const increment = () => {
    // 3. セッター関数を呼び出して、countの値を更新する
    setCount(count + 1);
  };

  return (
    <div>
      <p>現在のカウント: {count}</p>
      <button onClick={increment}>カウントアップ</button>
    </div>
  );
}
```

**動作の流れ:**
1.  コンポーネントが最初に表示されるとき、`useState(0)`が呼ばれ、`count`は`0`になる。画面には「現在のカウント: 0」と表示される。
2.  ユーザーがボタンをクリックすると、`increment`関数が実行される。
3.  `setCount(count + 1)`が呼ばれる。現在の`count`は`0`なので、`setCount(1)`が実行される。
4.  **`setCount`が呼ばれると、Reactは`count`というStateが変更されたことを検知し、`Counter`コンポーネントの再レンダリングをスケジュールする。**
5.  `Counter`コンポーネントが再実行（再レンダリング）される。このとき、`useState(0)`は2回目以降は無視され、`count`変数は更新された値である`1`を持つ。
6.  画面には「現在のカウント: 1」と表示される。

--- 

### 🔒 State更新の重要なルール

#### 1. Stateを直接変更しない

State変数は読み取り専用のように扱ってください。直接代入しても、Reactは変更を検知できず、再レンダリングは発生しません。

**❌ やってはいけないこと:**
```tsx
const increment = () => {
  count = count + 1; // ダメ！再レンダリングされない
};
```

**⭕ 正しい方法:**
```tsx
const increment = () => {
  setCount(count + 1); // 必ずセッター関数を使う
};
```

#### 2. Stateの更新は非同期

セッター関数（例: `setCount`）を呼び出しても、State変数が**即座に**更新されるわけではありません。Reactは、パフォーマンスのために複数のState更新をまとめてバッチ処理することがあります。

```tsx
const handleClick = () => {
  setCount(count + 1); // countの更新をスケジュール
  console.log(count);  // まだ古い値(0)が表示される！

  setCount(count + 1); // これも count + 1 をスケジュール
  console.log(count);  // やはり古い値(0)が表示される！
};
```

この場合、最終的に`count`は`1`にしかなりません。前のStateの値に基づいて更新を行いたい場合は、**更新関数**をセッターに渡す必要があります。（これは次のセクションで詳しく学びます）

--- 

### ⚙️ 複数のState変数を持つ

一つのコンポーネントは、複数のState変数を好きなだけ持つことができます。関連性の低いデータは、別々のStateとして管理するのが良い設計です。

```tsx
function UserForm() {
  const [name, setName] = useState('');
  const [age, setAge] = useState(20);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // ...
}
```

--- 

✨ **まとめ**

-   **State**は、コンポーネントが内部で保持・管理する、時間と共に変化するデータ（記憶）である。
-   **フック (Hook)** は、関数コンポーネントにReactの機能を追加するための特別な関数で、`use`で始まる。
-   **`useState`** フックは、コンポーネントにStateを追加する。`[state, setState]`のペアを返す。
-   Stateの更新は、必ず**セッター関数 (`setState`)** を使って行う。直接代入しても再レンダリングは起こらない。
-   セッター関数を呼ぶと、Reactはそのコンポーネントの**再レンダリング**をスケジュールする。
-   Stateの更新は非同期的に行われる。

📝 **学習のポイント**

-   [ ] PropsとStateの最も大きな違いは何ですか？それぞれの役割を、演劇に例えて説明してみてください。（Props: 脚本、State: 役者の感情など）
-   [ ] なぜStateを直接変更してはいけないのでしょうか？ Reactが変更を検知できなくなる理由を考えてみましょう。
-   [ ] `useState`が返す配列を、`const stateArray = useState(0); const count = stateArray[0]; const setCount = stateArray[1];` のように分割代入を使わずに書いた場合、コードはどうなりますか？ 分割代入の利便性を再確認しましょう。
