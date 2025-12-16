# Tutorial 3: Tailwind CSS徹底習得

## Chapter 1: Tailwind CSSの基礎

### Chapter 1 ハンズオン: Tailwind CSSでプロフィールページをリファクタリングする

🖼️ **完成形のイメージ**

このハンズオンでは、Tutorial 2で作成したCSSでスタイリングされたプロフィールページを、Tailwind CSSを使って完全にリファクタリングします。最終的な見た目は同じですが、その実装方法が従来のCSSからユーティリティファーストへと根本的に変わることを体験します。

*ここにスクリーンショットを挿入: 完成したプロフィールページ（見た目はTutorial 2の完成形と同じ）と、そのページのHTMLソースコード（class属性にTailwindのユーティリティクラスが多数記述されている様子）を並べて表示*

--- 

🎯 **このセクションで学ぶこと**

このハンズオンを終えると、あなたは以下のことができるようになります。

-   ゼロからTailwind CSSのプロジェクトをセットアップし、ビルドプロセスを構築できるようになる。
-   既存のCSSスタイルを、等価なTailwind CSSのユーティリティクラスに置き換えることができるようになる。
-   従来のCSSで書かれたプロジェクトをTailwind CSSにリファクタリングする具体的な手順と思考プロセスを理解する。

--- 

### 🏃 実践: 一緒に作ってみましょう！

理論を学んだら、次は実践です。Tutorial 2で完成させたプロフィールページを題材に、`style.css`に書かれたスタイルを一つずつTailwindのユーティリティクラスに置き換え、最終的に`style.css`を空にすることを目指します。

#### 💭 実装の思考プロセス

**このハンズオンのゴール:**

1.  **プロジェクトセットアップ:** `npm`プロジェクトを初期化し、Tailwind CSSをインストール、設定ファイルとビルドプロセスを準備する。
2.  **HTMLの準備:** Tutorial 2で作成した`index.html`をコピーし、`style.css`の読み込みを、Tailwindのビルド成果物である`output.css`に差し替える。
3.  **段階的なリファクタリング:** `style.css`のスタイル定義を上から順に見ていき、対応するユーティリティクラスを`index.html`の`class`属性に追加していく。
4.  **CSSファイルの削除:** すべてのスタイルをユーティリティクラスに置き換え終わったら、`style.css`の中身を空にし、ページのデザインが崩れないことを確認する。

💡 **ポイント:** 最初は、どのCSSプロパティがどのユーティリティクラスに対応するのか分からなくて当然です。Tailwind CSSの公式ドキュメントは非常に優秀なので、常に 옆に開いておき、「`background-color`はどう書くんだろう？」→「ドキュメントで`background-color`を検索」という流れで進めていくのが最も効率的な学習方法です。

#### 📝 ステップバイステップで実装

##### Step 1: プロジェクトのセットアップ

まず、このハンズオン用の新しいプロジェクトフォルダを作成し、Tailwind CSSをセットアップします。

1-1. `tailwind-profile`のような名前で新しいフォルダを作成し、その中でターミナルを開きます。

1-2. `npm`プロジェクトを初期化し、Tailwind CSSをインストールします。

-   **コマンド:**
    ```bash
    npm init -y
    npm install -D tailwindcss
    npx tailwindcss init
    ```

1-3. `tailwind.config.js`の`content`を編集して、これから作成するHTMLファイルをスキャン対象に加えます。

-   **コマンド/コード (tailwind.config.js):**
    ```javascript
    content: ["./*.html"], // ルートにあるすべてのHTMLファイルを対象にする
    ```

1-4. 入力用のCSSファイル`src/input.css`を作成します。

-   **コマンド/コード (src/input.css):**
    ```css
    @tailwind base;
    @tailwind components;
    @tailwind utilities;
    ```

1-5. `package.json`の`scripts`にビルドコマンドを登録します。

-   **コマンド/コード (package.json):**
    ```json
    "scripts": {
      "watch": "tailwindcss -i ./src/input.css -o ./output.css --watch"
    },
    ```

1-6. ターミナルでビルドを監視モードで開始します。

-   **コマンド:**
    ```bash
    npm run watch
    ```

##### Step 2: HTMLの準備とCSSの置き換え

Tutorial 2の`index.html`と`style.css`をコピーしてきて、リファクタリングの準備をします。

2-1. Tutorial 2で完成した`index.html`をプロジェクトのルートにコピーします。

2-2. `index.html`の`<head>`部分を修正し、`style.css`の代わりに、Tailwindが生成する`output.css`を読み込むように変更します。

-   **コマンド/コード (index.html):**
    ```html
    <!-- 変更前 -->
    <link rel="stylesheet" href="css/style.css">
    <!-- 変更後 -->
    <link rel="stylesheet" href="/output.css">
    ```

##### Step 3: ユーティリティクラスへの置き換え

ここからが本番です。`style.css`（まだコピーしていませんが、Tutorial 2の内容を参考にします）のスタイルを一つずつユーティリティクラスに変換していきます。

-   **`body`のスタイル:**
    -   `background-color: #f4f4f4;` → `bg-gray-100`
    -   `font-family: sans-serif;` → `font-sans`
    -   `color: #333;` → `text-gray-800`
    -   **適用後 (index.html):** `<body class="bg-gray-100 font-sans text-gray-800">`

-   **`#profile-card`のスタイル:**
    -   `width: 600px;` → `w-[600px]` (任意の花) or `max-w-2xl` (近い値)
    -   `margin: 40px auto;` → `my-10 mx-auto`
    -   `background-color: #ffffff;` → `bg-white`
    -   `padding: 30px;` → `p-8` (近い値)
    -   `border: 1px solid #ddd;` → `border border-gray-200`
    -   `border-radius: 8px;` → `rounded-lg`
    -   **適用後 (index.html):** `<div id="profile-card" class="max-w-2xl my-10 mx-auto bg-white p-8 border border-gray-200 rounded-lg">`

-   **`.profile-image`のスタイル:**
    -   `display: block;` → `block`
    -   `margin: 0 auto 20px;` → `mx-auto mb-5`
    -   `border-radius: 50%;` → `rounded-full`
    -   **適用後 (index.html):** `<img ... class="block mx-auto mb-5 rounded-full">`

...このように、一つ一つのスタイルをTailwindのクラスに置き換えていきます。`h1`, `h2`, `.social-links a`なども同様に作業を進めます。

-   **`h1`:** `text-center text-3xl font-bold text-gray-800 mb-4`
-   **`h2`:** `border-b-2 border-blue-500 pb-2 mt-8 mb-4 text-xl font-semibold`
-   **`.social-links`:** `flex justify-center gap-4 list-none p-0 mt-5`
-   **`.social-links a`:** `block py-2 px-5 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors`

##### Step 4: 確認

すべてのスタイルをユーティリティクラスに置き換えたら、`index.html`をブラウザで開いてみてください。Tutorial 2の完成形とほぼ同じ見た目になっているはずです。これで、`style.css`は不要になりました！

#### ✨ 完成！

お疲れ様でした！あなたは今、既存のCSSプロジェクトを、モダンで効率的なTailwind CSSプロジェクトへとリファクタリングするスキルを身につけました。クラス名を考えることから解放され、HTMLファイル内でデザインが完結する快適さを実感できたのではないでしょうか。これが、現代のフロントエンド開発のスタンダードの一つです。
