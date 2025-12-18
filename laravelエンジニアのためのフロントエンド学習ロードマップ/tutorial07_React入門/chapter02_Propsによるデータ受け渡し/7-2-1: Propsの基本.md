# 7-2-1: Propsの基本

## Chapter 2: Propsによるデータ受け渡し

### Section 1: Propsの基本と型定義

🎯 **このセクションで学ぶこと**

-   **Props** を使って、親コンポーネントから子コンポーネントへデータを渡す方法を習得する。
-   TypeScriptを使い、コンポーネントが受け取るPropsに**型を定義**する方法を習得する。
-   Propsが**読み取り専用**であるという重要なルールを理解する。

--- 

### イントロダクション：コンポーネントをカスタマイズ可能にする

前のChapterで、コンポーネントを再利用する方法を学びました。しかし、`UserProfile`コンポーネントを何度再利用しても、表示されるのはいつも「山田 太郎」さんでした。これでは再利用性が高いとは言えません。

コンポーネントを真に再利用可能にするには、呼び出し元（親コンポーネント）から、表示したいデータ（名前や趣味など）を動的に渡せるようにする必要があります。この「親から子へのデータの受け渡し」を実現する仕組みが **Props** (プロパティ) です。

Propsは、**関数における引数**のようなものだと考えることができます。コンポーネントに引数（Props）を渡すことで、その振る舞いや表示内容をカスタマイズできるのです。

--- 

### ⚙️ Propsを渡す・受け取る

Propsの受け渡しは、2つのステップで行われます。

1.  **親コンポーネント:** 子コンポーネントを呼び出す際に、HTMLの属性のような構文でデータを渡す。
2.  **子コンポーネント:** 関数の引数として、渡されたデータがひとまとめになったオブジェクトを受け取る。

**例：`UserProfile`コンポーネントに`name`と`hobby`を渡す**

**1. 親コンポーネント (`App.tsx`)**

```tsx
// App.tsx
import UserProfile from "./components/UserProfile";

function App() {
  return (
    <>
      {/* 属性のような構文でPropsを渡す */}
      <UserProfile name="山田 太郎" hobby="プログラミング" />
      <UserProfile name="鈴木 花子" hobby="読書" />
    </>
  );
}
```

-   `<UserProfile ... />` の中で、`name="..."` や `hobby="..."` のように、属性を渡すのと同じ要領でPropsを指定します。

**2. 子コンポーネント (`UserProfile.tsx`)**

```tsx
// UserProfile.tsx

// 関数の第一引数としてpropsオブジェクトを受け取る
function UserProfile(props) {
  return (
    <div className="user-profile">
      {/* propsオブジェクトのプロパティとしてデータにアクセス */}
      <p>名前: {props.name}</p>
      <p>趣味: {props.hobby}</p>
      <hr />
    </div>
  );
}
```

-   子コンポーネントは、その第一引数に、親から渡されたすべてのデータが格納された**`props`オブジェクト**を受け取ります。
-   `props.name`や`props.hobby`のように、ドット記法で各データにアクセスできます。

--- 

### 🚀 TypeScriptによるPropsの型定義

上記のコードは動作しますが、TypeScriptの観点からは不完全です。`props`オブジェクトがどのようなプロパティを持つべきか、型が定義されていないためです。

コンポーネントが受け取るPropsの型は、`type`エイリアスまたは`interface`を使って定義するのが一般的です。

```tsx
// UserProfile.tsx

// 1. Propsの型を定義する
type UserProfileProps = {
  name: string;
  hobby: string;
};

// 2. 引数に型注釈を付け、分割代入で受け取る
function UserProfile({ name, hobby }: UserProfileProps) {
  return (
    <div className="user-profile">
      <p>名前: {name}</p>
      <p>趣味: {hobby}</p>
      <hr />
    </div>
  );
}

export default UserProfile;
```

**解説:**
1.  `type UserProfileProps = { ... }` で、`UserProfile`コンポーネントが`string`型の`name`と`hobby`という2つのPropsを受け取ることを定義します。コンポーネント名の後ろに`Props`を付けるのが一般的な命名規則です。
2.  `function UserProfile({ name, hobby }: UserProfileProps)` の部分がポイントです。
    -   `{ name, hobby }`: これはJavaScriptの**分割代入 (Destructuring assignment)** という機能です。`props.name`や`props.hobby`と書く代わりに、`props`オブジェクトから`name`と`hobby`プロパティを直接取り出して、同名の変数として使えるようにします。コードがスッキリして読みやすくなるため、React開発では頻繁に使われます。
    -   `: UserProfileProps`: 分割代入で受け取るオブジェクトが、先ほど定義した`UserProfileProps`型に準拠していることをTypeScriptに伝えます。

このように型を定義することで、`App.tsx`側でPropsを渡し忘れたり、間違った型のデータを渡そうとしたりすると、コンパイルエラーとして即座に検知できるようになります。

**❌ 間違った呼び出しの例:**
```tsx
// App.tsx

// コンパイルエラー: プロパティ 'hobby' がありません。
<UserProfile name="佐藤 健" />

// コンパイルエラー: 型 'number' を型 'string' に割り当てることはできません。
<UserProfile name="高橋 恵子" hobby={30} />
```

--- 

### 🔒 Propsは読み取り専用

Propsに関して、一つだけ非常に重要なルールがあります。それは、**「コンポーネントは、受け取った自身のPropsを決して変更してはならない」**というルールです。

Propsは親から子への一方通行のデータです。子コンポーネントが受け取ったPropsを勝手に書き換えてしまうと、データの流れが混乱し、アプリケーションの挙動が予測不能になってしまいます。

**❌ やってはいけないこと:**
```tsx
function UserProfile({ name, hobby }: UserProfileProps) {
  // エラー！ Propsは読み取り専用です。
  name = "別の名前"; 

  return (...);
}
```

Reactでは、このような思想を「純粋関数」という言葉で説明することがあります。同じPropsが与えられれば、必ず同じJSXを返す、副作用のない関数のようにコンポーネントを扱うべき、ということです。

コンポーネント内で時間経過やユーザーの操作によって変化する値を扱いたい場合は、次のChapterで学ぶ**State**という別の仕組みを使います。

--- 

✨ **まとめ**

-   **Props**は、親コンポーネントから子コンポーネントへデータを渡すための仕組みである。
-   親はHTMLの属性のように`<MyComponent propName="value" />`と記述してPropsを渡す。
-   子は関数の引数として`props`オブジェクトを受け取る。**分割代入**で受け取るのがモダンな書き方。
-   TypeScriptでは、`type`や`interface`を使ってPropsの型を定義し、コンポーネントの引数に注釈する。
-   Propsは**読み取り専用**であり、子コンポーネント内で直接変更してはならない。

📝 **学習のポイント**

-   [ ] Propsは、通常のJavaScript関数における何に似ていますか？
-   [ ] 分割代入を使うと、コードの可読性がどのように向上しますか？ `props.name`と書くのと`name`と書くのでは、どのような違いがありますか？
-   [ ] なぜPropsは読み取り専用でなければならないのでしょうか？ もし子コンポーネントが自由にPropsを変更できたら、どのような問題が起こりうるか想像してみてください。
