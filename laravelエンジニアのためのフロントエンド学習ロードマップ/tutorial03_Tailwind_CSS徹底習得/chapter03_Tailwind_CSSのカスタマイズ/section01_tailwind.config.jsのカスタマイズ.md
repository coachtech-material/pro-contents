# Tutorial 3: Tailwind CSS徹底習得

## Chapter 3: Tailwind CSSのカスタマイズ

### Section 1: tailwind.config.jsのカスタマイズ - 自分だけのデザインシステムを構築する

🖼️ **完成形のイメージ**

このセクションでは、Tailwind CSSの心臓部である`tailwind.config.js`ファイルを編集し、プロジェクト独自のカラーパレットやフォント、スペースの単位を追加する方法を学びます。これにより、Tailwindを単なるユーティリティ集から、プロジェクト専用のデザインシステムへと昇華させることができます。

*ここにスクリーンショットを挿入: `tailwind.config.js`の`theme.extend`セクションに、`primary`という名前のカスタムカラーや、`montserrat`というカスタムフォントが追加されているコード。そして、HTML側で`bg-primary`や`font-montserrat`といったカスタムクラスが使われている様子。*

--- 

🎯 **このセクションで学ぶこと**

このセクションでは、Tailwind CSSをプロジェクトの要件に合わせて拡張する方法を習得します。このセクションを終えると、あなたは以下のことができるようになります。

-   `tailwind.config.js`の`theme`オブジェクトの役割を理解する。
-   `theme.extend`を使って、既存のカラーパレット、フォントファミリー、スペーシングなどを安全に拡張（追加）できるようになる。
-   プロジェクトのブランドカラーなどをカスタムカラーとして登録し、`bg-primary`や`text-primary`のような意味的なクラス名で利用できるようになる。

--- 

### 導入

Tailwind CSSが提供するデフォルトのカラーパレットやフォントスケールは非常に優れていますが、実際のプロジェクトでは、特定のブランドカラーや、デザインカンプで指定された独自のフォント、余白のルールを使いたい場面が必ず出てきます。`tailwind.config.js`は、まさにそのためのカスタマイズ機能を提供します。このファイルを編集することで、Tailwindのデフォルト設定を上書きしたり、新しい設定を追加したりして、プロジェクトに最適化された「自分だけのTailwind」を作り上げることができます。

### 詳細解説

カスタマイズは、`tailwind.config.js`ファイル内の`theme`オブジェクトに対して行います。`theme`オブジェクトには、`colors`, `fontFamily`, `spacing`など、Tailwindのすべてのデザイン定義（デザイントークン）が含まれています。

#### `theme` vs `theme.extend`

カスタマイズには2つの方法があります。

1.  **`theme`オブジェクトを直接編集する:**
    -   `theme`直下のキー（例: `theme.colors`）を編集すると、Tailwindの**デフォルト設定を完全に上書き**します。例えば、`colors`を上書きすると、`red-500`や`blue-500`といったデフォルトの色は一切使えなくなります。
    -   独自のデザインシステムをゼロから構築する場合以外は、あまり推奨されません。

2.  **`theme.extend`オブジェクトを編集する:**
    -   `theme.extend`内のキー（例: `theme.extend.colors`）を編集すると、Tailwindの**デフォルト設定を維持したまま、新しい設定を追加・拡張**できます。
    -   ほとんどの場合、こちらの方法を使うのが安全でベストプラクティスです。

#### 具体的なカスタマイズ例

##### 1. カラーパレットの拡張

プロジェクトのブランドカラーを`primary`, `secondary`として追加してみましょう。

-   **コード (tailwind.config.js):**
    ```javascript
    module.exports = {
      // ...
      theme: {
        extend: {
          colors: {
            'primary': '#FF6347', // トマト色
            'secondary': {
              'light': '#87CEFA', // ライトスカイブルー
              'DEFAULT': '#4682B4', // スチールブルー
              'dark': '#2E5A80',
            },
          },
        },
      },
      // ...
    }
    ```
-   **コードリーディング:**
    -   `theme.extend.colors`オブジェクト内に、新しいキーを追加します。
    -   `primary`のように単一の色を登録すると、`bg-primary`, `text-primary`, `border-primary`といったクラスが自動的に生成されます。
    -   `secondary`のようにオブジェクトで複数の濃淡を登録すると、`bg-secondary-light`, `text-secondary-dark`のようにアクセスできます。`DEFAULT`キーに指定した色は、`bg-secondary`のように濃淡を指定しない場合のデフォルト値として使われます。

##### 2. フォントファミリーの追加

Google Fontsなどから読み込んだカスタムフォントを追加します。

-   **コード (tailwind.config.js):**
    ```javascript
    const defaultTheme = require('tailwindcss/defaultTheme')

    module.exports = {
      // ...
      theme: {
        extend: {
          fontFamily: {
            sans: ['Montserrat', ...defaultTheme.fontFamily.sans],
          },
        },
      },
      // ...
    }
    ```
-   **コードリーディング:**
    -   `fontFamily`を拡張する場合、既存のフォント設定（`sans`, `serif`, `mono`）を完全に置き換えるのではなく、先頭に新しいフォントを追加し、その後ろにデフォルトのフォントをフォールバックとして連結するのが一般的です。
    -   `require('tailwindcss/defaultTheme')`でデフォルトのテーマ設定を読み込み、スプレッド構文 (`...`) を使って既存の`sans`フォント配列を展開しています。
    -   これにより、`font-sans`クラスを使った際に、まず`Montserrat`フォントが適用され、それが利用できない環境ではデフォルトのサンセリフフォントが適用されるようになります。

### 💡 TIP

-   **設定変更後はビルドを再実行:** `tailwind.config.js`ファイルを変更した場合、Tailwindのビルドプロセス（`npm run watch`など）を一度停止し、再実行しないと変更が反映されないことがあります。設定がうまく反映されない場合は、まずビルドプロセスを再起動してみてください。
-   **プラグイン:** Tailwindには、タイポグラフィのデフォルトスタイルを美しく整える`@tailwindcss/typography`や、フォーム要素のスタイルをリセットする`@tailwindcss/forms`など、公式のプラグインが多数用意されています。これらを`plugins`配列に追加することで、Tailwindの機能をさらに拡張できます。

### ✨ まとめ

-   Tailwind CSSのカスタマイズは、`tailwind.config.js`の`theme`オブジェクトで行う。
-   デフォルト設定を維持しつつ安全に拡張するには、`theme.extend`オブジェクトを使用するのがベストプラクティスである。
-   `extend.colors`でプロジェクト独自のカラーパレットを定義し、`bg-primary`のような意味的なクラス名を作成できる。
-   `extend.fontFamily`でカスタムフォントを追加し、既存のフォントスタックに組み込むことができる。

### 📝 学習のポイント

-   [ ] `theme`と`theme.extend`の違いは何か、どちらを優先的に使うべきか説明できるか？
-   [ ] `tailwind.config.js`で、`#00AABB`という色の`accent`という名前のカスタムカラーを登録するためのコードを書けるか？
-   [ ] `tailwind.config.js`を変更した後に、まず何をすべきか？
