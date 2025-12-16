# Tutorial 7: React基礎

## Chapter 3: Stateによる状態管理

### Section 2: Stateの更新とイベントハンドリング

🎯 **このセクションで学ぶこと**

-   `onClick`や`onChange`といった、JSXでの**イベントハンドリング**の方法を習得する。
-   フォーム入力要素（`input`など）の値をStateで管理する、**制御コンポーネント**というパターンを理解する。
-   Stateの更新が非同期である問題に対応するため、セッター関数に**更新関数**を渡す方法を習得する。

--- 

### イントロダクション：ユーザーの操作をStateに反映する

`useState`でStateを宣言する方法は学びましたが、それをいつ、どのように更新するのでしょうか？ State更新のきっかけのほとんどは、ユーザーによる**イベント**です。

-   ボタンのクリック (`click`)
-   フォームへの入力 (`change`)
-   フォームの送信 (`submit`)
-   マウスカーソルのホバー (`mouseover`)

このセクションでは、これらのイベントをReactで処理する方法（イベントハンドリング）と、それを使ってStateを安全かつ正確に更新するテクニックを学びます。

--- 

### ⚙️ JSXでのイベントハンドリング

JSXでイベントを処理するには、HTML要素に`camelCase`形式のイベントハンドラ属性（例: `onClick`, `onChange`）を渡します。属性値には、イベント発生時に実行したい**関数**を波括弧`{}`で囲んで指定します。

**❌ やってはいけないこと（関数を呼び出してしまう）:**
```jsx
// ページが表示された瞬間にhandleClickが実行されてしまう！
<button onClick={handleClick()}>Click me</button>
```

**⭕ 正しい方法（関数そのものを渡す）:**
```jsx
<button onClick={handleClick}>Click me</button>
```

または、アロー関数を使ってインラインで定義することもできます。

```jsx
<button onClick={() => alert("Clicked!")}>Click me</button>
```

#### イベントオブジェクト

イベントハンドラ関数は、第一引数に**イベントオブジェクト**を受け取ることができます。これには、イベントに関する詳細な情報（どのキーが押されたか、マウスの座標はどこか、など）が含まれています。

特にフォーム要素で重要なのが、`event.target.value`です。これは、イベントが発生した要素（例: `input`タグ）の現在の値を取得するために使われます。

--- 

### 🚀 フォーム入力と制御コンポーネント

HTMLの`input`や`textarea`は、それ自身が内部に状態（ユーザーが入力した値）を持っています。しかし、Reactでは、この状態もReactの**State**で一元管理するのがベストプラクティスです。このパターンのことを**制御コンポーネント (Controlled Component)** と呼びます。

**制御コンポーネントの実装ステップ:**
1.  入力値を保持するためのStateを`useState`で宣言する。
2.  `input`要素の`value`属性に、そのState変数をバインドする。
3.  `input`要素の`onChange`イベントを捕捉し、イベントハンドラを定義する。
4.  イベントハンドラ内で、`event.target.value`を使って入力値を取得し、セッター関数でStateを更新する。

**例：名前入力フォーム**

```tsx
// NameForm.tsx
import { useState } from "react";

function NameForm() {
  // 1. 入力値を保持するState
  const [name, setName] = useState("");

  // 3. onChangeイベントハンドラ
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    // 4. 入力値でStateを更新
    setName(event.target.value);
  };

  return (
    <div>
      <input 
        type="text" 
        // 2. value属性にStateをバインド
        value={name} 
        onChange={handleChange} 
      />
      <p>あなたの名前は: {name}</p>
    </div>
  );
}
```

-   **`React.ChangeEvent<HTMLInputElement>`**: `onChange`イベントオブジェクトの型です。ジェネリクスで、イベントの発生源が`HTMLInputElement`であることを明記しています。

**なぜ制御コンポーネントを使うのか？**
-   **単一の信頼できる情報源 (Single Source of Truth):** 入力値が常にReactのStateに保持されるため、データがどこにあるかが明確になります。
-   **動的な操作:** Stateを更新するだけで、入力値をプログラム側から変更したり（例: クリアボタン）、バリデーションをかけたりすることが容易になります。

--- 

### 🔒 安全なState更新：更新関数を使う

前のセクションで、「Stateの更新は非同期である」と学びました。これにより、前のStateの値に依存する更新処理が、意図通りに動かないことがあります。

**❌ 問題が起こる例：カウンターを一度に2回インクリメントしたい**
```tsx
const handleDoubleIncrement = () => {
  setCount(count + 1); // この時点ではまだcountは古い値
  setCount(count + 1); // ここでも同じ古い値を使ってしまう
};
// 結果：1しか増えない
```

この問題を解決するには、セッター関数に新しい値を直接渡すのではなく、**「現在のStateを受け取り、新しいStateを返す関数」（更新関数）**を渡します。

**⭕ 正しい方法：更新関数を渡す**

```tsx
const handleDoubleIncrement = () => {
  // (prevCount) => prevCount + 1 という関数を渡す
  setCount((prevCount) => prevCount + 1);
  setCount((prevCount) => prevCount + 1);
};
// 結果：期待通り2増える
```

-   `prevCount`という引数には、Reactが保証する**最新のStateの値**が渡されます。
-   Reactはこれらの更新関数をキューに入れ、順番に実行するため、前の更新結果が次の更新に正しく反映されます。

**ルール:** **前のStateの値に基づいて次のStateを計算する場合は、必ず更新関数形式を使いましょう。**

--- 

✨ **まとめ**

-   JSXのイベントハンドリングは、`onClick={handleClick}`のように、`camelCase`の属性に関数を渡すことで行う。
-   フォーム要素の値をReactのStateで管理する手法を**制御コンポーネント**と呼び、React開発の基本パターンである。
-   制御コンポーネントは、`value`をStateにバインドし、`onChange`でStateを更新することで実装する。
-   Stateの更新は非同期であるため、前のStateの値に依存する更新処理を行う場合は、`setState(prev => prev + 1)`のように**更新関数**を渡すのが安全である。

📝 **学習のポイント**

-   [ ] `onClick={handleClick()}`と`onClick={handleClick}`の違いを、もう一度自分の言葉で説明してください。
-   [ ] 制御コンポーネントではない、昔ながらのフォーム（非制御コンポーネント）では、入力された値を取得するためにどのような方法が使われていたか調べてみましょう。（ヒント: `ref`）
-   [ ] チェックボックス（`<input type="checkbox">`）を制御コンポーネントにする場合、`value`属性の代わりにどの属性をStateにバインドし、`event.target`からどのプロパティを取得する必要があるでしょうか？
