# 7-2-3: Propsのデフォルト値と分割代入

## Chapter 2: Propsによるデータ受け渡し

### Section 3: Propsのデフォルト値と分割代入の応用

🎯 **このセクションで学ぶこと**

-   Propsが渡されなかった場合に備えて、**デフォルト値**を設定する方法を習得する。
-   Propsの型定義で、特定のPropsを**任意（オプショナル）**にする方法を習得する。
-   分割代入を使い、残りのPropsをまとめてオブジェクトとして受け取る**Restパラメータ** (`...rest`) の使い方を学ぶ。

--- 

### イントロダクション：より堅牢なコンポーネントへ

Propsを使うことで、コンポーネントは非常に柔軟になりました。しかし、コンポーネントを多くの場所で再利用していると、「うっかりPropsを渡し忘れる」というミスが起こりがちです。

また、`button`タグのように、`onClick`や`disabled`など、たくさんの属性を受け取れるコンポーネントを作りたい場合、すべてのPropsを一つ一つ定義するのは大変です。

このセクションでは、Propsのデフォルト値を設定する方法や、分割代入の応用テクニックを使って、より堅牢で柔軟なコンポーネントを作成する方法を学びます。

--- 

### ⚙️ Propsのデフォルト値

Propsが親コンポーネントから渡されなかった場合に、代わりに使われる値を設定しておくことができます。これにより、Propsの渡し忘れによるエラーを防いだり、基本的なスタイルを保証したりできます。

デフォルト値の設定は、関数の引数のデフォルト値と同じ構文を、分割代入と組み合わせて使います。

**例：`Button`コンポーネントにデフォルト値を設定する**

```tsx
// Button.tsx

// 1. Propsの型を定義する
type ButtonProps = {
  label: string;
  // themeは任意（渡されなくても良い）なので、プロパティ名の後ろに ? を付ける
  theme?: 'primary' | 'secondary';
};

// 2. 分割代入でデフォルト値を設定する
function Button({ label, theme = 'secondary' }: ButtonProps) {
  // themeの値に応じてCSSクラスを切り替える
  const buttonClass = theme === 'primary' ? 'button-primary' : 'button-secondary';

  return <button className={buttonClass}>{label}</button>;
}
```

**解説:**
1.  **`theme?: 'primary' | 'secondary'`**: `theme` Propsの型定義です。
    -   `?` をプロパティ名の後ろに付けることで、このPropsが**任意（オプショナル）**であることを示します。これにより、`Button`コンポーネントを呼び出す際に`theme`を渡さなくても、TypeScriptのエラーが発生しなくなります。
    -   `'primary' | 'secondary'` は**ユニオン型**といい、`theme`が取りうる値をこの2つの文字列に限定します。これにより、`'danger'`のような意図しない値が渡されるのを防ぎます。
2.  **`theme = 'secondary'`**: 分割代入の部分で、`theme`にデフォルト値を設定しています。もし親から`theme` Propsが渡されなかった場合、`theme`変数の値は自動的に`'secondary'`になります。

**呼び出し側の例 (`App.tsx`)**

```tsx
// App.tsx

<Button label="OK" theme="primary" /> // primaryテーマのボタンが表示される
<Button label="Cancel" />            // themeを渡していないので、デフォルト値のsecondaryテーマのボタンが表示される
```

--- 

### 🚀 RestパラメータによるPropsの集約

標準のHTMLタグが持つ属性（`onClick`, `disabled`, `id`, `aria-label`など）を、すべてカスタムコンポーネントでも受け取れるようにしたい場合があります。しかし、これらすべてをPropsの型定義に一つ一つ書くのは現実的ではありません。

このような場合に便利なのが、分割代入の**Restパラメータ (`...rest`)** です。

**例：`button`のネイティブな属性をすべて受け取る`Button`コンポーネント**

```tsx
// Button.tsx

import React from "react";

// 1. Propsの型を拡張する
type ButtonProps = {
  label: string;
  theme?: 'primary' | 'secondary';
} & React.ComponentPropsWithoutRef<'button'>; // buttonタグの全属性を継承

// 2. 分割代入で残りのPropsをrestに集約
function Button({ label, theme = 'secondary', ...rest }: ButtonProps) {
  const buttonClass = theme === 'primary' ? 'button-primary' : 'button-secondary';

  // 3. 集約したpropsをbutton要素に展開する
  return (
    <button className={buttonClass} {...rest}>
      {label}
    </button>
  );
}
```

**解説:**
1.  **`& React.ComponentPropsWithoutRef<'button'>`**: ここがTypeScriptのテクニックです。
    -   `React.ComponentPropsWithoutRef<'button'>`は、Reactが提供する型で、`button`タグが受け取れるすべての属性（`onClick`, `disabled`, `type`など）の型情報を持っています。
    -   `&`（インターセクション型）を使って、自前で定義した`{ label, theme }`という型と結合することで、`ButtonProps`は「`label`と`theme`、**かつ**、`button`タグの全属性」を持つ型になります。
2.  **`...rest`**: 分割代入の最後に`...`を付けた変数を置くと、まだ分割代入されていない**残りのプロパティがすべて**、その変数にオブジェクトとして集約されます。ここでは、`label`と`theme`以外のすべてのProps（`onClick`, `disabled`など）が`rest`オブジェクトに格納されます。
3.  **`{...rest}`**: `button`要素の属性として`{...rest}`と記述すると、`rest`オブジェクトが持つすべてのプロパティが、`button`タグの属性として展開されます。これを**スプレッド構文**と呼びます。
    -   例えば、`rest`が`{ onClick: handleClick, disabled: true }`というオブジェクトだった場合、これは`onClick={handleClick} disabled={true}`と書いたのと同じ意味になります。

**呼び出し側の例 (`App.tsx`)**

```tsx
// App.tsx

const handleClick = () => alert('Clicked!');

<Button label="Click me" onClick={handleClick} />
<Button label="Submitting..." disabled={true} />
```

このテクニックを使うことで、コンポーネントのProps定義をシンプルに保ちつつ、HTML要素が持つすべての機能（アクセシビリティ属性を含む）を損なうことなく、ラップしたコンポーネントを作成できます。

--- 

✨ **まとめ**

-   Propsの型定義でプロパティ名の後ろに`?`を付けると、そのPropsは**任意（オプショナル）**になる。
-   分割代入の中で`propName = 'defaultValue'`と記述することで、Propsが渡されなかった場合の**デフォルト値**を設定できる。
-   分割代入の最後に`...rest`と記述すると、残りのPropsを**`rest`オブジェクトに集約**できる（Restパラメータ）。
-   JSX内で`{...rest}`と記述すると、`rest`オブジェクトのプロパティを**属性として展開**できる（スプレッド構文）。
-   `React.ComponentPropsWithoutRef<'tag'>`とインターセクション型`&`を組み合わせることで、既存のHTMLタグの属性をすべて受け継ぐ、柔軟なコンポーネントを型安全に作成できる。

📝 **学習のポイント**

-   [ ] なぜPropsにデフォルト値を設定することが、コンポーネントの堅牢性を高めるのでしょうか？
-   [ ] `...rest` パラメータを使わずに、`Button`コンポーネントで`onClick`と`disabled`の両方を受け取れるようにするには、`ButtonProps`の型定義とコンポーネントの実装をどのように変更する必要がありますか？
-   [ ] `input`タグをラップした`TextInput`コンポーネントを作成する場合、`React.ComponentPropsWithoutRef`はどのように使えばよいでしょうか？
