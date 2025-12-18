# 11-3-3: Chapter 3 ハンズオン: コンポーネントカタログを作成する

## 🎯 このセクションで学ぶこと

-   StorybookとPlaywrightを連携させて、ビジュアルリグレッションテスト（VRT）を実装する方法を学ぶ
-   `@storybook/test-runner`を使って、Storybookの全Storyを自動でテストするワークフローを構築する
-   Playwrightの`toHaveScreenshot()`マッチャーを使って、スクリーンショットの差分比較を行う方法を習得する

## 導入

前のセクションで、Storybookを使ってUIコンポーネントのカタログを作成しました。このハンズオンでは、そのカタログを利用して、UIの「見た目」を自動テストする**ビジュアルリグレッションテスト（VRT）**を構築します。

今回は、Storybook公式が提供している`@storybook/test-runner`と、E2Eテストでも使用したPlaywrightを組み合わせてVRTを実現します。このアプローチの利点は、既存のPlaywrightの知識を活かせ、追加のツール（ChromaticやPercyなど）を導入することなくVRTを始められる点です。

## VRTの仕組み

`@storybook/test-runner`は、Storybookに登録されているすべてのStoryを巡回し、各StoryをPlaywrightで開いてテストを実行するためのツールです。

テストの具体的な流れは以下のようになります。

1.  `@storybook/test-runner`がStorybookを内部的にビルドする。
2.  ビルドされたStorybookの各Story（例: `Button--primary`）に対して、Playwrightテストを生成・実行する。
3.  Playwrightは、指定されたStoryのページを開き、`page.screenshot()`または`expect(page).toHaveScreenshot()`を使ってスクリーンショットを撮影する。
4.  **初回実行時**: 撮影したスクリーンショットが「基準（Baseline）画像」として、`__screenshots__`ディレクトリに保存される。
5.  **2回目以降**: 新しく撮影したスクリーンショットと、保存されている基準画像を比較する。
6.  差分がなければテストは成功。差分があればテストは失敗し、差分画像（diff）が生成される。

## セットアップ

### ステップ1: 必要なライブラリのインストール

まず、`@storybook/test-runner`と、PlaywrightをStorybookから利用するための`@storybook/test-playwright`をインストールします。

```bash
npm install -D @storybook/test-runner @storybook/test-playwright
```

### ステップ2: テストスクリプトの追加

`package.json`の`scripts`に、VRTを実行するためのコマンドを追加します。

```json
// package.json
{
  ...
  "scripts": {
    ...
    "test:vrt": "test-storybook"
  },
  ...
}
```

### ステップ3: Playwrightテストファイルの作成

`@storybook/test-runner`が各Storyに対して実行するテストの内容を記述するファイルを作成します。プロジェクトのルートに`test-runner-jest.config.js`（Jestの設定ファイル）と、テストロジックを記述する`vrt.test.js`を作成します。

まず、`test-runner-jest.config.js`を作成します。

```javascript
// test-runner-jest.config.js
const { getJestConfig } = require('@storybook/test-runner');

module.exports = {
  // Storybook test-runnerのデフォルト設定を継承
  ...getJestConfig(),
  // ここで必要に応じて設定を上書きできる
  testMatch: ['**/vrt.test.js'],
};
```

次に、VRTの本体となる`vrt.test.js`を作成します。

```javascript
// vrt.test.js
const { test, expect } = require('@playwright/test');
const { createTestServer } = require('@storybook/test-server');
const { injectAxe, checkA11y } = require('axe-playwright');

let server;

beforeAll(async () => {
  server = await createTestServer();
});

afterAll(async () => {
  await server.close();
});

describe('VRT', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(server.url);
    await injectAxe(page);
  });

  // Storybookの全Storyに対してテストを実行
  server.stories.forEach((story) => {
    test(story.id, async ({ page }) => {
      await page.goto(server.url + '?path=/story/' + story.id);
      // アクセシビリティチェック
      await checkA11y(page, '#storybook-root', {
        detailedReport: true,
        detailedReportOptions: {
          html: true,
        },
      });
      // スクリーンショット比較
      await expect(page).toHaveScreenshot(`${story.id}.png`);
    });
  });
});
```

