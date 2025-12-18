# 11-2-2: Playwrightの基本

## 🎯 このセクションで学ぶこと

-   Playwrightの概要と特徴（クロスブラウザ、高速、高機能）を理解する
-   Playwrightのセットアップ方法と、主要な概念（`test`, `page`, `locator`, `expect`）を学ぶ
-   Playwright Codegenを使って、ブラウザ操作を自動でテストコードに記録する方法を体験する

## 導入

[Playwright](https://playwright.dev/)は、Microsoftが開発するモダンなE2Eテストフレームワークです。信頼性が高く、高速で、豊富な機能を備えていることから、近年急速に人気が高まっています。

### Playwrightの主な特徴

-   **クロスブラウザ対応**: Chromium（Google Chrome, Microsoft Edge）、Firefox、WebKit（Safari）の3つの主要なブラウザエンジンすべてに対応しており、同じテストコードで異なるブラウザでの動作を検証できます。
-   **自動待機（Auto-wait）**: Playwrightの最大の特徴の一つです。要素が表示される、クリック可能になる、といった状態になるまで自動で待機してくれるため、不安定になりがちなE2Eテストを安定して実行できます。`sleep`のような不安定な待機処理をテストコードに書く必要がほとんどありません。
-   **豊富な機能**: スクリーンショット撮影、ビデオ録画、ネットワークのモック、認証状態の保存など、E2Eテストに必要な機能がオールインワンで提供されています。
-   **テストジェネレーター（Codegen）**: ブラウザ上で行った操作を自動で記録し、テストコードを生成してくれる強力なツールです。これにより、テスト作成の生産性が劇的に向上します。

## Playwrightのセットアップ

Playwrightは、簡単なコマンドで対話的にセットアップできます。プロジェクトのルートで以下のコマンドを実行してください。

```bash
npm init playwright@latest
```

すると、いくつか質問されます。基本的にはデフォルトのままで問題ありません。

-   `Where to put your end-to-end tests?` -> `tests` （テストファイルの置き場所）
-   `Add a GitHub Actions workflow?` -> `false` （CI/CDの設定は後で可能）
-   `Install Playwright browsers?` -> `true` （テスト用のブラウザをインストール）

セットアップが完了すると、以下のファイル・ディレクトリが生成されます。

-   `playwright.config.ts`: Playwright全体の設定ファイル。
-   `tests/`: テストファイルを格納するディレクトリ。
-   `tests-examples/`: サンプルのテストファイル。

## Playwrightの主要な概念

Playwrightのテストコードは、Vitestとも似た、`test`と`expect`を使った直感的な構文で記述します。

```typescript
// tests/example.spec.ts

import { test, expect } from "@playwright/test";

test("ホームページにタイトルがあること", async ({ page }) => {
  // 1. ページにアクセス
  await page.goto("https://playwright.dev/");

  // 2. 要素を特定（Locator）
  const title = page.locator(".navbar__inner .navbar__title");

  // 3. アサーション
  await expect(title).toHaveText("Playwright");
});
```

-   **`test(title, callback)`**: テストケースを定義します。Vitestの`it`に相当します。
-   **`page`**: ブラウザのページ（タブ）を操作するためのメインのAPIです。`page.goto()`でURLにアクセスしたり、`page.click()`で要素をクリックしたりします。
-   **`locator(selector)`**: ページ上の要素を特定するための仕組みです。「ロケーター」は、要素を見つけるための指示書のようなものです。CSSセレクタやテキスト、テストIDなど、様々な方法で要素を指定できます。`page.locator()`は、要素が実際に表示されるまで待機する、Playwrightの自動待機機能の心臓部です。
-   **`expect(locator)`**: アサーションを行います。Playwrightの`expect`は、ロケーターを引数に取り、`.toHaveText()`（テキストを持つか）、`.toBeVisible()`（表示されているか）など、E2Eテストに特化したマッチャーを提供します。

## Playwright Codegenを体験しよう

Playwrightの最も強力な機能の一つが**Codegen**です。これを使うと、ブラウザでの操作を記録して、自動でテストコードを生成できます。

以下のコマンドを実行してみてください。

```bash
npx playwright codegen https://tailwindcss.com/docs/installation
```

すると、指定したURLのブラウザウィンドウと、Playwright Inspectorというツールウィンドウが立ち上がります。

1.  ブラウザ上で、検索ボックスをクリックします。
2.  「flexbox」と入力します。
3.  検索結果の「Flexbox & Grid」をクリックします。

すると、Playwright Inspectorのウィンドウに、あなたの操作に対応するテストコードがリアルタイムで生成されていくのが分かります。

![Playwright Codegen](https://raw.githubusercontent.com/coachtech-material/pro-contents/main/laravel%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E3%83%95%E3%83%AD%E3%83%B3%E3%83%88%E3%82%A8%E3%83%B3%E3%83%89%E5%AD%A6%E7%BF%92%E3%83%AD%E3%83%BC%E3%83%89%E3%83%9E%E3%83%83%E3%83%97/images/tutorial-11/playwright-codegen.gif)

生成されたコードはコピーして、自分のテストファイルに貼り付けて利用できます。これにより、複雑な操作のテストコードも素早く作成することができます。

## テストの実行

`package.json`の`scripts`に、Playwright用のコマンドが自動で追加されているはずですが、なければ追加します。

```json
// package.json
{
  ...
  "scripts": {
    ...
    "test:e2e": "playwright test"
  },
  ...
}
```

以下のコマンドでテストを実行します。

```bash
npm run test:e2e
```

デフォルトでは、Chromium, Firefox, WebKitの3つのブラウザで並行してテストが実行されます（ヘッドレスモード）。

テスト結果は、HTMLレポートとして自動生成されます。以下のコマンドでレポートを表示できます。

```bash
npx playwright show-report
```

ブラウザでレポートが開き、各テストの成功/失敗、実行時間、ブラウザごとの結果などをインタラクティブに確認できます。

## ✨ まとめ

-   Playwrightは、クロスブラウザ対応で高機能なE2Eテストフレームワークである。
-   `page`でページを操作し、`locator`で要素を特定し、`expect`でアサーションを行うのが基本的な流れ。
-   Playwrightの自動待機機能により、テストが安定しやすい。
-   `playwright codegen`を使うと、ブラウザ操作を記録してテストコードを自動生成できる。

次のハンズオンでは、これらの知識を使って、実際に自分たちのアプリケーションのログインフォームのE2Eテストを作成します。
