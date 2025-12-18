# 11-2-3: Chapter 2 ハンズオン: ログインフォームのテストを書く

## 🎯 このセクションで学ぶこと

-   Playwrightを使って、実際のNext.jsアプリケーションのE2Eテストを作成する方法を学ぶ
-   `getByRole`や`getByLabel`といった、より堅牢なロケーターの選び方を習得する
-   ログイン成功と失敗のシナリオをテストコードとして表現する方法を理解する

## 導入

前のセクションで、Playwrightの基本的な概念と使い方を学びました。このハンズオンでは、Tutorial 10で作成したLaravel + Next.jsアプリケーションのログイン機能を対象に、E2Eテストを実際に書いていきます。

### テストシナリオ

今回は、以下の2つの主要なシナリオをテストします。

1.  **ログイン成功シナリオ**: 正しい認証情報（メールアドレスとパスワード）を入力すると、ホームページにリダイレクトされ、ユーザー名が表示されること。
2.  **ログイン失敗シナリオ**: 間違った認証情報を入力すると、エラーメッセージが表示され、ログインページに留まること。

## ハンズオン: ログイン機能のE2Eテスト

### ステップ1: テストファイルの作成

Playwrightのセットアップ時に作成された`tests`ディレクトリ内に、`login.spec.ts`という新しいテストファイルを作成します。

```typescript
// tests/login.spec.ts

import { test, expect } from "@playwright/test";

// テストをグループ化
test.describe("ログイン機能", () => {
  // 各テストの前にログインページにアクセスする
  test.beforeEach(async ({ page }) => {
    await page.goto("http://localhost:3000/login");
  });

  // ログイン成功のテストケース
  test("正しい認証情報でログインできること", async ({ page }) => {
    // 1. フォームを入力する
    await page.getByLabel("メールアドレス").fill("test@example.com");
    await page.getByLabel("パスワード").fill("password");

    // 2. ログインボタンをクリックする
    await page.getByRole("button", { name: "ログイン" }).click();

    // 3. ホームページにリダイレクトされたことを確認する
    await expect(page).toHaveURL("http://localhost:3000/");

    // 4. ユーザー名が表示されていることを確認する
    await expect(page.getByText("ようこそ, Test Userさん")).toBeVisible();
  });

  // ログイン失敗のテストケース
  test("間違った認証情報ではログインできないこと", async ({ page }) => {
    // 1. フォームに間違った情報を入力する
    await page.getByLabel("メールアドレス").fill("wrong@example.com");
    await page.getByLabel("パスワード").fill("wrongpassword");

    // 2. ログインボタンをクリックする
    await page.getByRole("button", { name: "ログイン" }).click();

    // 3. エラーメッセージが表示されることを確認する
    await expect(
      page.getByText("メールアドレスまたはパスワードが正しくありません。")
    ).toBeVisible();

    // 4. ログインページに留まっていることを確認する
    await expect(page).toHaveURL("http://localhost:3000/login");
  });
});
```

**コードのポイント:**

-   **`test.beforeEach(async ({ page }) => { ... })`**: `describe`ブロック内の各テストケースが実行される**前**に、必ず実行される処理を定義します。ここでは、各テストの開始時にログインページにアクセスするという共通の準備作業を行っています。
-   **`getByLabel(text)`**: `<label>`要素のテキストを使って、関連付けられたフォーム要素（`<input>`など）を特定します。CSSセレクタよりも意味的で、ユーザーの操作に近い方法で要素を選択できるため、より堅牢なテストになります。
-   **`getByRole(role, { name })`**: [ARIA role](https://developer.mozilla.org/ja/docs/Web/Accessibility/ARIA/Roles)に基づいて要素を特定します。例えば、`<button>`は`button`ロールを持ちます。`name`オプションで、ボタンのテキスト（アクセシブルネーム）を指定することで、より正確に要素を特定できます。「`ログイン`という名前の`button`ロールを持つ要素」という意味になります。これも非常に推奨されるロケーターです。
-   **`toHaveURL(url)`**: ページのURLが期待通りであるかを検証します。
-   **`toBeVisible()`**: 要素がページ上で表示されている（非表示ではない）ことを検証します。

### ステップ2: テストの実行

テストを実行する前に、**必ずLaravelとNext.jsの両方の開発サーバーを起動してください**。E2Eテストは、実際に動作しているアプリケーションに対して行われるためです。

-   Laravel: `sail up -d`
-   Next.js: `npm run dev`

両方のサーバーが起動したら、新しいターミナルを開いてE2Eテストを実行します。

```bash
npm run test:e2e
```

テストが実行され、すべてのテストがパスすることを確認します。

```
Running 2 tests using 1 worker

  ✓  tests/login.spec.ts:9:7 › ログイン機能 › 正しい認証情報でログインできること (2s)
  ✓  tests/login.spec.ts:25:7 › ログイン機能 › 間違った認証情報ではログインできないこと (1s)


  2 tests passed (4s)
```

もし特定のテストだけを実行したい場合は、ファイル名を指定します。

```bash
npm run test:e2e tests/login.spec.ts
```

また、`--headed`フラグをつけると、ブラウザが実際に立ち上がり、テストが実行される様子を視覚的に確認できます。

```bash
npm run test:e2e -- --headed
```

### ステップ3: レポートの確認

テスト実行後、`npx playwright show-report`を実行して、HTMLレポートを確認してみましょう。各ステップでの動作や、成功・失敗の詳細を見ることができます。

## ✨ まとめ

-   `test.beforeEach`を使うと、テストケース間の共通の準備作業をまとめることができる。
-   `getByLabel`や`getByRole`といった、ユーザーの操作を模倣したセマンティックなロケーターを使うことで、変更に強いテストを書くことができる。
-   E2Eテストを実行する際は、対象のアプリケーションが起動している必要がある。

これで、アプリケーションの最も重要な機能の一つであるログインフローが、期待通りに動作することを自動で保証できるようになりました。次のチャプターでは、UIの「見た目」をテストするビジュアルリグレッションテストについて学びます。
