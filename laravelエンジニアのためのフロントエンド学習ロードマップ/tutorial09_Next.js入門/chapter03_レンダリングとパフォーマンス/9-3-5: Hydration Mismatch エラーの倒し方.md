
# 9-3-5: Hydration Mismatch エラーの倒し方

## 🎯 この章で学ぶこと

- Hydration Mismatchエラーがなぜ発生するのか、その根本原因を理解する。
- エラーを引き起こす一般的なシナリオを学ぶ。
- エラーをデバッグし、解決するための具体的なテクニックを習得する。
- エラーを未然に防ぐためのベストプラクティスを理解する。

## はじめに

Next.jsや他のSSRフレームワークを使っていると、多くの開発者が一度は遭遇するであろう厄介なエラー、それが「Hydration Mismatch」です。コンソールに表示される`"Text content does not match server-rendered HTML."`や`"Hydration failed because the initial UI does not match what was rendered on the server."`といった警告は、アプリケーションのパフォーマンスを低下させるだけでなく、予期せぬUIの不具合を引き起こす可能性もあります。

この章では、このハイドレーションミスマッチエラーの正体を解き明かし、その原因を特定し、そして解決するための実践的な「倒し方」を伝授します。

## Hydration Mismatchとは何か？

ハイドレーションとは、サーバーサイドでレンダリングされた静的なHTMLに、クライアントサイドでダウンロードしたJavaScriptがイベントリスナーなどをアタッチして、ページをインタラクティブにするプロセスのことでした。

このとき、Reactは**「サーバーから送られてきたHTMLの構造」**と**「クライアントで最初のレンダリングを行った結果生成されるべきDOMの構造」**が完全に一致していることを期待します。もし、この2つの間に少しでも食い違いがあると、Reactはどちらを信じてよいか分からなくなり、ハイドレーションミスマッチエラーを発生させるのです。[1]

エラーが発生すると、Reactは信頼できないサーバーのHTMLを破棄し、クライアントサイドでDOMツリー全体を再レンダリングしようとします。これは、SSR/SSGによるパフォーマンス向上のメリットを帳消しにしてしまうため、絶対に避けるべきです。

## エラーが発生する一般的な原因と解決策

Hydration Mismatchは、サーバーとクライアントでレンダリング結果が異なるあらゆる状況で発生する可能性があります。以下に代表的な原因と、その解決策を示します。

### 1. タイムゾーンやロケールに依存する日時の表示

-   **原因**: サーバー（例: UTC）とクライアント（例: JST）のタイムゾーンが異なる場合、`new Date().toLocaleString()`のようなコードは異なる結果を生成します。
-   **解決策**: 常にクライアントサイドでのみレンダリングするようにします。`useEffect`内で値を設定するか、`suppressHydrationWarning`属性を使う（非推奨）、またはクライアントコンポーネントに切り出して動的インポート（`ssr: false`）を利用します。

    ```jsx
    "use client";
    import { useState, useEffect } from 'react';

    export function ClientTime() {
      const [time, setTime] = useState("");

      useEffect(() => {
        // useEffectはクライアントでのみ実行される
        setTime(new Date().toLocaleTimeString());
      }, []);

      // 初回レンダリングではtimeは空文字列なので、サーバーと一致する
      return <span>{time}</span>;
    }
    ```

### 2. `window`や`localStorage`などのブラウザAPIの使用

-   **原因**: サーバーサイドには`window`や`localStorage`といったブラウザ固有のオブジェクトは存在しません。これらを使って条件分岐などをすると、サーバーとクライアントで異なるUIが生成されます。
-   **解決策**: 原因1と同様に、`useEffect`を使ってクライアントサイドでのみこれらのAPIにアクセスするようにします。

    ```jsx
    "use client";
    import { useState, useEffect } from 'react';

    function getTheme() {
      if (typeof window !== "undefined") {
        return localStorage.getItem('theme') || 'light';
      }
      return 'light'; // サーバーではデフォルト値を返す
    }

    export function ThemeSwitcher() {
      const [theme, setTheme] = useState('light');

      useEffect(() => {
        setTheme(getTheme());
      }, []);

      // ...
    }
    ```

### 3. 不適切なHTML構造

-   **原因**: 例えば、`<p>`タグの中に`<div>`タグを入れるなど、HTMLの仕様として正しくないネスト構造があると、ブラウザがレンダリング時にDOMを自動的に修正することがあります。この修正結果が、サーバーが生成したHTMLと食い違いを生みます。
-   **解決策**: HTMLの構造を正しく修正します。W3Cのバリデーターなどでチェックするのも有効です。

    ```jsx
    // NG: <p>の中に<div>
    <p><div>Hello</div></p>

    // OK: <div>の中に<p>
    <div><p>Hello</p></div>
    ```

### 4. CSSによる表示の差異

-   **原因**: `display: none`などを利用したレスポンシブデザインで、サーバー（モバイルサイズを想定）とクライアント（デスクトップサイズ）で表示される要素が異なる場合。
-   **解決策**: CSSだけで表示/非表示を切り替えるのが最も安全です。もしコンポーネント自体を出し分けたい場合は、`useEffect`と`window.matchMedia`を組み合わせて、クライアントサイドでのみ出し分けの判断を行います。

### 5. ライブラリの利用

-   **原因**: 内部でユニークIDを生成するようなサードパーティライブラリが、サーバーとクライアントで異なるIDを生成してしまう場合。
-   **解決策**: 多くのUIライブラリは、Next.jsのようなSSR環境で安全に動作するためのAPIを提供しています（例: `id`をpropsで渡すなど）。ライブラリのドキュメントを確認しましょう。それが不可能な場合は、そのライブラリを使ったコンポーネントを`next/dynamic`で`ssr: false`オプション付きで読み込むのが最終手段です。

## デバッグのヒント

-   **エラーメッセージを読む**: Next.js 13.1以降、エラーメッセージが改善され、どの要素でミスマッチが起きているかのヒントが表示されるようになりました。
-   **HTMLを比較する**: ブラウザの「ページのソースを表示」でサーバーが生成したHTMLを確認し、開発者ツールの「要素」タブでクライアントがレンダリングしたDOMと比較します。
-   **`suppressHydrationWarning`属性**: どうしても避けられないミスマッチ（例: タイムスタンプなど）がある場合、最終手段として要素に`suppressHydrationWarning={true}`を追加することで、警告を抑制できます。ただし、これは根本的な解決ではなく、多用は避けるべきです。[2]

## ✨ まとめ

-   Hydration Mismatchは、**サーバーのHTML**と**クライアントの初回レンダリング結果**が食い違うことで発生する。
-   主な原因は、**環境依存のAPI**（日時、`window`）、**不正なHTML**、**レスポンシブデザインの不適切な実装**など。
-   解決の基本戦略は、**「初回レンダリングではサーバーとクライアントの実行結果が必ず同じになるようにする」**こと。
-   `useEffect`を使って、クライアントサイドでのみ実行したい処理をカプセル化するのが最も一般的な解決策。
-   `next/dynamic`と`ssr: false`は、クライアントサイドでのみ動作させたいコンポーネントを切り離すための強力な武器となる。

このエラーを正しく理解し、恐れずに対処できるようになることは、Next.jsを使いこなす上で非常に重要なスキルです。

---

## 参考文献

[1] React Documentation. (n.d.). *hydrateRoot*. Retrieved from https://react.dev/reference/react-dom/client/hydrateRoot#handling-hydration-errors
[2] React Documentation. (n.d.). *suppressHydrationWarning*. Retrieved from https://react.dev/reference/react-dom/client/hydrateRoot#suppressing-hydration-warnings
