# 9-3-4: Hydration Mismatch エラーの倒し方

## 🎯 このセクションで学ぶこと

-   Reactの**Hydration**（ハイドレーション）とは何かを理解する
-   Hydration Mismatchエラーがなぜ発生するのか、その根本原因を学ぶ
-   エラーを引き起こす一般的なパターン（タイムスタンプ、`window`オブジェクトへのアクセスなど）を特定できるようになる
-   `useEffect`を使って、クライアントサイドでのみレンダリングを行うことでエラーを回避する方法を習得する
-   `suppressHydrationWarning` propを使った一時的なエラー抑制方法とその注意点を学ぶ

## 導入

Next.jsやReactのサーバーサイドレンダリング（SSR）を扱っていると、開発者コンソールで一度は目にするであろうエラー、それが**Hydration Mismatch**です。「Text content does not match server-rendered HTML.」や「Warning: Expected server HTML to contain a matching ...」といったメッセージで表示されます。

このエラーは、サーバーが生成したHTMLと、ブラウザ（クライアント）でReactが最初にレンダリングした結果が一致しない場合に発生します。これは、アプリケーションの動作が不安定になったり、予期せぬUIの不整合を引き起こしたりする可能性があるため、無視すべきではありません。

このセクションでは、Hydrationの概念から説き起こし、なぜこのミスマッチが発生するのか、そしてそれを解決するための実践的なテクニックを詳しく解説します。

## 詳細解説

### 🔑 Hydrationとは？

Hydration（日本語で「水分補給」や「水和」）とは、サーバーから送られてきた静的なHTMLに対して、クライアントサイドでJavaScript（React）がイベントハンドラなどをアタッチ（関連付け）し、ページをインタラクティブ（操作可能）にするプロセスのことです。

1.  **サーバー**: Reactコンポーネントをレンダリングし、静的なHTMLを生成してブラウザに送信する。
2.  **クライアント**: ブラウザはまずこの静的なHTMLを表示する。ユーザーはコンテンツを読むことができるが、まだボタンをクリックするなどの操作はできない。
3.  **クライアント (Hydration)**: バックグラウンドでダウンロードされたJavaScript（React）が実行される。Reactはサーバーが生成したHTML構造を元に、仮想DOMを構築し、イベントハンドラ（`onClick`など）を対応するDOM要素に「アタッチ」していく。このプロセスが完了すると、ページは完全にインタラクティブになる。

ReactがHydrationを正しく行うためには、**サーバーが生成したHTMLの構造と、クライアントで最初にレンダリングされるコンポーネントの構造が完全に一致している**必要があります。もしここに不一致があると、ReactはどのDOM要素にどのイベントハンドラをアタッチすればよいか分からなくなり、Hydration Mismatchエラーを発生させるのです。

### なぜミスマッチが起こるのか？

サーバーとクライアントでレンダリング結果が異なる主な原因は、**サーバーとクライアントで利用できる情報が異なる**コンポーネントをレンダリングしようとすることです。

**典型的な原因:**

1.  **タイムスタンプやランダムな値の表示**: `new Date()` や `Math.random()` は、サーバーとクライアントで実行されるタイミングが異なるため、違う値を生成します。

    ```tsx
    function MyComponent() {
      // サーバーとクライアントで値が異なるため、ミスマッチが発生
      return <div>Timestamp: {new Date().toLocaleTimeString()}</div>;
    }
    ```

2.  **`window`や`localStorage`など、ブラウザ固有のAPIへのアクセス**: `window`オブジェクトはサーバーサイドには存在しません。そのため、サーバーレンダリング中（SSR）に直接アクセスしようとするとエラーになるか、クライアントでのみ値が設定されミスマッチを引き起こします。

    ```tsx
    function MyComponent() {
      // サーバーでは`window.innerWidth`は未定義。クライアントでは定義されている。
      const width = typeof window !== "undefined" ? window.innerWidth : 0;
      return <div>Window width: {width}</div>;
    }
    ```