**コードのポイント:**

-   `createTestServer`: Storybookをビルドし、テスト用のサーバーを起動します。
-   `server.stories`: Storybookに登録されている全StoryのIDと名前のリストです。これをループさせることで、すべてのStoryに対してテストを実行できます。
-   `page.goto(server.url + '?path=/story/' + story.id)`: 各Storyの独立したページ（iframe内ではない）にアクセスします。
-   `checkA11y`: `axe-playwright`によるアクセシビリティチェックです。VRTと同時に行うと効果的です。
-   **`expect(page).toHaveScreenshot(...)`**: Playwrightの強力な機能で、ページのスクリーンショットを撮影し、基準画像との比較を行います。ファイル名を指定するだけで、差分比較のロジック全体を抽象化してくれます。

## VRTの実行

準備が整ったので、VRTを実行してみましょう。

### 初回実行（基準画像の作成）

```bash
npm run test:vrt
```

初回実行時は、比較対象の基準画像が存在しないため、すべてのテストが失敗します。しかし、これにより`__screenshots__`ディレクトリ以下に、現在のコンポーネントの見た目を「正解」とする基準画像が生成されます。

生成された画像を確認し、これが期待通りの見た目であれば、これらの画像をGitにコミットします。

### 2回目以降の実行（差分比較）

では、意図的にコンポーネントの見た目を変更してみましょう。`src/components/ui/Button.tsx`の`primary`バリアントの背景色を`bg-blue-500`から`bg-green-500`に変更します。

```tsx
// ...
variants: {
  variant: {
    primary: "bg-green-500 text-white hover:bg-green-600", // 変更
    // ...
  },
// ...
```

この状態で、再度VRTを実行します。

```bash
npm run test:vrt
```

今度は、`Button--primary`のStoryに対応するテストが失敗するはずです。Playwrightは、`test-results`ディレクトリに差分画像（`diff`）を生成します。これを見ると、どこがどのように変わったのかが一目瞭然です。

![VRTの差分画像](https://raw.githubusercontent.com/coachtech-material/pro-contents/main/laravel%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E3%83%95%E3%83%AD%E3%83%B3%E3%83%88%E3%82%A8%E3%83%B3%E3%83%89%E5%AD%A6%E7%BF%92%E3%83%AD%E3%83%BC%E3%83%89%E3%83%9E%E3%83%83%E3%83%97/images/tutorial-11/vrt-diff.png)

### 基準画像の更新

もしこの変更が意図したものであれば（例: デザイン仕様の変更）、基準画像を更新する必要があります。`--update-snapshots`フラグをつけてテストを実行すると、既存の基準画像が新しいスクリーンショットで上書きされます。

```bash
npm run test:vrt -- --update-snapshots
```

更新された基準画像をGitにコミットすれば、次回のテストからは新しい見た目が「正解」となります。

## ✨ まとめ

-   `@storybook/test-runner`とPlaywrightを組み合わせることで、ローカル環境でVRTを構築できる。
-   `test-runner`がStorybookの全Storyを巡回し、Playwrightで各Storyのスクリーンショットを撮影する。
-   `expect(page).toHaveScreenshot()`を使うことで、スクリーンショットの撮影から差分比較までを簡単に行える。
-   初回実行で「基準画像」を作成し、2回目以降はその基準画像との差分を検出する。
-   意図した変更の場合は、`--update-snapshots`フラグで基準画像を更新する。

これで、ユニットテスト（機能）、E2Eテスト（ユーザーフロー）、そしてビジュアルリグレッションテスト（見た目）という、フロントエンドテストの3つの主要な柱をすべて実践できるようになりました。これらのテストをCI/CDパイプラインに組み込むことで、アプリケーションの品質と開発速度を大幅に向上させることができます。
