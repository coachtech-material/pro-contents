# Tutorial 6: TypeScript 基礎から実用へ

## Chapter 2: TypeScriptの開発環境設定

### Chapter 2 ハンズオン: TypeScriptプロジェクトの環境構築

🎯 **このハンズオンで達成すること**

-   `npm`を使い、TypeScript, ESLint, Prettierをゼロからプロジェクトに導入できる。
-   `tsconfig.json`, `.eslintrc.js`, `.prettierrc.json`の3つの主要な設定ファイルを自分で作成・設定できる。
-   `package.json`にスクリプトを登録し、コマンドラインからコンパイル、リント、フォーマットを実行できる。
-   VS Codeの拡張機能と連携させ、保存時に自動でコードが整形される快適な開発体験を構築する。

--- 

🖼️ **完成イメージ**

`my-ts-app`という名前のディレクトリ内に、TypeScriptを開発するための基本的なファイル群と設定がすべて揃った状態を作り上げます。最終的に、`src/index.ts`に書いたTypeScriptコードが、`dist/index.js`にコンパイルされ、`node`コマンドで実行できるようになります。

**最終的なディレクトリ構造:**
```
my-ts-app/
├── node_modules/
├── src/
│   └── index.ts       # TypeScriptソースコード
├── dist/
│   └── index.js       # コンパイル後のJavaScript
├── .eslintrc.js       # ESLint設定ファイル
├── .prettierrc.json   # Prettier設定ファイル
├── package.json
├── package-lock.json
└── tsconfig.json      # TypeScript設定ファイル
```

--- 

### 🧠 先輩エンジニアの思考プロセス

「新しいTypeScriptプロジェクト、セットアップお願い！」と言われたら、以下の手順を機械的に実行する。

1.  **土台作り:** まずはプロジェクトの器となるディレクトリを作り、`npm init`で`package.json`を生成する。これがすべての始まり。
2.  **TypeScriptの導入:** 主役である`typescript`を`devDependencies`としてインストール。そして、`npx tsc --init`で`tsconfig.json`を生成する。これは「設計図」だから、最初に作るのがセオリー。
3.  **`tsconfig.json`の編集:** 生成された`tsconfig.json`を開き、最低限必要な項目を編集する。
    -   `target`: モダンな環境なら`"ES2020"`以上でOK。
    -   `module`: Node.jsで動かすなら`"CommonJS"`。
    -   `outDir`: コンパイル後の`.js`ファイルの出力先。`"./dist"`が一般的。
    -   `rootDir`: ソースコードの場所。`"./src"`が分かりやすい。
    -   `strict`: **これは絶対`true`！** TypeScriptの恩恵を最大限に受けるため。
4.  **コード品質ツールの導入:** 次に脇を固める役者たち。`eslint`と`prettier`関連のパッケージをまとめてインストールする。
    -   `eslint`, `@typescript-eslint/parser`, `@typescript-eslint/eslint-plugin` (ESLint本体とTypeScript対応)
    -   `prettier`, `eslint-config-prettier` (Prettier本体とESLintとの競合解消)
5.  **設定ファイルの作成:** ESLintとPrettierの設定ファイル (`.eslintrc.js`, `.prettierrc.json`) を作成する。これはネット上のテンプレートを参考にすればOK。大事なのは、`.eslintrc.js`の`extends`の最後に`"prettier"`を入れること。
6.  **`package.json`のスクリプト設定:** 毎回長いコマンドを打つのは面倒なので、`package.json`の`scripts`にショートカットを登録する。
    -   `build`: `tsc`を実行してコンパイルする。
    -   `lint`: `eslint`を実行する。
    -   `format`: `prettier`を実行する。
7.  **動作確認:** `src/index.ts`に簡単なコードを書き、`npm run build`で`dist/index.js`が生成されるか確認。`node dist/index.js`で実行できれば完璧。

この流れを一度経験すれば、どんなTypeScriptプロジェクトでも怖くない。

--- 

