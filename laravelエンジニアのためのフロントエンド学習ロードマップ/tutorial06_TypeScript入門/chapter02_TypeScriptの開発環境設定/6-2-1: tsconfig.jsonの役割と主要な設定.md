# 6-2-1: tsconfig.jsonの役割と主要な設定

## 🎯 このセクションで学ぶこと

- `tsconfig.json` ファイルがTypeScriptプロジェクトにおいて果たす中心的な役割を理解する
- コンパイラオプションの主要な設定（`target`, `module`, `strict`など）の意味と影響を説明できるようになる
- プロジェクトの要件に合わせて `tsconfig.json` を適切に設定するための基礎知識を習得する

## 導入

TypeScriptプロジェクトを始めると、必ずルートディレクトリに `tsconfig.json` というファイルが存在します。このファイルは、TypeScriptコンパイラ（`tsc`）に対する**設定ファイル**であり、プロジェクト全体の振る舞いを定義する、いわば「**憲法**」のような存在です。

Laravel開発における `composer.json` がパッケージを管理し、`.env` が環境を定義するように、`tsconfig.json` は「どのファイルをコンパイル対象とするか」「どのバージョンのJavaScriptに変換するか」「どれだけ厳格に型チェックを行うか」といった、コンパイルに関するあらゆるルールを定めます。このファイルを理解することは、TypeScriptを使いこなし、堅牢なアプリケーションを構築するための第一歩です。

## 詳細解説

### `tsconfig.json` の役割

`tsconfig.json` ファイルがプロジェクトのルートディレクトリに存在することで、そのディレクトリがTypeScriptプロジェクトのルートであることを示します。主な役割は以下の2つです。

1.  **コンパイル対象のファイルを指定する**: どの `.ts` ファイルをコンパイルし、どのファイルを除外するかを定義します。
2.  **コンパイラオプションを指定する**: TypeScriptコードをJavaScriptコードに変換する際のルールや、型チェックの厳格度などを細かく設定します。

`tsc` コマンドを引数なしで実行すると、カレントディレクトリから親ディレクトリを遡って `tsconfig.json` を探し、その設定に従ってコンパイルが実行されます。

### ⚙️ 主要な設定項目

設定は主に `compilerOptions` オブジェクト内で行います。ここでは、実務で特に重要となる項目を解説します。

| オプション | 設定例 | 説明 |
|:---|:---|:---|
| **`target`** | `"ES2020"`, `"ESNext"` | **どのバージョンのJavaScriptにコンパイルするか**を指定します。新しいバージョンほどモダンな構文が使えますが、古いブラウザのサポートが必要な場合は `ES6` など低いバージョンを指定します。 |
| **`module`** | `"CommonJS"`, `"ESNext"` | **モジュールシステムの種類**を指定します。Node.js環境では `CommonJS`、ブラウザ環境やモダンな開発では `ESNext`（ES Modules）が一般的です。`import/export` 構文の扱いに影響します。 |
| **`strict`** | `true` | **すべての厳格な型チェックオプションを有効にする**メタオプションです。`true` にすることが強く推奨され、TypeScriptの恩恵を最大限に引き出します。（例: `strictNullChecks`, `noImplicitAny` などが含まれます） |
| **`esModuleInterop`** | `true` | CommonJS形式で書かれたモジュールを、ES Modulesの `import` 構文で自然に扱えるようにするための互換性オプションです。`import React from 'react'` のような記述に必要で、ほぼ必須の設定です。 |
| **`jsx`** | `"react-jsx"`, `"preserve"` | JSX（`.tsx` ファイル）の構文をどのように処理するかを指定します。React 17以降では `"react-jsx"` が推奨されます。 |
| **`outDir`** | `"./dist"` | コンパイル後に生成される **JavaScriptファイルの出力先ディレクトリ**を指定します。Laravelでいう `public` ディレクトリのようなイメージです。 |
| **`rootDir`** | `"./src"` | **コンパイル対象のTypeScriptファイルが含まれるルートディレクトリ**を指定します。このディレクトリ内のファイルのみが `outDir` に出力されます。 |

### `include` と `exclude`

`compilerOptions` と同階層で、コンパイルに含めるファイルや除外するファイルを指定できます。

- **`include`**: コンパイル対象に含めるファイルのパターンを配列で指定します。
- **`exclude`**: コンパイル対象から除外するファイルのパターンを配列で指定します。デフォルトでは `node_modules` などが除外されます。

### サンプル `tsconfig.json`

モダンなReactプロジェクトでよく使われる設定例です。

```json
{
  "compilerOptions": {
    /* --- 基本設定 --- */
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["DOM", "DOM.Iterable", "ESNext"],
    "jsx": "react-jsx",

    /* --- 厳格な型チェック --- */
    "strict": true,

    /* --- モジュール解決 --- */
    "moduleResolution": "node",
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,

    /* --- 高度な設定 --- */
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src"], // srcディレクトリ内のファイルのみをコンパイル対象とする
  "exclude": ["node_modules"] // node_modulesはコンパイルから除外する
}
```

## 💡 TIP

- 新しいプロジェクトで `tsconfig.json` を作成するには、ターミナルで `tsc --init` コマンドを実行します。これにより、すべてのオプションがコメント付きで記述された、非常に詳細な設定ファイルが生成されます。最初は圧倒されるかもしれませんが、この中から必要な設定を有効にしていくのが良いでしょう。
- Next.jsやViteなどのフレームワークは、プロジェクト作成時に最適な `tsconfig.json` を自動で生成してくれます。しかし、その設定内容を理解しておくことで、後々のカスタマイズやトラブルシューティングに大いに役立ちます。

## ✨ まとめ

- `tsconfig.json` は、TypeScriptコンパイラ（`tsc`）の挙動を制御する設定ファイルである。
- `compilerOptions` 内で、出力するJavaScriptのバージョン（`target`）、モジュールシステム（`module`）、型チェックの厳格度（`strict`）などを設定する。
- **`"strict": true`** は、TypeScriptの型安全性を最大限に活用するために、現代の開発では必須のオプションである。
- `include` と `exclude` を使うことで、コンパイルの対象範囲を正確にコントロールできる。
