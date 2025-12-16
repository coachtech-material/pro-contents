# 6-2-1: TypeScriptコンパイラの導入

## Chapter 2: TypeScriptの開発環境設定

### Section 1: TypeScriptコンパイラの導入と`tsconfig.json`

🎯 **このセクションで学ぶこと**

-   Node.jsとnpmを使って、TypeScriptコンパイラ (`tsc`) をプロジェクトに導入できるようになる。
-   `tsc --init`コマンドを使い、TypeScriptの設定ファイルである`tsconfig.json`を生成できるようになる。
-   `tsconfig.json`の役割と、いくつかの重要な設定項目（`target`, `module`, `strict`）について理解する。

--- 

### イントロダクション：TypeScriptを「実行」できるようにする

前のChapterでは、TypeScriptの基本的な構文を学びました。しかし、書かれたTypeScriptコード (`.ts`ファイル) は、そのままではブラウザやNode.js環境で実行できません。実行するためには、まずJavaScriptコード (`.js`ファイル) に**コンパイル（変換）**する必要があります。

このコンパイル作業を行ってくれるのが、**TypeScriptコンパイラ**、通称`tsc`です。

このセクションでは、`npm`を使って`tsc`をプロジェクトに導入し、その動作を制御するための設定ファイル`tsconfig.json`を作成する方法を学びます。ここが、本格的なTypeScript開発の出発点となります。

--- 

### ⚙️ TypeScriptコンパイラのインストール

TypeScriptコンパイラは、`npm`パッケージとして提供されています。プロジェクトの`devDependencies`（開発時依存）としてインストールするのが一般的です。

まず、プロジェクト用のディレクトリを作成し、`npm`を初期化します。

```bash
# ターミナル
mkdir ts-project
cd ts-project
npm init -y # package.jsonを生成
```

次に、`typescript`パッケージをインストールします。

```bash
# ターミナル
npm install --save-dev typescript
```

インストールが完了すると、`package.json`と`node_modules`ディレクトリが作成されます。`node_modules/.bin/`の中に、TypeScriptコンパイラ本体である`tsc`コマンドが格納されます。

プロジェクト内の`tsc`コマンドを実行するには、`npx tsc`のように`npx`を先頭に付けます。

--- 

### ⚙️ `tsconfig.json`の生成と役割

`tsc`は、**`tsconfig.json`**という名前の設定ファイルを探して、その指示に従ってコンパイル作業を行います。この設定ファイルには、「どの`.ts`ファイルをコンパイル対象とするか」「どのバージョンのJavaScriptに変換するか」「どれくらい厳しく型チェックを行うか」といった、数十ものオプションを記述できます。

`tsconfig.json`の雛形は、以下のコマンドで簡単に生成できます。

```bash
# ターミナル
npx tsc --init
```

これを実行すると、たくさんのオプションがコメントアウトされた状態で記述された`tsconfig.json`ファイルが生成されます。最初は圧倒されるかもしれませんが、重要な項目は限られています。

--- 

### 🚀 `tsconfig.json`の主要なオプション

`compilerOptions`の中に記述する、特に重要な3つのオプションを見ていきましょう。

#### 1. `target`：どのバージョンのJavaScriptに変換するか

`target`は、コンパイル後のJavaScriptのバージョンを指定します。例えば、`"ES2016"`や`"ESNext"`などを指定します。

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2016", // 生成するJSのバージョン
    // ...
  }
}
```

-   **なぜ重要か？** 古いブラウザは新しいJavaScriptの構文（`async/await`など）を理解できないため、幅広い環境をサポートする必要がある場合は、`"ES5"`のような古いバージョンをターゲットに設定します。これにより、TypeScriptコンパイラが自動的に古い構文に変換（トランスパイル）してくれます。
-   モダンなブラウザのみを対象とする場合は、`"ES2020"`や`"ESNext"`を指定すればOKです。

#### 2. `module`：モジュールシステムをどう扱うか

`module`は、`import`/`export`構文を、どのモジュールシステムのコードに変換するかを指定します。

```json
// tsconfig.json
{
  "compilerOptions": {
    "module": "CommonJS", // モジュール解決の方法
    // ...
  }
}
```

-   **`"CommonJS"`**: Node.js環境で標準的に使われる形式 (`require`/`module.exports`)。
-   **`"ESNext"`**: ブラウザで標準のES Modules形式 (`import`/`export`) のまま出力する。
-   **なぜ重要か？** 実行環境（ブラウザなのか、Node.jsなのか）に合わせて適切なモジュール形式を選択しないと、`import`文が正しく解決されず、実行時エラーの原因となります。

#### 3. `strict`：どれくらい厳しくチェックするか

`strict`を`true`に設定すると、TypeScriptが推奨するすべての厳格な型チェックオプションが一括で有効になります。**これは、特別な理由がない限り、必ず`true`に設定するべき最重要オプションです。**

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true, // 厳格な型チェックをすべて有効にする
    // ...
  }
}
```

`strict: true`にすると、以下のようなチェックが有効になります。
-   `null`や`undefined`を許容しない、より安全なコードになる (`strictNullChecks`)。
-   `any`型（何でも入る型、実質的に型チェックを無効にする）を暗黙的に使用することを禁止する (`noImplicitAny`)。

`strict: true`は、TypeScriptのメリットを最大限に引き出すためのスイッチです。新しいプロジェクトでは、必ず最初から有効にしておきましょう。

--- 

✨ **まとめ**

-   TypeScriptコンパイラ (`tsc`) は、`npm install --save-dev typescript`でプロジェクトに導入する。
-   `npx tsc --init`コマンドで、コンパイラの設定ファイルである`tsconfig.json`を生成する。
-   `tsconfig.json`は、コンパイルの挙動を細かく制御するためのファイルである。
-   **`target`**: 出力するJavaScriptのバージョンを指定する。
-   **`module`**: `import`/`export`をどのモジュールシステムに変換するか指定する。
-   **`strict: true`**: TypeScriptの厳格な型チェックを有効にする最重要オプション。必ず`true`に設定する。

📝 **学習のポイント**

-   [ ] `tsc`は、TypeScriptコードを何に変換するためのツールですか？
-   [ ] `tsconfig.json`の役割を説明してください。
-   [ ] `strict: true`に設定すると、どのようなメリットがありますか？
