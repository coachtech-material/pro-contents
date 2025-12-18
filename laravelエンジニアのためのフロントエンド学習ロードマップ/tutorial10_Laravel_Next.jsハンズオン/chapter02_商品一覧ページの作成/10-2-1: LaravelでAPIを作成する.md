# 10-2-1: LaravelでAPIを作成する

## 🎯 このセクションで学ぶこと

-   LaravelでAPI用のルートを定義する方法を学ぶ
-   マイグレーションを使ってデータベースにテーブルを作成する方法を習得する
-   シーダーを使って、テスト用のダミーデータをデータベースに投入する方法を学ぶ
-   コントローラーを作成し、データベースから取得したデータをJSON形式で返す基本的なAPIロジックを実装する

## 導入

開発環境が整ったので、いよいよアプリケーションの機能を実装していきます。このチャプターでは、Next.jsフロントエンドに表示するための「商品一覧データ」を提供するAPIを、Laravelバックエンドに作成します。

API作成の基本的な流れは以下の通りです。

1.  **データベース準備**: 商品データを保存するためのテーブルをデータベースに作成します（マイグレーション）。
2.  **ダミーデータ投入**: 動作確認用のダミー商品データをテーブルに投入します（シーダー）。
3.  **ルーティング**: `/api/products` のようなAPIのエンドポイント（URL）を定義します。
4.  **コントローラー作成**: リクエストを受け取り、データベースから商品データを取得して、JSON形式でレスポンスを返す処理を記述します。

それでは、ステップバイステップで進めていきましょう。

## 詳細解説

**注意**: これ以降のコマンドは、すべてLaravelプロジェクトのディレクトリ（`laravel-next-app`）で、Sailを使って実行します。`sail`のエイリアスを設定していない場合は、コマンドの先頭に`./vendor/bin/`を付けてください。

### ステップ1: モデルとマイグレーションの作成

まず、商品データを表現するための`Product`モデルと、対応する`products`テーブルを作成するためのマイグレーションファイルを同時に生成します。

```bash
# -mオプションでマイグレーションファイルも同時に作成
sail artisan make:model Product -m
```

このコマンドにより、以下のファイルが生成されます。

-   `app/Models/Product.php` (モデル)
-   `database/migrations/xxxx_xx_xx_xxxxxx_create_products_table.php` (マイグレーションファイル)

次に、マイグレーションファイルを編集して、`products`テーブルのカラムを定義します。`database/migrations/..._create_products_table.php`を開き、`up`メソッドを以下のように修正してください。

```php
// database/migrations/..._create_products_table.php

public function up(): void
{
    Schema::create('products', function (Blueprint $table) {
        $table->id();
        $table->string('name');
        $table->text('description');
        $table->integer('price');
        $table->timestamps();
    });
}
```

### ステップ2: シーダーの作成とダミーデータ投入

次に、`products`テーブルにダミーデータを投入するためのシーダーを作成します。

```bash
sail artisan make:seeder ProductSeeder
```

`database/seeders/ProductSeeder.php`が生成されるので、`run`メソッドを編集して、ダミーデータを10件作成するロジックを記述します。

```php
// database/seeders/ProductSeeder.php

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\Product; // Productモデルをインポート

class ProductSeeder extends Seeder
{
    public function run(): void
    {
        Product::create([
            'name' => '商品A',
            'description' => 'これは商品Aです。高品質な素材を使用しています。',
            'price' => 1000,
        ]);

        Product::create([
            'name' => '商品B',
            'description' => 'これは商品Bです。最新の技術で作られています。',
            'price' => 2500,
        ]);

        // Fakerを使ってランダムなデータを8件追加
        Product::factory()->count(8)->create();
    }
}
```

> **補足**: `Product::factory()` を使うには、対応する`ProductFactory`が必要です。`sail artisan make:factory ProductFactory --model=Product`でファクトリを作成し、`definition`メソッドを定義してください。ここでは簡単のため、手動で2件、ファクトリで8件のデータを作成しています。

作成した`ProductSeeder`を呼び出すために、`database/seeders/DatabaseSeeder.php`を編集します。

```php
// database/seeders/DatabaseSeeder.php

public function run(): void
{
    // \App\Models\User::factory(10)->create();

    $this->call([
        ProductSeeder::class, // ProductSeederを呼び出す
    ]);
}
```

準備ができたので、マイグレーションとシーディングを実行します。`migrate:fresh`コマンドは、すべてのテーブルを一度削除してから再度マイグレーションを実行し、`--seed`オプションでシーダーも実行します。開発中にテーブル構造を頻繁に変更する場合に便利です。

```bash
sail artisan migrate:fresh --seed
```

これで、データベースに`products`テーブルが作成され、10件のダミーデータが投入されました。

### ステップ3: APIルートとコントローラーの作成

次に、APIのエンドポイントを定義します。`routes/api.php`ファイルに、`/products`へのGETリクエストを処理するためのルートを追加します。

```php
// routes/api.php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ProductController; // コントローラーをインポート

// ...

Route::get('/products', [ProductController::class, 'index']);
```

このルートが参照している`ProductController`をまだ作成していないので、`artisan`コマンドで作成します。

```bash
# --apiオプションで、API用の基本的なメソッドが用意されたコントローラーが作成される
sail artisan make:controller ProductController --api
```

`app/Http/Controllers/ProductController.php`が生成されるので、`index`メソッドを編集して、すべての商品データを取得してJSON形式で返すロジックを実装します。

```php
// app/Http/Controllers/ProductController.php

namespace App\Http\Controllers;

use App\Models\Product; // Productモデルをインポート
use Illuminate\Http\Request;

class ProductController extends Controller
{
    public function index()
    {
        // Productモデルを使って、productsテーブルのすべてのレコードを取得
        $products = Product::all();

        // 取得したデータをJSON形式で返す
        return response()->json($products);
    }

    // ... 他のメソッドは今回は使用しない
}
```

### ステップ4: APIの動作確認

以上でAPIの実装は完了です。動作確認をしてみましょう。

ブラウザまたは`curl`コマンドで、`http://localhost/api/products`にアクセスします。

```bash
curl http://localhost/api/products
```

以下のようなJSONデータが返ってくれば成功です。

```json
[
    {
        "id": 1,
        "name": "商品A",
        "description": "これは商品Aです。高品質な素材を使用しています。",
        "price": 1000,
        "created_at": "2023-10-27T12:34:56.000000Z",
        "updated_at": "2023-10-27T12:34:56.000000Z"
    },
    {
        "id": 2,
        "name": "商品B",
        "description": "これは商品Bです。最新の技術で作られています。",
        "price": 2500,
        "created_at": "2023-10-27T12:34:56.000000Z",
        "updated_at": "2023-10-27T12:34:56.000000Z"
    },
    // ... (残りのデータ)
]
```

## ✨ まとめ

-   `make:model`と`make:seeder`コマンドで、モデル、マイグレーション、シーダーを効率的に作成できる。
-   `migrate:fresh --seed`コマンドで、データベースの初期化とデータ投入を一度に行える。
-   `routes/api.php`にルートを定義し、コントローラーのメソッドに処理を紐付ける。
-   コントローラー内でモデルを使ってデータベースからデータを取得し、`response()->json()`でJSONレスポンスを返す。

これで、Next.jsから呼び出すためのバックエンドAPIが準備できました。次のセクションでは、いよいよフロントエンドからこのAPIを呼び出し、取得したデータを画面に表示します。
