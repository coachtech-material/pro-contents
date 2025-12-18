# 11-3-2: Storybookの基本

## 🎯 このセクションで学ぶこと

-   Next.jsプロジェクトにStorybookをセットアップする方法を学ぶ
-   Storybookの主要なファイル（`.storybook/main.ts`, `.storybook/preview.ts`）の役割を理解する
-   コンポーネントの「Story」を作成し、Storybook上で表示する方法を習得する

## 導入

前のセクションでは、Storybookの概念と利点について学びました。このセクションでは、実際にNext.jsプロジェクトにStorybookを導入し、最初のStoryを作成するまでの手順をハンズオン形式で進めていきます。

## Storybookのセットアップ

Storybookの導入は、Playwrightと同様に、簡単なコマンドで対話的に行うことができます。Next.jsプロジェクトのルートディレクトリで、以下のコマンドを実行してください。

```bash
npx storybook@latest init
```

このコマンドは、プロジェクトの依存関係（`react`, `next`など）を自動で検出し、最適な設定を対話形式で進めてくれます。基本的にはデフォルトの選択肢のままで問題ありません。

セットアップが完了すると、主に以下の2つのディレクトリと、`package.json`へのスクリプト追加が行われます。

-   `.storybook/`: Storybook自体の設定ファイルを格納するディレクトリ。
-   `src/stories/`: サンプルのコンポーネントとStoryファイルが格納されるディレクトリ。

また、`package.json`の`scripts`には、Storybookを起動・ビルドするためのコマンドが追加されます。

```json
// package.json
{
  ...
  "scripts": {
    ...
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build"
  },
  ...
}
```

## Storybookを起動する

早速、Storybookを起動してみましょう。

```bash
npm run storybook
```

しばらくすると、ブラウザで`http://localhost:6006`が開き、StorybookのUIが表示されます。`src/stories`に自動生成されたサンプルコンポーネントのStoryがいくつか表示されているはずです。

## Storybookの主要な設定ファイル

`.storybook`ディレクトリにある2つの主要な設定ファイルを見てみましょう。

### `.storybook/main.ts`

Storybookのメインの設定ファイルです。どの場所にあるStoryファイルを読み込むか、どのアドオンを利用するかなどを定義します。

```typescript
// .storybook/main.ts

import type { StorybookConfig } from "@storybook/nextjs";

const config: StorybookConfig = {
  // 1. Storyファイルの場所を指定
  stories: ["../src/**/*.mdx", "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"],
  
  // 2. 使用するアドオンを列挙
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@storybook/addon-onboarding",
    "@storybook/addon-interactions",
  ],
  framework: {
    name: "@storybook/nextjs",
    options: {},
  },
  docs: {
    autodocs: "tag",
  },
};
export default config;
```

1.  **`stories`**: Storybookが読み込むファイルのパスをglobパターンで指定します。デフォルトでは、`src`ディレクトリ以下の`.stories.tsx`（または`.mdx`）という名前のファイルを探しに行きます。
2.  **`addons`**: Storybookの機能を拡張するアドオンのリストです。`addon-essentials`には、コンポーネントのpropsを動的に変更できる`Controls`や、コンポーネントの説明書を書ける`Docs`など、基本的な機能が含まれています。

### `.storybook/preview.ts`

すべてのStoryに共通で適用される「プレビュー」の設定を行います。例えば、グローバルなCSSを読み込んだり、Storyを特定のコンポーネントでラップしたりすることができます。

Next.jsでTailwind CSSを使用している場合、`globals.css`をここでインポートする必要があります。

```typescript
// .storybook/preview.ts

import type { Preview } from "@storybook/react";
import "../src/app/globals.css"; // グローバルCSSをインポート

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: "^on[A-Z].*" },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
};

export default preview;
```

## Storyを書いてみよう

それでは、自分たちで作成したコンポーネントのStoryを書いてみましょう。