3.  **CSS-in-JSライブラリによるランダムなクラス名**: 一部の古いCSS-in-JSライブラリは、サーバーとクライアントで異なるクラス名を生成することがありました（最近のライブラリでは対策済みが多い）。

4.  **不正なHTML構造**: 例えば、`<table>`の中に`<div>`を置いたり、`<p>`の中に`<div>`をネストしたりすると、ブラウザがHTMLをパースする段階で構造を自動的に修正し、サーバーが意図した構造と異なるDOMツリーを生成してしまうことがあります。

### 解決策

Hydration Mismatchを解決する基本的なアプローチは、「**サーバーとクライアントで結果が異なる可能性のある部分は、クライアントサイドでのみレンダリングする**」ということです。

#### 解決策1: `useEffect` を使う（推奨）

最もクリーンで一般的な解決策は、`useEffect`フックを使うことです。`useEffect`の中身はクライアントサイドでのみ、かつコンポーネントがマウントされた後に実行されます。これにより、サーバーレンダリングの結果には影響を与えずに、クライアントでのみ値を設定・表示することができます。

```tsx
import { useState, useEffect } from "react";

function MyComponent() {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    // コンポーネントがマウントされたら、isClientをtrueに設定
    // これにより、クライアントでのみ再レンダリングがトリガーされる
    setIsClient(true);
  }, []);

  return (
    <div>
      {/* isClientがtrueのとき（=クライアント）のみ、動的な値を表示 */}
      Window width: {isClient ? window.innerWidth : "calculating..."}
    </div>
  );
}
```

このパターンは少し冗長に見えますが、何が起きているかが明確で、Reactのライフサイクルに沿った正しい方法です。カスタムフックとして抽出すると再利用しやすくなります。

```tsx
function useIsClient() {
  const [isClient, setIsClient] = useState(false);
  useEffect(() => { setIsClient(true) }, []);
  return isClient;
}

function MyComponent() {
  const isClient = useIsClient();
  return <div>{isClient ? "Client" : "Server"}</div>;
}
```

#### 解決策2: `suppressHydrationWarning`（一時的な回避策）

Reactは、どうしてもミスマッチが避けられないケース（例: タイムスタンプの表示など）のために、エラーを意図的に抑制するための`suppressHydrationWarning`というpropを提供しています。

```tsx
function MyComponent() {
  // このdiv要素でHydration Mismatchが発生しても、コンソールに警告は出ない
  return (
    <div suppressHydrationWarning={true}>
      Timestamp: {new Date().toLocaleTimeString()}
    </div>
  );
}
```

**注意点:**
-   これはあくまで**警告を非表示にするだけ**であり、根本的な問題を解決するものではありません。
-   ミスマッチは依然として発生しており、パフォーマンスにわずかな影響を与える可能性があります。
-   属性（例: `className`）のミスマッチには機能しません。テキストコンテンツのミスマッチにのみ有効です。
-   多用は禁物です。本当に意図したミスマッチであり、他にクリーンな解決策がない場合にのみ、最後の手段として使用してください。

## ✨ まとめ

-   **Hydration**は、サーバーから送られた静的HTMLにReactがインタラクティブ性を持たせるプロセスである。
-   **Hydration Mismatch**は、サーバーのHTMLとクライアントの初期レンダリング結果が一致しない場合に発生する。
-   主な原因は、`new Date()`や`window`オブジェクトなど、サーバーとクライアントで結果が異なる値やAPIを、最初のレンダリングで使ってしまうこと。
-   最も確実な解決策は、`useEffect`と`useState`を使い、**クライアントサイドでのみ動的なコンテンツをレンダリングする**こと。
-   `suppressHydrationWarning`は、警告を抑制するだけで問題を解決するものではないため、使用は慎重に行うべきである。
-   Hydration Mismatchを正しく理解し、適切に対処することは、安定した堅牢なNext.jsアプリケーションを構築するために不可欠なスキルである。
