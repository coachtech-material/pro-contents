# Tutorial 11: 品質保証とチーム開発

## Chapter 1: テストの基礎

### Section 3: Next.jsでのコンポーネントテスト (Jest + RTL)

🎯 **このセクションで学ぶこと**

-   フロントエンドのテストでよく使われるJestとReact Testing Library (RTL) の役割を理解する。
-   Next.jsプロジェクトにJestとRTLをセットアップできるようになる。
-   `render`と`screen`を使い、Reactコンポーネントをテスト環境に描画して検証する方法を習得する。
-   「ユーザーは実装の詳細ではなく、最終的にレンダリングされた結果を見る」というRTLの哲学を理解する。

--- 

### イントロダクション：ユーザーの視点でUIをテストする

Next.js（React）アプリケーションのテストでは、一般的に以下の2つのライブラリが組み合わせて使われます。

1.  **Jest**: Facebookによって開発された、人気のJavaScriptテストランナー。テストの実行、アサーション（表明）、モック作成など、テストに必要な包括的な機能を提供します。
2.  **React Testing Library (RTL)**: 「ユーザーが見るもの」をテストすることを推奨する、Reactコンポーネント用のテストユーティリティ集。コンポーネントの内部実装の詳細（StateやPropsなど）を直接テストするのではなく、**ユーザーがブラウザで操作するのと同じように**、レンダリングされたDOMを検証することに焦点を当てています。

この「**実装の詳細ではなく、挙動をテストする**」というRTLの哲学は非常に重要です。なぜなら、UIの見た目や挙動が変わらない限り、内部のリファクタリング（例えば、`useState`を`useReducer`に変更するなど）を行っても、テストが壊れるべきではないからです。これにより、メンテナンス性が高く、リファクタリングに強いテストを書くことができます。

--- 

### 🚀 JestとRTLのセットアップ

Next.jsは、`create-next-app`にテスト環境をセットアップするための公式サンプルを提供しています。これを利用するのが最も簡単です。

```bash
# Next.jsプロジェクトのルートで実行
npx create-next-app --example with-jest my-app
```

既存のプロジェクトに追加する場合は、以下の手順で手動セットアップします。

1.  **必要なライブラリのインストール**

    ```bash
    npm install --save-dev jest jest-environment-jsdom @testing-library/react @testing-library/jest-dom
    ```

2.  **Jest設定ファイルの作成**

    `jest.config.js`を作成し、Next.jsのSWCコンパイラと連携するための設定を行います。

    ```javascript
    // jest.config.js
    const nextJest = require("next/jest");

    const createJestConfig = nextJest({
      dir: "./",
    });

    const customJestConfig = {
      setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],
      testEnvironment: "jest-environment-jsdom",
    };

    module.exports = createJestConfig(customJestConfig);
    ```

3.  **カスタムマッチャーの設定**

    `@testing-library/jest-dom`が提供する、DOMの状態を検証するための便利なマッチャー（例: `toBeInTheDocument()`）をJestで使えるように、`jest.setup.js`ファイルを作成します。

    ```javascript
    // jest.setup.js
    import "@testing-library/jest-dom/extend-expect";
    ```

--- 

### ⚙️ はじめてのコンポーネントテスト

では、簡単な`Button`コンポーネントをテストしてみましょう。

**テスト対象のコンポーネント:**

```tsx
// src/components/Button.tsx

import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
}

export const Button = ({ children, ...props }: ButtonProps) => {
  return (
    <button
      className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      {...props}
    >
      {children}
    </button>
  );
};
```

**テストコード:**

テストファイルは、`__tests__`ディレクトリに置くか、コンポーネントと同じ階層に`.test.tsx`という拡張子で作成するのが一般的です。

```tsx
// src/components/__tests__/Button.test.tsx

import { render, screen } from "@testing-library/react";
import { Button } from "../Button";

// `describe`で関連するテストをグループ化できる
describe("Button Component", () => {
  // `it` または `test` で個々のテストケースを定義
  it("renders the button with children", () => {
    // 1. Arrange & Act: コンポーネントをレンダリング
    render(<Button>Click Me</Button>);

    // 2. Assert: 画面に期待する要素が存在するか検証

    // `screen.getByRole`で要素を取得。ボタンは`button`ロールを持つ
    // `name`オプションでアクセシブルネーム（表示テキスト）を指定
    const buttonElement = screen.getByRole("button", { name: /click me/i });

    // `expect`とRTLのカスタムマッチャーで表明
    expect(buttonElement).toBeInTheDocument();
  });

  it("applies disabled attribute correctly", () => {
    // 1. Arrange & Act: `disabled` propを渡してレンダリング
    render(<Button disabled>Click Me</Button>);

    // 2. Assert: ボタンがdisabled状態であることを検証
    const buttonElement = screen.getByRole("button", { name: /click me/i });
    expect(buttonElement).toBeDisabled();
  });
});
```

