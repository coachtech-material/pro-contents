# Tutorial 10: Laravel × Next.js

## Chapter 1: API連携の準備

### Section 2: CORSと環境変数の設定

🎯 **このセクションで学ぶこと**

-   CORS（Cross-Origin Resource Sharing）がなぜ必要なのか、その仕組みを説明できるようになる。
-   LaravelでCORSを設定し、特定のドメイン（Next.jsアプリ）からのAPIリクエストを許可する方法を習得する。
-   Next.jsで環境変数を設定し、Laravel APIのURLを安全に管理する方法を理解する。

--- 

### イントロダクション：異なる世界の橋渡し

前セクションで学んだように、LaravelとNext.jsは別々のサーバーで動作します。これは、Webセキュリティの観点から重要な問題を一つ引き起こします。それが**オリジン間リソース共有（CORS）**の問題です。

ブラウザには**同一オリジンポリシー（Same-Origin Policy）**という基本的なセキュリティ原則があります。これは、「あるオリジン（例: `http://localhost:3000`）から読み込まれたスクリプトは、それとは異なるオリジン（例: `http://localhost:8000`）のリソースにアクセスできない」というルールです。

もしこの制約がなければ、悪意のあるサイトが、ユーザーがログインしている銀行サイトのAPIを勝手に叩いて送金する、といった攻撃が可能になってしまいます。

しかし、私たちのアーキテクチャでは、Next.jsアプリ（`http://localhost:3000`）がLaravel API（`http://localhost:8000`）にアクセスする必要があり、これはまさにオリジンを越えたリクエストです。この正当なリクエストを許可するために、サーバー側（Laravel）で「このオリジンからのリクエストは安全ですよ」と明示的に許可する仕組みが**CORS**です。

--- 

### ⚙️ LaravelでのCORS設定

幸いなことに、LaravelにはCORSを処理するための便利なミドルウェアが標準で組み込まれています。設定は非常に簡単です。

#### 1. `config/cors.php`の確認

まず、`config/cors.php`という設定ファイルを開いてみましょう。このファイルで、CORSに関する挙動を細かく制御できます。

```php
// config/cors.php

return [
    // ...

    'paths' => ['api/*', 'sanctum/csrf-cookie'],

    'allowed_methods' => ['*'],

    'allowed_origins' => ['*'],

    'allowed_origins_patterns' => [],

    'allowed_headers' => ['*'],

    // ...
];
```

#### 2. 許可するオリジンの設定

最も重要な設定は`allowed_origins`です。ここに、APIへのアクセスを許可するフロントエンドのオリジン（URL）を指定します。

開発中は、Next.jsの開発サーバーが`http://localhost:3000`で動作しています。これを許可リストに追加しましょう。

`.env`ファイルを開き、以下の変数を追加します。

```env
# .env (Laravelプロジェクトのルート)

# ...

# フロントエンドのURLを環境変数として定義
# カンマ区切りで複数指定も可能
FRONTEND_URL="http://localhost:3000"
```

次に、`config/cors.php`がこの環境変数を読み込むように修正します。

```php
// config/cors.php

return [
    // ...

    // allowed_originsの値を環境変数から取得するように変更
    'allowed_origins' => explode(',', env('FRONTEND_URL', 'http://localhost')),

    // ...
];
```

-   `env('FRONTEND_URL', 'http://localhost')`: `.env`ファイルから`FRONTEND_URL`の値を取得します。もし変数が存在しない場合は、デフォルト値として`http://localhost`を使用します。
-   `explode(',', ...)`: カンマ区切りで複数のURLが指定された場合、それらを配列に分割します。

**なぜハードコーディングしないのか？**
本番環境では、フロントエンドのURLは`https://www.your-app.com`のようなドメインになります。環境変数を使うことで、コードを変更することなく、開発環境と本番環境で異なるURLを柔軟に設定できます。

#### 3. `supports_credentials`の設定

後のチュートリアルで扱う認証（Cookieを使ったセッション管理）を行うためには、`supports_credentials`を`true`に設定する必要があります。これにより、オリジンを越えたリクエストでCookieの送受信が可能になります。

```php
// config/cors.php

return [
    // ...

    'supports_credentials' => true,

];
```

これでLaravel側の設定は完了です。Laravelは、`FRONTEND_URL`で指定されたオリジンからのAPIリクエストに対して、適切なCORSヘッダー（`Access-Control-Allow-Origin`など）を自動的にレスポンスに付与してくれるようになります。

--- 

### 🚀 Next.jsでの環境変数の設定

次に、Next.js側で、接続先であるLaravel APIのURLを管理する方法を設定します。

ここでも、URLをコード内に直接書き込む（ハードコーディングする）のは避けるべきです。APIのURLも、開発環境と本番環境では異なるためです。

Next.jsでは、プロジェクトのルートに`.env.local`というファイルを作成することで、環境変数を定義できます。

#### 1. `.env.local`の作成

Next.jsプロジェクトのルートディレクトリに`.env.local`ファイルを作成します。

```
my-next-app/
├── .env.local  // このファイルを作成
├── src/
├── package.json
└── ...
```

#### 2. 環境変数の定義

`.env.local`ファイルに、Laravel APIのURLを定義します。Next.jsでブラウザ側にも公開される環境変数を定義する場合、変数名のプレフィックスとして**`NEXT_PUBLIC_`**を付ける必要があります。これは、誤ってサーバーサイドの秘密鍵などをブラウザに公開してしまうのを防ぐためのセキュリティ機能です。

```env
# .env.local (Next.jsプロジェクトのルート)

# Laravel APIのベースURL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### 3. 環境変数の利用

これで、アプリケーション内のどこからでも`process.env.NEXT_PUBLIC_API_URL`として、この値にアクセスできます。

例えば、APIからデータを取得する`fetch`リクエストは以下のようになります。

```tsx
// 例: APIから記事を取得する関数

async function getPosts() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const response = await fetch(`${apiUrl}/api/posts`);
  const data = await response.json();
  return data;
}
```

`.env.local`ファイルは、通常`.gitignore`に含まれており、Gitリポジトリにはコミットされません。これにより、各開発者が自分のローカル環境に合わせた設定を使ったり、本番環境のURLが漏洩したりするのを防ぎます。

--- 

✨ **まとめ**

-   ブラウザの**同一オリジンポリシー**により、異なるオリジン間のリソースアクセスはデフォルトで禁止されている。
-   **CORS**は、サーバー側（Laravel）が特定のオリジン（Next.js）からのリクエストを安全に許可するための仕組みである。
-   Laravelでは、`config/cors.php`と`.env`ファイルを編集して、`allowed_origins`にフロントエンドのURLを設定する。
-   Next.jsでは、`.env.local`ファイルに環境変数を定義する。
-   ブラウザで利用する環境変数には、**`NEXT_PUBLIC_`**というプレフィックスを付ける必要がある。

📝 **学習のポイント**

-   [ ] もしLaravelのCORS設定で`allowed_origins`を`["*"]`（ワイルドカード）に設定した場合、どのようなセキュリティ上のリスクが考えられますか？
-   [ ] Next.jsで`NEXT_PUBLIC_`プレフィックスを付けずに定義した環境変数は、どこでならアクセスできるでしょうか？（ヒント: サーバーコンポーネントとクライアントコンポーネント）
-   [ ] CORSエラーが発生したとき、ブラウザの開発者コンソールの「コンソール」タブと「ネットワーク」タブには、それぞれどのような情報が表示されるか調べてみましょう。これはデバッグに非常に役立ちます。