### 🏃 実践: Step by Stepで環境を構築しよう

#### Step 1: プロジェクトの初期化

```bash
# ターミナル
mkdir my-ts-app
cd my-ts-app
npm init -y
```

#### Step 2: TypeScriptのインストールと設定

```bash
# ターミナル
npm install --save-dev typescript
npx tsc --init
```

生成された`tsconfig.json`を以下のように編集します。（コメントアウトを解除・修正）

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "CommonJS",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

#### Step 3: ESLintとPrettierのインストール

関連パッケージをまとめてインストールします。

```bash
# ターミナル
npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin prettier eslint-config-prettier
```

#### Step 4: ESLintとPrettierの設定ファイル作成

プロジェクトルートに`.eslintrc.js`と`.prettierrc.json`を作成します。

```javascript
// .eslintrc.js
module.exports = {
  parser: "@typescript-eslint/parser",
  plugins: ["@typescript-eslint/eslint-plugin"],
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier",
  ],
  root: true,
};
```

```json
// .prettierrc.json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

#### Step 5: `package.json`にスクリプトを追加

`package.json`の`scripts`セクションを編集します。

```json
// package.json
"scripts": {
  "test": "echo \"Error: no test specified\" && exit 1",
  "build": "tsc",
  "lint": "eslint src/**/*.ts",
  "format": "prettier --write src/**/*.ts"
},
```

#### Step 6: 動作確認

ソースコードを置くための`src`ディレクトリを作成し、`index.ts`ファイルを作成します。

```bash
# ターミナル
mkdir src
```

```typescript
// src/index.ts

function greet(name: string): string {
    return `Hello, ${name}!`;
}

const user = 'TypeScript Developer';

console.log(greet(user));
```

それでは、コマンドを実行してみましょう。

1.  **コンパイル:**
    ```bash
    npm run build
    ```
    `dist/index.js`が生成されていることを確認してください。

2.  **実行:**
    ```bash
    node dist/index.js
    ```
    コンソールに`Hello, TypeScript Developer!`と表示されれば成功です。

3.  **リンターとフォーマッターのテスト:**
    `src/index.ts`をわざと汚くしてみます。
    ```typescript
    // src/index.ts (わざと汚くしたコード)
    function greet(name: string): string {
    let unusedVar = 123; // 未使用の変数 (ESLintが警告)
        return `Hello, ${name}!`; // インデントがバラバラ (Prettierが修正)
    }

    const user = "TypeScript Developer"; // ダブルクォート (Prettierが修正)

    console.log(greet(user))
    ```
    -   `npm run lint` を実行すると、`unusedVar`に関する警告が出ます。
    -   `npm run format` を実行すると、コードが`.prettierrc.json`の設定通りに整形されます。

#### Step 7: VS Codeとの連携（推奨）

1.  VS Codeで拡張機能「**ESLint**」と「**Prettier - Code formatter**」をインストールします。
2.  VS Codeの設定（`settings.json`）を開き、以下を追加します。
    ```json
    {
      "editor.formatOnSave": true, // 保存時にフォーマット
      "editor.defaultFormatter": "esbenp.prettier-vscode", // デフォルトフォーマッターをPrettierに
      "editor.codeActionsOnSave": {
        "source.fixAll.eslint": true // 保存時にESLintの修正も適用
      }
    }
    ```
    これで、`.ts`ファイルを保存するたびに、Prettierによる整形とESLintによる自動修正が実行されるようになります。

--- 

✨ **まとめ**

-   TypeScriptプロジェクトの環境構築は、決まった手順に従えば誰でも再現できる定型作業である。
-   `tsconfig.json`, `.eslintrc.js`, `.prettierrc.json`の3つの設定ファイルが、プロジェクトの品質を支える三種の神器となる。
-   `package.json`の`scripts`を活用することで、日々の開発作業を効率化できる。
-   エディタ拡張機能と設定を組み合わせることで、最高の開発体験を手に入れることができる。
