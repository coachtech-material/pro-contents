# Tutorial 3: Tailwind CSS 徹底習得

## Chapter 3: カスタムテーマとベストプラクティス

### Chapter 3 ハンズオン: プロジェクトのブランドカラーを定義し、カスタムボタンコンポーネントを作成する

🎯 **このハンズオンで達成すること**

-   `tailwind.config.js`を編集し、プロジェクト独自のブランドカラーを追加できるようになる。
-   `@apply`を使い、カスタマイズした色を含んだボタンコンポーネント（`.btn`）を作成できるようになる。
-   作成したコンポーネントを使い、複数のバリエーション（プライマリ、セカンダリ）を持つボタンを効率的に実装できるようになる。

--- 

🖼️ **完成イメージ**

このハンズオンでは、まずプロジェクトのテーマカラーとして「Laravelの赤」と「落ち着いたグレー」を定義します。その後、それらの色を使った2種類のボタンコンポーネント（`.btn-primary`, `.btn-secondary`）を`@apply`を使って作成します。

*ここにスクリーンショットを挿入: (1) Laravelの赤色を基調としたプライマリボタン。 (2) グレーを基調としたセカンダリボタン。どちらも同じ形状・サイズで、ホバー時のインタラクションも実装されている。*

--- 

### 🧠 先輩エンジニアの思考プロセス

「ブランドカラーを使ったボタンをコンポーネント化してください」と頼まれたとき、頭の中では以下のような手順を考えます。

| 手順 | 思考プロセス |
|:---|:---|
| **1. 色の定義 (`tailwind.config.js`)** | まずはデザインシステムの中核となる色を定義しよう。`theme.extend.colors`にブランドカラーを追加する。 |
| **2. 共通スタイルの抽出 (`@apply`)** | プライマリボタンとセカンダリボタンで共通するスタイル（サイズ、余白、フォント、角丸など）は、ベースとなる`.btn`クラスにまとめよう。 |
| **3. バリエーションの作成 (`@apply`)** | 色に関する部分だけを、`.btn-primary`と`.btn-secondary`に分けて定義しよう。こうすれば、後から色の変更が楽になる。 |
| **4. HTMLでの実装** | 最後に、HTML側で`.btn`と`.btn-primary`のように、基本クラスと修飾クラスを組み合わせて使う。 |

💡 **ポイント:** **「共通部分」と「可変部分」を分離する**のが、優れたコンポーネント設計の鍵です。`@apply`を使う際も、この原則を意識することが重要です。

--- 

### 🏃 実践: Step by Stepでカスタムボタンを作成しよう

`tailwind-handson`プロジェクトを使います。

#### Step 1: ブランドカラーの追加

まず、`tailwind.config.js`を開き、`theme.extend.colors`にプロジェクトのブランドカラーを追加します。

```javascript
// tailwind.config.js
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'brand': {
          'primary': '#F05340', // Laravel Red
          'secondary': '#6c757d', // Gray
        },
      },
    },
  },
  plugins: [],
}
```

-   **コードリーディング**
    -   `brand`というキーで色をグループ化し、その中に`primary`と`secondary`を定義しました。これにより、`bg-brand-primary`や`text-brand-secondary`といったクラス名で色を使えるようになります。

#### Step 2: `@apply`を使ったコンポーネントの作成

次に、`src/input.css`を開き、`@tailwind`ディレクティブの下にボタンコンポーネントのスタイルを記述します。

```css
/* src/input.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* ボタンの共通スタイル */
.btn {
  @apply font-bold py-2 px-4 rounded-lg shadow-md transition-colors duration-300;
}

/* プライマリボタン */
.btn-primary {
  @apply bg-brand-primary text-white;
}
.btn-primary:hover {
  @apply bg-red-700; /* 少し濃い赤 */
}

/* セカンダリボタン */
.btn-secondary {
  @apply bg-brand-secondary text-white;
}
.btn-secondary:hover {
  @apply bg-gray-700; /* 少し濃いグレー */
}
```

-   **コードリーディング**
    -   `.btn`: ボタンの形状やフォント、影、アニメーション効果など、**色以外の共通スタイル**をすべてここにまとめます。
        -   `transition-colors duration-300`: ホバー時の色の変化が0.3秒かけて滑らかに行われるようになります。
    -   `.btn-primary`, `.btn-secondary`: **色に関するスタイル**だけをそれぞれ定義します。
    -   `:hover`: ホバー時の色も定義します。ここでは、configで定義した色名ではなく、Tailwindのデフォルトカラーパレットの濃い色を指定しています。（もちろん、`hover`用の色をconfigで定義することも可能です）

#### Step 3: HTMLでの実装

最後に、`src/index.html`を編集し、作成したボタンコンポーネントを使ってみましょう。`<body>`の中身を以下のように書き換えます。

```html
<!-- src/index.html -->
<body class="bg-gray-100 flex justify-center items-center h-screen space-x-4">

  <button class="btn btn-primary">
    Primary Button
  </button>

  <button class="btn btn-secondary">
    Secondary Button
  </button>

</body>
```

-   **コードリーディング**
    -   `class="btn btn-primary"`: **共通の`.btn`クラス**と、**バリエーションの`.btn-primary`クラス**を両方指定しているのがポイントです。これにより、スタイルが合成されます。

#### Step 4: ビルドと確認

ターミナルで`npm run watch`が実行されていることを確認し、ブラウザをリロードしてください。

定義したブランドカラーの2種類のボタンが表示され、それぞれにホバーエフェクトが適用されていれば成功です。`src/input.css`の`.btn-primary`の`bg-brand-primary`を`bg-blue-500`などに変更して保存すると、即座にブラウザ上のボタンの色が変わることも確認してみましょう。コンポーネント化のメリットが実感できるはずです。

--- 

✨ **まとめ**

-   `tailwind.config.js`でプロジェクトのカラースキームを定義することで、デザインの一貫性を保ちやすくなる。
-   `@apply`を使う際は、「共通スタイル」と「バリエーションのスタイル」を分離して定義すると、メンテナンス性の高いコンポーネントを作ることができる。
-   HTML側では、ベースとなるクラスとバリエーションのクラスを組み合わせて使用する。

📝 **学習のポイント**

-   [ ] もし「危険な操作」を表す赤い`.btn-danger`を追加したい場合、`input.css`にどのようなコードを追加しますか？
-   [ ] `.btn`クラスに`disabled:opacity-50 disabled:cursor-not-allowed`というユーティリティを追加すると、HTMLで`<button class="btn btn-primary" disabled>...`とした場合にどのような表示になるか想像できますか？
-   [ ] このハンズオンで作成したボタンコンポーネントは、`@apply`を使わずにReactコンポーネントとして実装することもできます。もしReactで実装する場合、どのようなコードになるか考えてみましょう。
