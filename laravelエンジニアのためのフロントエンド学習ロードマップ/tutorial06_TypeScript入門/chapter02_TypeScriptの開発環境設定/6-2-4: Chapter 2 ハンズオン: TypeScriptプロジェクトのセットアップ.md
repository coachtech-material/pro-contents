# 6-2-4: Chapter 2 ハンズオン: TypeScriptプロジェクトのセットアップ

## 🎯 このハンズオンの目的

このハンズオンでは、実際のプロジェクトで使えるTypeScript開発環境を一から構築します。tsconfig.json、ESLint、Prettierを設定し、型安全で品質の高いコードを書くための基盤を整えましょう。

## Step 1: プロジェクトの初期化

まず、新しいプロジェクトを作成します。

```bash
# プロジェクトディレクトリを作成
mkdir my-ts-project && cd my-ts-project

# package.jsonを初期化
npm init -y

# TypeScriptをインストール
npm install typescript --save-dev

# tsconfig.jsonを生成
npx tsc --init
```

## Step 2: tsconfig.jsonの設定

生成された`tsconfig.json`を以下のように編集します。

```json
{
  "compilerOptions": {
    // 基本設定
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "node",
    "esModuleInterop": true,

    // 厳格な型チェック
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noImplicitReturns": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,

    // 出力設定
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,

    // その他
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## Step 3: ESLintの設定

ESLintをインストールし、設定ファイルを作成します。

```bash
# ESLintと関連パッケージをインストール
npm install eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin --save-dev
```

`.eslintrc.js`ファイルを作成します。

```javascript
module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
    project: './tsconfig.json'
  },
  plugins: ['@typescript-eslint'],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-requiring-type-checking'
  ],
  rules: {
    // カスタムルール
    '@typescript-eslint/explicit-function-return-type': 'warn',
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/no-explicit-any': 'error'
  },
  ignorePatterns: ['dist/', 'node_modules/']
};
```

## Step 4: Prettierの設定

Prettierをインストールし、設定ファイルを作成します。

```bash
# Prettierと競合を防ぐパッケージをインストール
npm install prettier eslint-config-prettier --save-dev
```

`.prettierrc`ファイルを作成します。

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```

`.eslintrc.js`の`extends`配列の最後に`prettier`を追加します。

```javascript
extends: [
  'eslint:recommended',
  'plugin:@typescript-eslint/recommended',
  'plugin:@typescript-eslint/recommended-requiring-type-checking',
  'prettier' // 追加
],
```

## Step 5: package.jsonにスクリプトを追加

`package.json`にビルドとリントのスクリプトを追加します。

```json
{
  "scripts": {
    "build": "tsc",
    "lint": "eslint src/**/*.ts",
    "lint:fix": "eslint src/**/*.ts --fix",
    "format": "prettier --write src/**/*.ts"
  }
}
```

## Step 6: サンプルコードの作成

`src`ディレクトリを作成し、サンプルコードを書いてみましょう。

```bash
mkdir src
```

`src/index.ts`を作成します。

```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

function greetUser(user: User): string {
  return `Hello, ${user.name}! Your email is ${user.email}.`;
}

const user: User = {
  id: 1,
  name: 'Taro',
  email: 'taro@example.com',
};

console.log(greetUser(user));
```

## Step 7: 動作確認

設定が正しく動作するか確認します。

```bash
# リントを実行
npm run lint

# コードをフォーマット
npm run format

# TypeScriptをビルド
npm run build

# ビルド結果を実行
node dist/index.js
```

## Step 8: .envファイルの設定（オプション）

環境変数を使う場合は、`dotenv`パッケージをインストールします。

```bash
npm install dotenv
```

`.env`ファイルを作成します。

```
API_URL=https://api.example.com
API_KEY=your-secret-key
```

`.gitignore`に`.env`を追加します。

```
node_modules/
dist/
.env
```

`src/config.ts`で環境変数を読み込みます。

```typescript
import dotenv from 'dotenv';
dotenv.config();

interface Config {
  apiUrl: string;
  apiKey: string;
}

export const config: Config = {
  apiUrl: process.env.API_URL ?? 'http://localhost:3000',
  apiKey: process.env.API_KEY ?? '',
};
```

## ✨ まとめ

このハンズオンでは、以下の開発環境を構築しました。

- TypeScriptコンパイラ（tsconfig.json）
- ESLintによる静的解析
- Prettierによるコードフォーマット
- 環境変数の管理

この環境をベースに、型安全で品質の高いTypeScriptプロジェクトを開発できます。次のチャプターでは、より高度な型操作について学んでいきましょう。