#### テストの実行

`package.json`にテスト実行用のスクリプトを追加します。

```json
// package.json
"scripts": {
  "dev": "next dev",
  "build": "next build",
  "start": "next start",
  "lint": "next lint",
  "test": "jest"
}
```

そして、コマンドを実行します。

```bash
npm test
```

#### コードの解説

-   `render()`: RTLの関数。引数に渡されたReactコンポーネントを、テスト用の仮想的なDOMにレンダリングします。
-   `screen`: レンダリングされたDOMにアクセスするためのオブジェクト。`getBy...`, `findBy...`, `queryBy...`といったクエリメソッドを提供します。
-   `getByRole()`: `screen`のクエリメソッドの一つ。**アクセシビリティのロール**に基づいて要素を検索します。これは、ユーザーがどのようにUIを認識するかに近いため、最も推奨されるクエリです。
-   `/click me/i`: 正規表現。`i`フラグにより、大文字・小文字を区別せずにマッチします。
-   `toBeInTheDocument()`: 要素がDOM内に存在することを検証するカスタムマッチャー。
-   `toBeDisabled()`: 要素が`disabled`属性を持っていることを検証するカスタムマッチャー。

--- 

### 🤔 RTLのクエリメソッド

`screen`オブジェクトが提供するクエリは、主に3つのファミリーに分かれています。

| ファミリー | 要素が見つからない場合 | 用途 |
|:---|:---|:---|
| **`getBy...`** | **エラーをスローする** | 要素が**必ず存在するはず**の場合に使う。テストの主要な表明に最適。 |
| **`queryBy...`** | **`null`を返す** | 要素が**存在しないこと**を検証したい場合に使う。 |
| **`findBy...`** | **Promiseを返す** | 要素が**非同期で出現する**（例: APIレスポンス後に表示される）のを待ちたい場合に使う。 |

**クエリの優先順位**
RTLは、ユーザーの操作に近い順で、以下の優先順位でクエリを使うことを推奨しています。

1.  **`getByRole`**: アクセシビリティの観点から最も推奨。
2.  **`getByLabelText`**: フォーム要素の`<label>`から探す。
3.  **`getByPlaceholderText`**: プレースホルダーから探す。
4.  **`getByText`**: 表示されているテキストで探す。
5.  **`getByDisplayValue`**: フォーム要素の現在の`value`で探す。

`getByTestId`という、テスト専用の`data-testid`属性で探す方法もありますが、これは上記のクエリでどうしても要素を特定できない場合の「最後の手段」とされています。

--- 

✨ **まとめ**

-   Reactコンポーネントのテストには、テストランナーの**Jest**と、テストユーティリティの**React Testing Library (RTL)**を組み合わせるのが一般的である。
-   RTLは、コンポーネントの内部実装ではなく、**ユーザーの視点から見た挙動**をテストすることを推奨している。
-   `render`関数でコンポーネントを描画し、`screen`オブジェクトのクエリメソッド（特に`getByRole`）を使って、レンダリングされた要素を取得・検証する。
-   `@testing-library/jest-dom`が提供するカスタムマッチャー（`toBeInTheDocument`など）を使うと、DOMの状態を直感的に表明できる。

📝 **学習のポイント**

-   [ ] ボタンをクリックするとカウンターが増える、シンプルなカウンターコンポーネントを作成してください。そして、RTLの`userEvent`ライブラリを使って、「ボタンをクリックすると、表示されている数字が1から2に増えること」をテストするコードを書いてみましょう。
-   [ ] APIからデータを非同期で取得して表示するコンポーネントを考えます。`findBy...`クエリと、Jestのモック機能（`jest.mock`）を使って、`fetch`をモック化し、「Loading...」という表示が消え、APIからのデータが表示されることをテストするにはどうすればよいか、手順を考えてみましょう。
-   [ ] 「スナップショットテスト」というJestの機能について調べてみましょう。これはどのようなテストで、どのような利点と欠点がありますか？
