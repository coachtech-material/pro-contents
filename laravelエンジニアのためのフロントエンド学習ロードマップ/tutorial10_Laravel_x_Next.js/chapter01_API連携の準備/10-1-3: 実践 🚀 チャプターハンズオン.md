# Tutorial 10: Laravel × Next.js

## Chapter 1: API連携の準備

### Chapter 1 ハンズオン: 開発環境のセットアップと疎通確認

🎯 **このハンズオンで達成すること**

-   LaravelプロジェクトとNext.jsプロジェクトをローカル環境にセットアップできるようになる。
-   LaravelのCORS設定を行い、Next.jsからのリクエストを受け入れられるようにする。
-   Next.jsに環境変数を設定し、Laravel APIのURLを管理できるようにする。
-   Next.jsからLaravelのテスト用APIを叩き、JSONデータを取得して画面に表示することで、両者の疎通確認を完了させる。

--- 

🖼️ **完成イメージ**

Next.jsで作成したページにアクセスすると、Laravel APIから取得したメッセージが画面に表示されます。これにより、フロントエンドとバックエンドが正しく通信できていることを確認します。

![完成イメージ](https://placehold.jp/800x300.png?text=Next.js%20Page%0A---%0A%0AAPIからのメッセージ:%0AHello%20from%20Laravel!)

--- 

### 🧠 先輩エンジニアの思考プロセス

「LaravelとNext.jsの連携環境を作って」と言われたら、こう考える。

1.  **プロジェクトの準備:**
    -   まず、作業用のディレクトリを作る。その中に`backend`と`frontend`という2つのディレクトリを掘って、それぞれにLaravelとNext.jsのプロジェクトをセットアップするのが管理しやすいな。
2.  **バックエンド（Laravel）の準備:**
    -   `laravel new backend`でプロジェクト作成。
    -   疎通確認用の簡単なAPIエンドポイントを作ろう。`routes/api.php`に`/api/hello`みたいなルートを追加して、JSONを返すようにすればOKだ。
    -   次にCORS設定。Next.jsは`localhost:3000`で動くから、これを許可しないとブラウザに怒られる。`.env`に`FRONTEND_URL=http://localhost:3000`を追加して、`config/cors.php`でそれを読み込むように修正する。認証も後々やるから`supports_credentials`も`true`にしておこう。
    -   `php artisan serve`でLaravelの開発サーバーを起動。`http://localhost:8000/api/hello`にブラウザでアクセスして、JSONが表示されるか確認。
3.  **フロントエンド（Next.js）の準備:**
    -   `create-next-app frontend`でプロジェクト作成。
    -   Laravel APIのURLをどう管理するか？ コードに直書きは絶対ダメ。`.env.local`ファイルを作って、`NEXT_PUBLIC_API_URL=http://localhost:8000`と定義しよう。`NEXT_PUBLIC_`プレフィックスを忘れずに。
    -   トップページ (`src/app/page.tsx`) を編集して、APIを叩く処理を書く。`useEffect`と`useState`を使って、ページが読み込まれたら`fetch`でデータを取得し、Stateに保存して表示する、という流れだ。
    -   `npm run dev`でNext.jsの開発サーバーを起動。
4.  **最終確認（疎通確認）:**
    -   ブラウザで`http://localhost:3000`にアクセスする。
    -   画面に「Hello from Laravel!」と表示されれば成功！
    -   もしCORSエラーが出たら、Laravelの`config/cors.php`の設定や`.env`のURLが正しいか、スペルミスがないか再確認する。ブラウザの開発者コンソールを見れば、エラーの原因が詳しくわかるはずだ。

--- 

### 🏃 実践: Step by Stepで実装しよう

#### Step 1: プロジェクトのセットアップ

まず、作業用のディレクトリを作成し、その中にバックエンドとフロントエンドのプロジェクトを作成します。

```bash
# 作業ディレクトリを作成
mkdir laravel-next-app
cd laravel-next-app

# Laravelプロジェクトを作成
laravel new backend

# Next.jsプロジェクトを作成
npx create-next-app@latest frontend
```

#### Step 2: バックエンド（Laravel）の設定

1.  **テスト用APIの作成**

    `backend/routes/api.php`を開き、以下のルートを追加します。

    ```php
    // backend/routes/api.php

    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Route;

    // ...

    // 疎通確認用のテストAPI
    Route::get("/hello", function () {
        return response()->json(["message" => "Hello from Laravel!"]);
    });
    ```

2.  **CORS設定**

    `backend/.env`ファイルに、フロントエンドのURLを追加します。

    ```env
    # backend/.env

    # ...
    FRONTEND_URL=http://localhost:3000
    ```

    `backend/config/cors.php`を編集します。

    ```php
    // backend/config/cors.php

    // ...
    // allowed_originsを修正
    'allowed_origins' => explode(',', env('FRONTEND_URL', 'http://localhost')),

    // ...
    // supports_credentialsをtrueに修正
    'supports_credentials' => true,

    // ...
    ```

3.  **Laravel開発サーバーの起動**

    ターミナルで`backend`ディレクトリに移動し、開発サーバーを起動します。

    ```bash
    cd backend
    php artisan serve
    ```

    ブラウザで`http://localhost:8000/api/hello`にアクセスし、`{"message":"Hello from Laravel!"}`と表示されることを確認してください。

#### Step 3: フロントエンド（Next.js）の設定

1.  **環境変数の設定**

    `frontend`ディレクトリのルートに`.env.local`ファイルを作成し、以下を記述します。

    ```env
    # frontend/.env.local

    NEXT_PUBLIC_API_URL=http://localhost:8000
    ```

2.  **APIからデータを取得して表示**

    `frontend/src/app/page.tsx`を編集します。クライアントサイドでデータを取得するため、`'use client'`ディレクティブが必要です。

    ```tsx
    // frontend/src/app/page.tsx

    'use client'; // クライアントコンポーネントとして宣言

    import { useState, useEffect } from 'react';

    export default function HomePage() {
      const [message, setMessage] = useState('Loading...');

      useEffect(() => {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL;

        fetch(`${apiUrl}/api/hello`)
          .then((response) => response.json())
          .then((data) => {
            setMessage(data.message);
          })
          .catch((error) => {
            console.error('Error fetching data:', error);
            setMessage('Failed to load message from API.');
          });
      }, []); // 空の依存配列で、コンポーネントのマウント時に一度だけ実行

      return (
        <div>
          <h1 className="text-3xl font-bold mb-4">Welcome to Next.js!</h1>
          <p className="text-xl">APIからのメッセージ: <span className="font-semibold text-blue-600">{message}</span></p>
        </div>
      );
    }
    ```

3.  **Next.js開発サーバーの起動**

    **新しいターミナル**を開き（Laravelのサーバーは起動したまま）、`frontend`ディレクトリに移動して開発サーバーを起動します。

    ```bash
    cd frontend
    npm run dev
    ```

#### Step 4: 疎通確認

ブラウザで`http://localhost:3000`にアクセスしてください。

最初は「Loading...」と表示され、その後すぐに「APIからのメッセージ: **Hello from Laravel!**」と表示されれば、ハンズオンは成功です！

**もしエラーが出たら？**

-   **CORSエラー**: ブラウザの開発者コンソールにCORS関連のエラーメッセージが表示されている場合、Laravelの`config/cors.php`や`.env`の`FRONTEND_URL`が`http://localhost:3000`になっているか、スペルミスがないか確認してください。
-   **404 Not Found**: Laravel APIのURLが間違っている可能性があります。Next.jsの`.env.local`の`NEXT_PUBLIC_API_URL`が`http://localhost:8000`になっているか、Laravelのルートが`/api/hello`で正しいか確認してください。

--- 

✨ **まとめ**

-   LaravelとNext.jsのプロジェクトをそれぞれセットアップし、同時に開発サーバーを起動した。
-   LaravelのCORS設定を正しく行い、Next.jsからのAPIリクエストを許可した。
-   Next.jsの環境変数を使って、APIのURLを安全に管理した。
-   `useEffect`と`fetch`を使って、クライアントサイドでAPIからデータを取得し、画面に表示することに成功した。

これで、2つの強力なフレームワークが連携して動作する、モダンな開発環境の第一歩が踏み出せました。
