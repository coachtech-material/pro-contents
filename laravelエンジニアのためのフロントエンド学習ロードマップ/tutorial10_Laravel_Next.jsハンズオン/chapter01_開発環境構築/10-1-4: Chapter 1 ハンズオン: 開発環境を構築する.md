# 10-1-4: 実践 🚀 Chapter 1 ハンズオン: 開発環境を構築する

## 🎯 このハンズオンの目的

このチャプターで学んだ手順に従い、Laravel + Next.jsアプリケーション開発のための環境を実際に構築します。すべてのステップを完了すると、バックエンド（Laravel）とフロントエンド（Next.js）それぞれの開発サーバーがローカルで動作している状態になります。

## ハンズオン

### ステップ1: バックエンド（Laravel）のセットアップ

1.  **プロジェクトの作成**
    -   ターミナルを開き、作業用のディレクトリ（例: `~/develop`）に移動します。
    -   以下のコマンドを実行して、`laravel-next-app`という名前のLaravelプロジェクトを作成します。
        ```bash
        curl -s "https://laravel.build/laravel-next-app" | bash
        ```
    -   完了するまで数分待ちます。

2.  **Sailの起動**
    -   作成されたプロジェクトディレクトリに移動します。
        ```bash
        cd laravel-next-app
        ```
    -   Sailをバックグラウンドで起動します。
        ```bash
        ./vendor/bin/sail up -d
        ```
    -   初回はDockerイメージのビルドに時間がかかります。

3.  **動作確認**
    -   ブラウザで `http://localhost` にアクセスし、Laravelのウェルカムページが表示されることを確認してください。

### ステップ2: フロントエンド（Next.js）のセットアップ

1.  **プロジェクトの作成**
    -   ターミナルで、Laravelプロジェクトと同じ階層のディレクトリに戻ります。
        ```bash
        # laravel-next-app ディレクトリから一つ上の階層に移動
        cd ..
        ```
    -   以下のコマンドを実行して、`next-frontend-app`という名前のNext.jsプロジェクトを作成します。
        ```bash
        npx create-next-app@latest
        ```
    -   対話形式の質問には、以下のように回答します。
        -   Project name: `next-frontend-app`
        -   TypeScript: `Yes`
        -   ESLint: `Yes`
        -   Tailwind CSS: `Yes`
        -   `src/` directory: `Yes`
        -   App Router: `Yes`
        -   Default import alias: `No`

2.  **開発サーバーの起動**
    -   作成されたプロジェクトディレクトリに移動します。
        ```bash
        cd next-frontend-app
        ```
    -   開発サーバーを起動します。
        ```bash
        npm run dev
        ```

3.  **動作確認**
    -   ブラウザで `http://localhost:3000` にアクセスし、Next.jsのウェルカムページが表示されることを確認してください。

4.  **初期ページのクリーンアップ**
    -   エディタで `src/app/page.tsx` を開き、内容を以下のように書き換えます。
        ```tsx
        // src/app/page.tsx
        export default function Home() {
          return (
            <main className="flex min-h-screen flex-col items-center justify-center p-24">
              <h1 className="text-4xl font-bold">Hello, Frontend!</h1>
            </main>
          );
        }
        ```
    -   保存後、ブラウザの表示が自動で切り替わることを確認します。

## ✨ まとめ

お疲れ様でした！これで、あなたのローカルマシンには、

-   `http://localhost` で動作するLaravelバックエンド
-   `http://localhost:3000` で動作するNext.jsフロントエンド

の2つの開発環境が整いました。

次のチャプターでは、いよいよこの2つを接続し、Laravelで作成したAPIからデータを取得してNext.jsで表示する、というヘッドレス構成の基本を実装していきます。
