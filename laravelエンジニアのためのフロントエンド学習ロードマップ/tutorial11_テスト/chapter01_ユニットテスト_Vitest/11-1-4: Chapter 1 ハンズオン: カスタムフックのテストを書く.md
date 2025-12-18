# 11-1-4: Chapter 1 ハンズオン: カスタムフックのテストを書く

## 🎯 このセクションで学ぶこと

-   Reactのカスタムフックをテストする方法を学ぶ
-   `@testing-library/react`の`renderHook`と`act`の使い方を習得する
-   実際にカウンターフックのユニットテストを作成し、実行する

## 導入

前のセクションでは、純粋関数のテスト方法を学びました。しかし、Reactアプリケーションでは、状態（`useState`）や副作用（`useEffect`）を持つカスタムフックのロジックをテストしたい場面が頻繁にあります。

フックは通常のJavaScript関数とは異なり、Reactコンポーネントの内部でしか呼び出すことができません。では、どうすればフックを単体でテストできるのでしょうか？

ここで登場するのが、**`@testing-library/react`** というライブラリです。このライブラリは、Reactコンポーネントやフックをテストするための便利なユーティリティを提供します。

## `@testing-library/react` のセットアップ

まず、必要なライブラリをインストールします。`@testing-library/react`は、Reactコンポーネントをテスト用の仮想DOMにレンダリングする機能を提供します。また、テスト環境でDOMを扱えるようにするために`jsdom`も必要です。

```bash
npm install -D @testing-library/react jsdom
```

次に、Vitestの設定ファイル `vitest.config.ts` をプロジェクトのルートに作成し、テスト環境として`jsdom`を使用するように設定します。

```typescript
// vitest.config.ts

import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom", // テスト環境としてjsdomを指定
    setupFiles: "./vitest.setup.ts", // セットアップファイルへのパス
  },
});
```

さらに、`vitest.setup.ts` というファイルをプロジェクトルートに作成します。このファイルは、各テストファイルの実行前に一度だけ実行されるファイルで、`@testing-library/jest-dom`から提供されるカスタムマッチャーを`expect`に拡張するために使用します。

```typescript
// vitest.setup.ts

import "@testing-library/jest-dom";
```

`@testing-library/jest-dom`は、DOMの状態を検証するための便利なマッチャー（例: `.toBeInTheDocument()`）を提供します。これもインストールしておきましょう。

```bash
npm install -D @testing-library/jest-dom
```

## ハンズオン: `useCounter`フックのテスト

それでは、Tutorial 8で作成した`useCounter`カスタムフックのユニットテストを書いてみましょう。

### ステップ1: テスト対象のフックの準備

まず、テスト対象となる`useCounter`フックを`src/hooks/useCounter.ts`に作成します。

```typescript
// src/hooks/useCounter.ts

import { useState, useCallback } from "react";

export const useCounter = (initialValue = 0) => {
  const [count, setCount] = useState(initialValue);

  const increment = useCallback(() => setCount((c) => c + 1), []);
  const decrement = useCallback(() => setCount((c) => c - 1), []);

  return { count, increment, decrement };
};
```

### ステップ2: テストファイルの作成

`src/hooks/useCounter.test.ts`を作成し、テストコードを記述します。

```typescript
// src/hooks/useCounter.test.ts

import { describe, it, expect } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useCounter } from "./useCounter";

describe("useCounter", () => {
  it("初期値が正しく設定されること", () => {
    // 1. フックをレンダリング
    const { result } = renderHook(() => useCounter(10));

    // 2. 初期状態を検証
    expect(result.current.count).toBe(10);
  });

  it("incrementを呼び出すとcountが1増えること", () => {
    const { result } = renderHook(() => useCounter());

    // 3. 状態を更新する処理を`act`で囲む
    act(() => {
      result.current.increment();
    });

    // 4. 更新後の状態を検証
    expect(result.current.count).toBe(1);
  });

  it("decrementを呼び出すとcountが1減ること", () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(-1);
  });
});
```

**コードのポイント:**

1.  **`renderHook(() => useCounter(10))`**: `@testing-library/react`が提供する`renderHook`関数は、テスト対象のフックを呼び出し、その結果を返すためのテスト用のコンポーネントを内部で作成・レンダリングします。戻り値の`result`オブジェクトから、フックの現在の戻り値に`result.current`でアクセスできます。

2.  **`expect(result.current.count).toBe(10)`**: `result.current`は`useCounter`フックの戻り値（`{ count, increment, decrement }`）そのものです。そのため、`result.current.count`で現在のカウント値にアクセスし、初期値が正しく設定されているかを検証しています。

3.  **`act(() => { ... })`**: `act`は、Reactの状態更新がすべて完了し、DOMに反映されるのを待つためのユーティリティです。Reactの状態を更新する可能性のある処理（この例では`increment`や`decrement`の呼び出し）は、必ず`act`で囲む必要があります。これを怠ると、「`act`でラップされていない更新があります」という警告が表示され、テストが意図通りに動作しない可能性があります。

4.  **`expect(result.current.count).toBe(1)`**: `act`による状態更新が完了した後、`result.current`は最新のフックの戻り値に更新されています。ここで、カウントが期待通りに変化したかを検証します。

### ステップ3: テストの実行

ターミナルで`npm test`を実行し、テストがすべてパスすることを確認しましょう。

```
 ✓ src/hooks/useCounter.test.ts (3)

 Test Files  1 passed (1)
      Tests  3 passed (3)
   Start at  10:05:00
   Duration  256ms ...
```

`PASS`と表示されれば成功です！

## ✨ まとめ

-   Reactのフックをテストするには、`@testing-library/react`ライブラリを使用する。
-   `renderHook`関数を使って、テスト対象のフックをテスト用のコンポーネント内でレンダリングする。
-   フックの戻り値には`result.current`でアクセスできる。
-   状態を更新する処理は、必ず`act`ユーティリティでラップする。

これで、カスタムフックのロジックを分離し、その振る舞いを保証するユニットテストが書けるようになりました。次のチャプターでは、ユーザー視点でアプリケーション全体をテストする「E2Eテスト」について学びます。
