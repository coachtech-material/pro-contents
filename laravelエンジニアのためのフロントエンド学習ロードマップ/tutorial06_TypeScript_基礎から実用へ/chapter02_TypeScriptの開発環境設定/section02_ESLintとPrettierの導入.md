# Tutorial 6: TypeScript 基礎から実用へ

## Chapter 2: TypeScriptの開発環境設定

### Section 2: ESLintとPrettierによるコード品質の向上

🎯 **このセクションで学ぶこと**

-   **リンター (Linter)** と **フォーマッター (Formatter)** の役割の違いを理解する。
-   **ESLint**を導入し、TypeScriptコードの潜在的なバグや非推奨な書き方を静的に解析・警告できるようになる。
-   **Prettier**を導入し、コーディングスタイル（インデント、クォートの種類など）をチーム全体で自動的に統一できるようになる。
-   ESLintとPrettierを連携させ、快適な開発環境を構築する方法を習得する。

--- 

### イントロダクション：コードの「健康診断」と「身だしなみ」

TypeScriptコンパイラ(`tsc`)は、コードの**型**が正しいかどうかをチェックしてくれます。しかし、実際の開発では、型以外の品質も重要になります。

-   使われていない変数が残っている。
-   無限ループになりかねない危険な書き方をしている。
-   人によってインデントがタブだったりスペースだったりして、コードが読みにくい。

このような「型の正しさ」以外の問題を解決してくれるのが、**リンター (Linter)** と **フォーマッター (Formatter)** です。

-   **ESLint (リンター):** コードの潜在的なバグや問題点を指摘する「**健康診断**」の役割を果たします。
-   **Prettier (フォーマッター):** コードの見た目をルールに従って整形する「**身だしなみ**」の役割を果たします。

この2つのツールを組み合わせることで、コードの品質と可読性を飛躍的に向上させることができます。

--- 

### ⚙️ ESLint：コードの静的解析ツール

ESLintは、JavaScriptおよびTypeScriptのコードを静的に解析し、問題のあるパターンを検出して報告するためのツールです。

**ESLintが検出できる問題の例:**
-   未使用の変数
-   到達不能なコード
-   `==` の代わりに `===` を使うべき箇所
-   `async`関数なのに`await`を使っていない

#### インストールと設定

TypeScriptプロジェクトでESLintを使うには、いくつかの関連パッケージをインストールする必要があります。

```bash
# ターミナル
npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

-   `eslint`: ESLint本体。
-   `@typescript-eslint/parser`: ESLintがTypeScriptの構文を理解できるようにするためのパーサー。
-   `@typescript-eslint/eslint-plugin`: TypeScriptに特化したルールセット。

次に、設定ファイル `.eslintrc.js` をプロジェクトのルートに作成します。

```javascript
// .eslintrc.js
module.exports = {
  parser: "@typescript-eslint/parser", // TypeScriptを解析するパーサー
  plugins: ["@typescript-eslint/eslint-plugin"], // TypeScript用のプラグイン
  extends: [
    "eslint:recommended", // ESLintが推奨する基本的なルール
    "plugin:@typescript-eslint/recommended", // TypeScript推奨ルール
  ],
  rules: {
    // ここに個別のルールをカスタマイズできる
    // 例: "no-unused-vars": "warn" // 未使用の変数はエラーではなく警告にする
  },
};
```

`package.json`に`lint`スクリプトを追加すると便利です。

```json
// package.json
{
  "scripts": {
    "lint": "eslint . --ext .ts"
  }
}
```

これで、`npm run lint` を実行すると、プロジェクト内のすべての`.ts`ファイルがチェックされます。

--- 

### ⚙️ Prettier：コードフォーマッター

Prettierは、コードのスタイルに関するあらゆる議論を終わらせるための、強力なコードフォーマッターです。インデントの幅、シングルクォートかダブルクォートか、行末のセミコロンの有無など、コードの見た目に関するすべてを、設定ファイルに従って自動で整形してくれます。

#### インストールと設定

```bash
# ターミナル
npm install --save-dev --save-exact prettier
```

`--save-exact`は、チームメンバー間でPrettierのバージョンを完全に一致させるための推奨オプションです。

設定ファイル `.prettierrc.json` を作成し、好みのスタイルを定義します。

```json
// .prettierrc.json
{
  "semi": true, // 行末にセミコロンを付ける
  "singleQuote": true, // シングルクォートを使う
  "tabWidth": 2, // インデントはスペース2つ
  "trailingComma": "es5" // 末尾のカンマを付ける
}
```

`package.json`に`format`スクリプトを追加します。

```json
// package.json
{
  "scripts": {
    "lint": "eslint . --ext .ts",
    "format": "prettier --write ."
  }
}
```

`npm run format` を実行すると、プロジェクト内のすべてのファイルが自動で整形されます。

--- 

### 🚀 ESLintとPrettierの連携

ESLintにも一部フォーマットに関するルールがあるため、Prettierと競合してしまうことがあります。この競合を避けるため、`eslint-config-prettier`というパッケージを導入します。

```bash
# ターミナル
npm install --save-dev eslint-config-prettier
```

そして、`.eslintrc.js`の`extends`配列の**一番最後**に`"prettier"`を追加します。これにより、Prettierと競合するESLintのルールが無効化されます。

```javascript
// .eslintrc.js
module.exports = {
  // ... (省略)
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier", // 必ず最後に書く！
  ],
  // ... (省略)
};
```

**最終的な役割分担:**
-   **ESLint:** コードの品質やバグのチェックに専念する。
-   **Prettier:** コードの見た目の整形に専念する。

さらに、VS Codeの拡張機能「ESLint」と「Prettier - Code formatter」をインストールし、設定で「保存時に自動でフォーマットする」を有効にすると、ファイルを保存するたびに自動でコードが綺麗になり、非常に快適な開発体験が得られます。

--- 

✨ **まとめ**

-   **ESLint**は、コードの潜在的なバグや問題点をチェックする**リンター**である。
-   **Prettier**は、コードのスタイルを統一する**フォーマッター**である。
-   `@typescript-eslint`関連のパッケージを導入することで、ESLintはTypeScriptコードを解析できるようになる。
-   `eslint-config-prettier`を使い、ESLintとPrettierのルール競合を解消する。
-   これらを組み合わせることで、コードの品質と可読性を自動的に維持し、開発者は本質的なロジックの実装に集中できる。

📝 **学習のポイント**

-   [ ] リンターとフォーマッターの役割の違いを、あなた自身の言葉で説明してください。
-   [ ] なぜESLintとPrettierを連携させる必要があるのでしょうか？
-   [ ] あなたのチームでは、インデントはスペース2つですか、4つですか？ シングルクォート派ですか、ダブルクォート派ですか？ Prettierは、このような「聖戦」をどのように解決しますか？
