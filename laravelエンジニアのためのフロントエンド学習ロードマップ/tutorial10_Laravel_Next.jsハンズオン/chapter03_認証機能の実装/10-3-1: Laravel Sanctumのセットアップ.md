# 10-3-1: Laravel Sanctumのセットアップ

## 🎯 このセクションで学ぶこと

-   Laravel Sanctumとは何か、SPA認証におけるその役割を理解する
-   Sanctumをインストールし、基本的な設定を行う方法を学ぶ
-   認証関連の環境変数を設定し、フロントエンドとの連携準備を整える

## 導入

商品一覧ページが完成しましたが、現状では誰でもAPIにアクセスできてしまいます。実用的なアプリケーションでは、「ログインしているユーザーにだけ特定の操作を許可する」といった認証機能が不可欠です。

LaravelでSPA（Single Page Application）向けの認証を実装する際のデファクトスタンダードとなっているのが、**Laravel Sanctum**です。Sanctumは、Laravelが公式に提供するパッケージで、SPA認証やAPIトークン認証を簡単かつ安全に実装する仕組みを提供します。

このチュートリアルでは、Sanctumの**SPA認証**機能を利用します。これは、従来のWebアプリケーションで使われてきたCookieとセッションを利用した、ステートフルな認証方法です。Next.jsのようなフロントエンドとLaravelバックエンドが異なるドメイン（またはポート）で動作していても、安全に認証状態を維持することができます。

## 詳細解説

**注意**: これ以降のコマンドは、すべてLaravelプロジェクトのディレクトリ（`laravel-next-app`）で、Sailを使って実行します。

### ステップ1: Sanctumのインストール

まず、Composerを使ってSanctumパッケージをインストールします。

```bash
sail composer require laravel/sanctum
```

### ステップ2: 設定ファイルとマイグレーションの発行

次に、`vendor:publish`コマンドを使って、Sanctumの設定ファイル（`config/sanctum.php`）とマイグレーションファイルをプロジェクトにコピーします。

```bash
sail artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
```

### ステップ3: データベースのマイグレーション

Sanctumは、APIトークンを保存するための`personal_access_tokens`テーブルを使用します。ステップ2で発行されたマイグレーションファイルを実行して、このテーブルをデータベースに作成します。

```bash
sail artisan migrate
```

> **補足**: `migrate:fresh`ではなく`migrate`を使っているのは、既存の`products`テーブルのデータを消さずに、新しいマイグレーションだけを適用するためです。

### ステップ4: APIカーネルの設定

次に、フロントエンドからのリクエストに対して、SanctumのSPA認証ミドルウェアが適用されるように設定します。

`app/Http/Kernel.php`を開き、`api`ミドルウェアグループに`EnsureFrontendRequestsAreStateful`クラスを追加します。

```php
// app/Http/Kernel.php

protected $middlewareGroups = [
    // ...
    "api" => [
        \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class, // この行を追加
        "throttle:api",
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],
];
```

このミドルウェアが、フロントエンドからのリクエストをステートフルなものとして扱い、Cookieベースの認証を機能させるための重要な役割を担います。

### ステップ5: 環境変数の設定

最後に、Sanctumとセッションの設定を環境変数で行います。Laravelプロジェクトの`.env`ファイルを開き、以下の点を修正・確認してください。

1.  **`SANCTUM_STATEFUL_DOMAINS`**: どのフロントエンドドメインからのリクエストをステートフルとして扱うかを指定します。今回は`localhost:3000`で動作するNext.jsアプリケーションを対象とします。
2.  **`SESSION_DOMAIN`**: セッションCookieが有効になるドメインを指定します。サブドメインが異なるSPA認証では、これをルートドメイン（今回は`localhost`）に設定することが重要です。
3.  **`SESSION_DRIVER`**: セッションの保存方法。デフォルトの`file`でも動作しますが、`cookie`に設定することで、Laravel側でセッションファイルを管理する必要がなくなり、構成がシンプルになります。

```.env
# .env (Laravelプロジェクトのルート)

# ...

# フロントエンドのURLを指定
SANCTUM_STATEFUL_DOMAINS=localhost:3000

# セッションの設定
SESSION_DRIVER=cookie
SESSION_LIFETIME=120
SESSION_DOMAIN=localhost

# CORSの設定（変更なし）
CORS_ALLOWED_ORIGINS=http://localhost:3000
CORS_SUPPORTS_CREDENTIALS=true # 認証情報（Cookie）の送受信を許可
```

**`CORS_SUPPORTS_CREDENTIALS=true`** を追記するのを忘れないでください。これは、オリジン間でCookieなどの認証情報を含むリクエスト（Credentialed Request）を許可するために不可欠な設定です。

また、対応する`config/cors.php`の設定も確認しておきましょう。

```php
// config/cors.php

// ...
    "supports_credentials" => env("CORS_SUPPORTS_CREDENTIALS", false),
// ...
```

`.env`で`CORS_SUPPORTS_CREDENTIALS`が`true`に設定されることで、この値が`true`になり、`Access-Control-Allow-Credentials`ヘッダーがレスポンスに含まれるようになります。

設定を変更したので、Sailを再起動して反映させます。

```bash
sail down
sail up -d
```

## ✨ まとめ

-   Laravel Sanctumは、SPA認証を簡単かつ安全に実装するための公式パッケージである。
-   `composer require`でインストールし、`vendor:publish`と`migrate`で基本的なセットアップを行う。
-   `app/Http/Kernel.php`の`api`ミドルウェアグループに`EnsureFrontendRequestsAreStateful`を追加する。
-   `.env`ファイルで`SANCTUM_STATEFUL_DOMAINS`と`SESSION_DOMAIN`を正しく設定し、フロントエンドからのステートフルなリクエストを受け入れる準備をする。
-   認証情報（Cookie）を伴うリクエストのために、CORSの設定で`supports_credentials`を`true`にする必要がある。

これで、Laravelバックエンド側で認証リクエストを受け入れる準備が整いました。次のセクションでは、フロントエンドに**NextAuth.js**というライブラリを導入し、このSanctumバックエンドと連携してログイン・ログアウト機能を実装していきます。
