# 7-1-2: JSXの基本ルール

## Chapter 1: Reactの基本概念

### Section 2: JSXの基本ルール

🎯 **このセクションで学ぶこと**

-   JSXがJavaScriptの構文拡張であり、最終的にJavaScriptオブジェクトに変換されることを理解する。
-   JSXを記述する上での3つの重要なルール（単一のルート要素、閉じタグの必須、`camelCase`の属性名）を習得する。
-   JSX内で波括弧`{}`を使って、JavaScriptの変数を埋め込む方法を習得する。

--- 

### イントロダクション：JavaScriptの中にHTMLを書く？

Reactのコードを初めて見ると、多くの人が驚きます。なぜなら、JavaScriptのファイル（`.js`または`.jsx`, `.tsx`）の中に、HTMLのようなコードが直接書かれているからです。

```jsx
const element = <h1>Hello, world!</h1>;
```

このHTMLのような構文が**JSX (JavaScript XML)** です。JSXは、ReactでUIの構造を記述するために使われる、JavaScriptの構文拡張です。

一見すると奇妙に感じるかもしれませんが、JSXはUIの構造とロジックを同じ場所に記述できるため、コンポーネントの全体像を把握しやすくなるという大きなメリットがあります。このセクションでは、JSXを正しく書くための基本的なルールを学びます。

--- 

### ⚙️ JSXとは？ JavaScriptへの変換

JSXはブラウザが直接解釈できるものではありません。Babelのような**トランスパイラ**によって、最終的に`React.createElement()`という関数呼び出しに変換されます。この関数は、UIの構造を表すJavaScriptオブジェクトを生成します。

**JSX:**
```jsx
const element = <h1 className="greeting">Hello, world!</h1>;
```

**上記が変換されたJavaScriptコード:**
```javascript
const element = React.createElement(
  'h1',
  {className: 'greeting'},
  'Hello, world!'
);
```

つまり、JSXは`React.createElement()`をより直感的で書きやすくするための**シンタックスシュガー（糖衣構文）**なのです。開発者はHTMLを書く感覚でUIを構築できますが、その実体はJavaScriptである、という点を理解しておくことが重要です。

--- 

### 🚀 JSXの3大ルール

JSXを書く際には、HTMLとは異なるいくつかの重要なルールを守る必要があります。

#### ルール1：コンポーネントは単一のルート要素を返さなければならない

コンポーネントが返すJSXは、必ず**一つの親要素**で囲まれている必要があります。複数の要素を並べて返すことはできません。

**❌ 間違い:**
```jsx
return (
  <h1>Title</h1>
  <p>Paragraph</p>
);
```

**⭕ 正しい:**
```jsx
return (
  <div>
    <h1>Title</h1>
    <p>Paragraph</p>
  </div>
);
```

もし、余計な`div`要素をDOMに追加したくない場合は、**フラグメント (`<></>`)** を使って要素をグループ化できます。

**⭕ フラグメントを使った正しい書き方:**
```jsx
return (
  <>
    <h1>Title</h1>
    <p>Paragraph</p>
  </>
);
```

#### ルール2：すべてのタグは閉じなければならない

HTMLでは`<br>`や`<img>`のように閉じタグが不要な要素もありますが、JSXでは**すべてのタグを明示的に閉じる**必要があります。子要素を持たないタグは、`/>`で自己終了させます。

**❌ 間違い:**
```jsx
return (
  <>
    <h1>Title</h1>
    <img src="image.png">
  </>
);
```

**⭕ 正しい:**
```jsx
return (
  <>
    <h1>Title</h1>
    <img src="image.png" />
  </>
);
```

#### ルール3：属性名は`camelCase`で書く

JSXの属性は、最終的にJavaScriptオブジェクトのプロパティになります。そのため、HTMLの属性名とは少し異なる命名規則に従います。

-   `class` → `className`
-   `for` → `htmlFor`
-   `onclick` → `onClick`
-   `tabindex` → `tabIndex`

`class`や`for`はJavaScriptの予約語であるため、そのままでは使えません。その他の多くの属性（例: `onclick`）は、`camelCase`形式で記述するのがルールです。

**❌ 間違い (HTMLの書き方):**
```jsx
<div class="my-class" onclick="handleClick()">Click me</div>
```

**⭕ 正しい (JSXの書き方):**
```jsx
<div className="my-class" onClick={handleClick}>Click me</div>
```

--- 

### ⚙️ 波括弧`{}`によるJavaScriptの埋め込み

JSXの最も強力な機能の一つが、波括弧`{}`を使って、その中にJavaScriptの式を直接埋め込めることです。

#### 変数の表示

```jsx
const name = "Taro";
const element = <h1>Hello, {name}!</h1>; // "Hello, Taro!" と表示される
```

#### 関数の結果の表示

```jsx
function formatName(user) {
  return `${user.firstName} ${user.lastName}`;
}

const user = { firstName: 'Hanako', lastName: 'Suzuki' };
const element = <h1>Hello, {formatName(user)}!</h1>; // "Hello, Hanako Suzuki!" と表示される
```

#### 属性への適用

属性の値として文字列リテラルではなく、JavaScriptの変数を渡したい場合も波括弧を使います。

```jsx
const imageUrl = "/images/profile.png";
const element = <img src={imageUrl} />;
```

**注意:** 波括弧の中には、**値を返す式**（変数、関数呼び出し、三項演算子など）のみ記述できます。`if`文や`for`ループのような文は直接記述できません。

--- 

✨ **まとめ**

-   **JSX**は、ReactでUIを記述するためのJavaScriptの構文拡張である。
-   JSXは、最終的に`React.createElement()`という関数呼び出しに変換される。
-   JSXの3大ルール:
    1.  **単一のルート要素**で全体を囲む（`<div>`またはフラグメント`<></>`）。
    2.  すべてのタグは**必ず閉じる**（自己終了タグは`<img />`のように書く）。
    3.  属性名は`class` -> `className`のように**`camelCase`**で書く。
-   波括弧`{}`を使うことで、JSX内にJavaScriptの変数や式を埋め込むことができる。

📝 **学習のポイント**

-   [ ] なぜJSXでは`class`の代わりに`className`を使わなければならないのでしょうか？
-   [ ] 以下のHTMLコードを、JSXのルールに従って書き直してください。
    ```html
    <div>
      <label for="name">名前:</label>
      <input type="text" id="name">
      <img src="icon.png">
    </div>
    ```
-   [ ] `const element = <h1>{if (user) { return user.name; }}</h1>;` というJSXがエラーになるのはなぜですか？ これを正しく書くにはどうすればよいでしょうか？（ヒント: 三項演算子）
