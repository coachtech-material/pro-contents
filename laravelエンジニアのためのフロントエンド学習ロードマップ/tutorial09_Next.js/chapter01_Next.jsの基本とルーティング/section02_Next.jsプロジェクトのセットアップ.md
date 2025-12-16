# Tutorial 9: Next.js

## Chapter 1: Next.jsの基本とルーティング

### Section 2: Next.jsプロジェクトのセットアップ

🎯 **このセクションで学ぶこと**

-   `create-next-app`コマンドを使って、新しいNext.jsプロジェクトをセットアップできるようになる。
-   セットアップ時に尋ねられる各質問の意味を理解し、推奨設定でプロジェクトを作成できるようになる。
-   生成されたプロジェクトの主要なディレクトリとファイルの役割を説明できるようになる。

--- 

### イントロダクション：コマンド一つで始めるモダン開発

Next.jsの素晴らしい点の一つは、複雑な環境構築が不要であることです。ViteがReactのシンプルな開発環境を提供してくれたように、Next.jsは、本番環境を見据えたフルスタックな開発環境を、たった一つのコマンドで構築してくれます。

このコマンドが`create-next-app`です。これを使えば、TypeScript, ESLint, Tailwind CSSといった、現代的な開発に不可欠なツールがすべて設定済みの状態でプロジェクトを開始できます。

--- 

### 🚀 `create-next-app`によるプロジェクト作成

ターミナルを開き、プロジェクトを作成したいディレクトリで以下のコマンドを実行します。

```bash
npx create-next-app@latest
```

すると、対話形式でいくつかの質問が表示されます。推奨される回答は以下の通りです。

```
✔ What is your project named? … my-app
✔ Would you like to use TypeScript? … No / Yes > Yes
✔ Would you like to use ESLint? … No / Yes > Yes
✔ Would you like to use Tailwind CSS? … No / Yes > Yes
✔ Would you like to use `src/` directory? … No / Yes > Yes
✔ Would you like to use App Router? (recommended) … No / Yes > Yes
✔ Would you like to customize the default import alias? … No / Yes > No
```

| 質問 | 推奨 | 理由 |
|:---|:---|:---|
| **Project name?** | 好きな名前 | プロジェクト名になります。 |
| **Use TypeScript?** | **Yes** | 型安全な開発はもはや標準です。 |
| **Use ESLint?** | **Yes** | コードの品質を保つための必須ツールです。 |
| **Use Tailwind CSS?** | **Yes** | ユーティリティファーストのCSSはNext.jsと非常に相性が良いです。 |
| **Use `src/` directory?** | **Yes** | アプリケーションのソースコードを`src`ディレクトリにまとめるのは、一般的な構成で管理しやすくなります。 |
| **Use App Router?** | **Yes (Recommended)** | Next.js 13から導入された新しいルーティング方式です。サーバーコンポーネントなどの新機能を活用でき、今後の主流となります。 |
| **Customize import alias?** | **No** | デフォルトの`@/*`で十分です。後からでも変更できます。 |

すべての質問に答えると、プロジェクトの雛形が作成され、必要なパッケージが自動的にインストールされます。

作成されたプロジェクトディレクトリに移動し、開発サーバーを起動してみましょう。

```bash
cd my-app
npm run dev
```

ブラウザで `http://localhost:3000` を開くと、Next.jsのウェルカムページが表示されます。

--- 

### ⚙️ プロジェクトのディレクトリ構造

`create-next-app`で生成されたプロジェクト（`src`ディレクトリを使用する設定）の主要なファイルとディレクトリの役割を見てみましょう。

```
my-app/
├── src/
│   └── app/
│       ├── favicon.ico
│       ├── globals.css
│       ├── layout.tsx
│       └── page.tsx
├── .eslintrc.json
├── .gitignore
├── next.config.js
├── package.json
├── postcss.config.js
├── tailwind.config.js
└── tsconfig.json
```

#### `src/app` ディレクトリ：最重要エリア

**App Router** を使用する場合、この`app`ディレクトリがアプリケーションの中心となります。ファイルやフォルダを特定のルールで配置することで、ルーティングが自動的に定義されます。

-   **`layout.tsx`**: アプリケーション全体の共通レイアウトを定義するコンポーネントです。HTMLの`<html>`や`<body>`タグはここに記述します。すべてのページで共通のヘッダーやフッターを配置するのに使います。
-   **`page.tsx`**: 特定のルート（この場合はルート`/`）のUIを定義するメインのコンポーネントです。各ページの実体は、この`page.tsx`ファイルになります。
-   **`globals.css`**: アプリケーション全体に適用されるグローバルなCSSファイルです。`layout.tsx`でインポートされています。

#### 設定ファイル群

-   **`next.config.js`**: Next.js自体の動作をカスタマイズするための設定ファイルです。リダイレクトの設定や、外部ドメインの画像を利用する際の設定などをここで行います。
-   **`tailwind.config.js`**: Tailwind CSSのテーマ（色、フォント、ブレークポイントなど）をカスタマイズするための設定ファイルです。
-   **`tsconfig.json`**: TypeScriptのコンパイラオプションを設定するファイルです。
-   **`.eslintrc.json`**: ESLintのルールを設定するファイルです。

これらの設定ファイルは、`create-next-app`によって最適な初期設定がされているため、最初のうちはほとんど触る必要はありません。

--- 

✨ **まとめ**

-   `npx create-next-app@latest`コマンドで、対話的にNext.jsプロジェクトを作成できる。
-   TypeScript, ESLint, Tailwind CSS, `src/`ディレクトリ, App Router を**すべてYes**で進めるのが現代的な推奨設定である。
-   `npm run dev`で開発サーバーを起動できる。
-   **App Router**では、`src/app`ディレクトリ内のファイル構造がそのままURLのルーティングに対応する。
-   `layout.tsx`が全ページの共通レイアウト、`page.tsx`が各ページの本体を定義する。

📝 **学習のポイント**

-   [ ] App Routerではなく、古いPages Routerを選択してプロジェクトを作成した場合、ディレクトリ構造はどのように変わるか調べてみましょう。
-   [ ] `next.config.js`で設定できる項目には、他にどのようなものがあるか公式ドキュメントで確認してみましょう。
-   [ ] `package.json`の`scripts`には、`dev`, `build`, `start`, `lint`の4つのコマンドが定義されています。それぞれのコマンドがどのような役割を持つか説明してください。
