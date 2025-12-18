# 7-2-2: children_props

## Chapter 2: Propsによるデータ受け渡し

### Section 2: `children` Propsによるコンテンツの埋め込み

🎯 **このセクションで学ぶこと**

-   特別なPropsである `children` の役割を理解する。
-   コンポーネントの開始タグと終了タグの間に書かれたコンテンツが、`children` Propsとして渡される仕組みを習得する。
-   `children` Propsを活用して、再利用性の高い汎用的なコンポーネント（`Card`, `Modal`など）を作成する方法を学ぶ。

--- 

### イントロダクション：コンポーネントの「中身」を渡したい

前のセクションでは、コンポーネントに属性のような形でデータを渡す方法を学びました。しかし、もし渡したいデータが、単純な文字列や数値ではなく、**他のJSX要素やコンポーネント**だったらどうでしょうか？

例えば、様々なコンテンツを囲むことができる、汎用的な「カード」コンポーネントを作りたいとします。

```jsx
<Card>
  {/* ここにプロフィール情報を入れたい */}
</Card>

<Card>
  {/* ここに記事の要約を入れたい */}
</Card>
```

このように、コンポーネントの開始タグと終了タグの間にコンテンツを「埋め込む」ことを可能にするのが、特別なPropsである **`children`** です。

--- 

### ⚙️ `children` Propsの使い方

コンポーネントを呼び出す際に、`<MyComponent>...</MyComponent>`のように開始タグと終了タグで囲むと、その間に書かれたすべてのものが、`children`という名前のPropsとして子コンポーネントに渡されます。

**例：汎用的な`Card`コンポーネント**

**1. 子コンポーネント (`Card.tsx`)**

`Card`コンポーネントは、渡された`children`を、自身の`div`要素の中に表示するだけです。

```tsx
// Card.tsx

import React from "react"; // ReactNode型のためにインポート

// 1. Propsの型を定義する
type CardProps = {
  // childrenの型は React.ReactNode を使うのが一般的
  children: React.ReactNode;
};

// 2. propsからchildrenを受け取り、表示したい場所に配置する
function Card({ children }: CardProps) {
  return (
    <div className="card">
      {children}
    </div>
  );
}

export default Card;
```

-   **`React.ReactNode`**: `children` Propsの型注釈には、`React.ReactNode`を使うのが最も安全で一般的です。これは、JSX要素、文字列、数値、`null`、`undefined`など、Reactがレンダリングできるすべてのものを含む包括的な型です。

**2. 親コンポーネント (`App.tsx`)**

親コンポーネントは、`Card`コンポーネントの「中身」として、好きなJSXを渡すことができます。

```tsx
// App.tsx
import Card from "./components/Card";
import UserProfile from "./components/UserProfile";

function App() {
  return (
    <>
      {/* UserProfileコンポーネントをCardの中身として渡す */}
      <Card>
        <UserProfile name="山田 太郎" hobby="プログラミング" />
      </Card>

      {/* 別のコンテンツをCardの中身として渡す */}
      <Card>
        <h2>お知らせ</h2>
        <p>新しいチュートリアルが公開されました！</p>
      </Card>
    </>
  );
}
```

-   `<Card>...</Card>`で囲まれた部分（`UserProfile`コンポーネントや、`h2`と`p`タグ）が、`Card`コンポーネントの`children` Propsとして渡されます。
-   `Card`コンポーネントは、受け取った`children`をそのままレンダリングするため、結果として、`UserProfile`や「お知らせ」が、カードのスタイルが適用された`div`の中に表示されます。

--- 

### 🚀 `children` Propsの活用例

`children` Propsは、特定のレイアウトやスタイルを提供しつつ、その中身は自由に差し替え可能にしたい、という**ラッパーコンポーネント**を作成する際に非常に強力です。

#### 例1：モーダルダイアログ (`Modal`)

```jsx
<Modal title="確認">
  <p>本当に削除しますか？</p>
  <button>はい</button>
  <button>いいえ</button>
</Modal>
```

`Modal`コンポーネントは、モーダルの背景や閉じるボタンといった共通のUIを提供し、`title` Propsでタイトルを受け取り、`children` Propsでモーダルの本文を受け取ります。

#### 例2：認証付きページ (`AuthenticatedPage`)

```jsx
<AuthenticatedPage>
  <Dashboard />
</AuthenticatedPage>
```

`AuthenticatedPage`コンポーネントは、まずユーザーがログインしているかどうかをチェックします。ログインしていれば、渡された`children`（この場合は`Dashboard`コンポーネント）を表示し、ログインしていなければログインページにリダイレクトする、といったロジックを共通化できます。

このように、`children` Propsを使いこなすことで、コンポーネントの再利用性が格段に向上し、アプリケーションの構造をよりクリーンに保つことができます。

--- 

✨ **まとめ**

-   `children`は、コンポーネントの開始タグと終了タグの間に記述されたコンテンツを受け取るための、特別なPropsである。
-   `children` Propsの型には、`React.ReactNode`を使用するのが一般的。
-   `children` Propsを使うことで、中身を自由に差し替えられる、汎用的な**ラッパーコンポーネント**（`Card`, `Modal`など）を簡単に作成できる。
-   これにより、レイアウトや共通ロジックをカプセル化しつつ、高い再利用性を実現できる。

📝 **学習のポイント**

-   [ ] `children` Propsは、HTMLのどの概念に似ていますか？
-   [ ] `<Card content={<UserProfile />} />` のように、`children`以外の名前（例: `content`）でコンポーネントを渡す方法と、`<Card><UserProfile /></Card>` のように`children`を使う方法では、どちらがより直感的で読みやすいと感じますか？また、それはなぜですか？
-   [ ] 「利用規約」のような長い文章を表示するための、スクロール可能なボックスコンポーネント`ScrollableBox`を考えてみましょう。このコンポーネントは、`children` Propsをどのように利用するでしょうか？