### ステップ1: コンポーネントの準備

まず、`src/components/ui/Button.tsx`というシンプルなボタンコンポーネントを作成します。

```tsx
// src/components/ui/Button.tsx

import { cva, type VariantProps } from "class-variance-authority";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium",
  {
    variants: {
      variant: {
        primary: "bg-blue-500 text-white hover:bg-blue-600",
        secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300",
        destructive: "bg-red-500 text-white hover:bg-red-600",
      },
      size: {
        sm: "h-9 px-3",
        md: "h-10 px-4 py-2",
        lg: "h-11 px-8",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

const Button = ({ className, variant, size, ...props }: ButtonProps) => {
  return (
    <button
      className={buttonVariants({ variant, size, className })}
      {...props}
    />
  );
};

export { Button };
```

### ステップ2: Storyファイルの作成

次に、この`Button`コンポーネントと同じ階層に`Button.stories.tsx`というファイルを作成します。これが`Button`コンポーネントのStoryファイルになります。

```tsx
// src/components/ui/Button.stories.tsx

import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

// 1. メタデータオブジェクト
const meta: Meta<typeof Button> = {
  title: "UI/Button", // Storybookのサイドバーでの表示名
  component: Button, // 対象のコンポーネント
  tags: ["autodocs"], // Docsタブを自動生成
  argTypes: { // propsの型定義
    variant: {
      control: { type: "radio" },
      options: ["primary", "secondary", "destructive"],
    },
    size: {
      control: { type: "select" },
      options: ["sm", "md", "lg"],
    },
  },
};

export default meta;

type Story = StoryObj<typeof Button>;

// 2. PrimaryボタンのStory
export const Primary: Story = {
  args: {
    variant: "primary",
    children: "Primary Button",
  },
};

// 3. SecondaryボタンのStory
export const Secondary: Story = {
  args: {
    variant: "secondary",
    children: "Secondary Button",
  },
};

// 4. DestructiveボタンのStory
export const Destructive: Story = {
  args: {
    variant: "destructive",
    children: "Destructive Button",
  },
};
```

**コードのポイント:**

1.  **`meta`オブジェクト**: Storyファイルの「メタ情報」を定義します。`title`でStorybook上での階層構造と表示名を決め、`component`で対象コンポーネントを指定します。`argTypes`を設定すると、StorybookのControlsアドオンでpropsをどのように操作するかをカスタマイズできます（例: `radio`ボタンや`select`ドロップダウン）。

2.  **`Story`オブジェクト**: 個々のStory（コンポーネントの特定の状態）を定義します。`export const`でエクスポートされたオブジェクトが、それぞれ一つのStoryになります。

3.  **`args`**: コンポーネントに渡すpropsの値を指定します。`Primary` Storyでは、`variant`に`primary`を、`children`にボタンのテキストを渡しています。

このファイルを作成して保存すると、Storybookが自動でリロードされ、サイドバーに「UI/Button」という項目が追加され、その下に`Primary`, `Secondary`, `Destructive`という3つのStoryが表示されるはずです。

Controlsタブを開けば、`variant`や`size`をGUIで変更して、リアルタイムにコンポーネントの見た目が変わるのを確認できます。

## ✨ まとめ

-   Storybookは`npx storybook@latest init`で簡単にセットアップできる。
-   `.storybook/main.ts`でStoryファイルの場所やアドオンを設定し、`.storybook/preview.ts`でグローバルな設定（CSSのインポートなど）を行う。
-   Storyファイル（`.stories.tsx`）では、`meta`オブジェクトでコンポーネントのメタ情報を定義し、`export const`で個々のStoryを定義する。
-   `args`を使って、各Storyに渡すpropsを指定する。

これで、UIコンポーネントをカタログ化し、様々な状態をインタラクティブに確認する準備が整いました。次のハンズオンでは、このStorybookを使ってビジュアルリグレッションテストをセットアップします。
