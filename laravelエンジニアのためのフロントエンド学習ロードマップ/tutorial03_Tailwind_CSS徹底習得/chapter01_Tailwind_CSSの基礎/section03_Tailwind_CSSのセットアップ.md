# Tutorial 3: Tailwind CSS徹底習得

## Chapter 1: Tailwind CSSの基礎

### Section 3: Tailwind CSSのセットアップ - プロジェクトへの導入とビルド

🖼️ **完成形のイメージ**

このセクションでは、Tailwind CSSを実際にプロジェクトに導入し、動作させるための具体的な手順を学びます。設定ファイルを作成し、ビルドコマンドを実行することで、HTMLに書いたユーティリティクラスが実際のCSSに変換されるプロセスを体験します。

*ここにスクリーンショットを挿入: ターミナルでビルドコマンドを実行している様子と、その結果として生成されたCSSファイルの中身（HTMLで使われているクラスに対応するCSSだけが含まれている）がわかる画像*

--- 

🎯 **このセクションで学ぶこと**

このセクションでは、Tailwind CSSをプロジェクトにセットアップし、最初のビルドを行うまでの一連の流れを実践します。このセクションを終えると、あなたは以下のことができるようになります。

-   `npx tailwindcss init`コマンドを使って、Tailwind CSSの設定ファイル (`tailwind.config.js`) を生成できるようになる。
-   `tailwind.config.js`ファイルで、どのファイルに書かれたユーティリティクラスをスキャン対象にするかを設定できるようになる。
-   Tailwindのディレクティブ (`@tailwind`) を使って、基本的なCSSファイルを準備できるようになる。
-   Tailwind CLIを使って、ユーティリティクラスを実際のCSSにビルド（コンパイル）できるようになる。

--- 

### 導入

前のセクションで`npm`を使ってTailwind CSSをインストールしました。しかし、インストールしただけではまだ使えません。Tailwind CSSは、HTMLやBladeファイルに書かれたクラス名を**スキャン**し、実際に使われているクラスに対応するCSSだけを**抽出して**、一つのCSSファイルを**生成（ビルド）**するという仕組みで動作します。このセクションでは、そのための設定とコマンド実行の方法を学びます。

### 詳細解説

セットアップは大きく分けて3つのステップで行います。

#### Step 1: 設定ファイルの生成

まず、Tailwind CSSの設定ファイルである`tailwind.config.js`を生成します。このファイルで、Tailwind CSSの動作をカスタマイズします。

-   **コマンド:**
    ```bash
    npx tailwindcss init
    ```
-   **コマンド解説:**
    -   `npx`は、`npm` 5.2から導入されたコマンドで、ローカルにインストールされたパッケージのコマンドを実行するためのものです。`npx tailwindcss`とすることで、プロジェクトの`node_modules`にインストールされた`tailwindcss`コマンドを実行できます。
    -   `init`は、初期設定ファイルを生成するサブコマンドです。

    このコマンドを実行すると、プロジェクトのルートに以下の`tailwind.config.js`ファイルが作成されます。

    ```javascript
    /** @type {import('tailwindcss').Config} */
    module.exports = {
      content: [],
      theme: {
        extend: {},
      },
      plugins: [],
    }
    ```

#### Step 2: スキャン対象ファイルの設定

次に、`tailwind.config.js`の中の`content`プロパティを編集します。ここに、Tailwind CSSがスキャンすべきファイル（ユーティリティクラスが書かれているファイル）のパスを指定します。これにより、Tailwindは指定されたファイルを監視し、使われているクラスを検出します。

-   **コード (tailwind.config.js):**
    ```javascript
    /** @type {import('tailwindcss').Config} */
    module.exports = {
      content: [
        "./src/**/*.{html,js}", // srcフォルダ内のすべてのhtmlとjsファイル
        "./public/index.html"   // publicフォルダのindex.html
        // Laravelプロジェクトの場合は './resources/views/**/*.blade.php' などを指定
      ],
      theme: {
        extend: {},
      },
      plugins: [],
    }
    ```
-   **コードリーディング:**
    -   `content`配列の中に、globパターンを使ってファイルを指定します。
    -   `./src/**/*.{html,js}`は、「`src`ディレクトリ、およびその配下のすべてのサブディレクトリ（`**`）にある、拡張子が`.html`または`.js`のすべてのファイル（`*`）」を意味します。

#### Step 3: CSSファイルの準備とビルド

最後に、Tailwindの基本的なスタイルを読み込むためのCSSファイルを作成し、ビルドコマンドを実行します。

3-1. **入力用CSSファイルの作成**

   `src`フォルダなど（場所は任意）に、`input.css`といった名前でファイルを作成し、以下の3行を記述します。

   -   **コード (src/input.css):**
       ```css
       @tailwind base;
       @tailwind components;
       @tailwind utilities;
       ```
   -   **コードリーディング:**
       -   これらはTailwindの**ディレクティブ**です。ビルド時に、Tailwindはこれらのディレクティブを、それぞれ対応するCSS（基本的なリセットスタイル、コンポーネントクラス、すべてのユーティリティクラス）に置き換えます。

3-2. **ビルドコマンドの実行**

   ターミナルで以下のコマンドを実行し、`src/input.css`をビルドして、公開用の`public/output.css`を生成します。

   -   **コマンド:**
       ```bash
       npx tailwindcss -i ./src/input.css -o ./public/output.css --watch
       ```
   -   **コマンド解説:**
       -   `-i` (input): 入力元となるCSSファイルを指定します。
       -   `-o` (output): 出力先となるCSSファイルを指定します。
       -   `--watch`: ファイルの変更を監視し、変更があるたびに自動で再ビルドを実行する便利なオプションです。開発中はこれを付けておくと良いでしょう。

これでセットアップは完了です！あとは、`public/index.html`から`public/output.css`を読み込み、HTMLのクラスに`text-red-500`や`bg-blue-200`といったユーティリティクラスを記述してみてください。`--watch`オプションが有効であれば、ファイルを保存するたびに`output.css`が自動で更新され、スタイルがブラウザに反映されるはずです。

### 💡 TIP

-   **`package.json`の`scripts`を活用する:** 毎回長いビルドコマンドを打つのは大変です。`package.json`の`scripts`セクションに、ビルドコマンドを登録しておくと便利です。

    ```json
    "scripts": {
      "build": "tailwindcss -i ./src/input.css -o ./public/output.css",
      "watch": "tailwindcss -i ./src/input.css -o ./public/output.css --watch"
    },
    ```

    このように登録しておけば、`npm run watch`という短いコマンドでビルドを開始できます。

### ✨ まとめ

-   `npx tailwindcss init`で設定ファイル`tailwind.config.js`を生成する。
-   `tailwind.config.js`の`content`に、ユーティリティクラスを記述するHTMLやJS、Bladeファイルのパスを指定する。
-   `@tailwind`ディレクティブを含む入力用CSSファイルを作成する。
-   `npx tailwindcss -i <input> -o <output>`コマンドで、実際に使われているクラスのみを含むCSSファイルをビルドする。

### 📝 学習のポイント

-   [ ] Tailwind CSSの設定ファイルの名前は何か？
-   [ ] `tailwind.config.js`の`content`プロパティの役割を説明できるか？
-   [ ] Tailwind CSSをビルドするための基本的なコマンド（入力と出力の指定）を書けるか？
