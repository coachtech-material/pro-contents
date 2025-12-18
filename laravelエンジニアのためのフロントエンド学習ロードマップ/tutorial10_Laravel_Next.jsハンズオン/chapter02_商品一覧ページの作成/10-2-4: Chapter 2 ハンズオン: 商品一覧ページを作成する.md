# 10-2-4: 実践 🚀 Chapter 2 ハンズオン: 商品一覧ページを作成する

## 🎯 このハンズオンの目的

このチャプターで学んだ内容を総動員して、LaravelバックエンドでAPIを作成し、Next.jsフロントエンドからそのAPIを呼び出して商品一覧ページを完成させます。CORSエラーの解決から、取得したデータのUIへの反映まで、一連の流れを自分の手で体験します。

## ハンズオン

### ステップ1: バックエンド（Laravel）の準備

**注意**: コマンドはすべてLaravelプロジェクト（`laravel-next-app`）のルートで、`sail`を使って実行します。

1.  **モデルとマイグレーションの作成**
    ```bash
    sail artisan make:model Product -m
    ```

2.  **マイグレーションファイルの編集**
    -   `database/migrations/..._create_products_table.php`を開き、`up`メソッドを以下のように編集します。
        ```php
        public function up(): void
        {
            Schema::create("products", function (Blueprint $table) {
                $table->id();
                $table->string("name");
                $table->text("description");
                $table->integer("price");
                $table->timestamps();
            });
        }
        ```

3.  **シーダーの作成と編集**
    -   シーダーを作成します。
        ```bash
        sail artisan make:seeder ProductSeeder
        ```
    -   `database/seeders/ProductSeeder.php`の`run`メソッドを編集します。
        ```php
        use App\Models\Product;

        public function run(): void
        {
            Product::factory()->count(10)->create();
        }
        ```
    -   `database/seeders/DatabaseSeeder.php`で`ProductSeeder`を呼び出します。
        ```php
        public function run(): void
        {
            $this->call([ProductSeeder::class]);
        }
        ```

4.  **データベースのマイグレーションとシーディング**
    ```bash
    sail artisan migrate:fresh --seed
    ```

5.  **コントローラーとルートの作成**
    -   APIコントローラーを作成します。
        ```bash
        sail artisan make:controller ProductController --api
        ```
    -   `app/Http/Controllers/ProductController.php`の`index`メソッドを編集します。
        ```php
        use App\Models\Product;

        public function index()
        {
            return response()->json(Product::all());
        }
        ```
    -   `routes/api.php`にルートを追加します。
        ```php
        use App\Http\Controllers\ProductController;

        Route::get("/products", [ProductController::class, "index"]);
        ```

6.  **CORS設定**
    -   Laravelプロジェクトの`.env`ファイルに、Next.jsのURLを追記します。
        ```.env
        # .env
        CORS_ALLOWED_ORIGINS=http://localhost:3000
        ```
    -   設定を反映させるためにSailを再起動します。
        ```bash
        sail down
        sail up -d
        ```

7.  **API動作確認**
    -   ブラウザで`http://localhost/api/products`にアクセスし、JSONデータが表示されることを確認します。

### ステップ2: フロントエンド（Next.js）の実装

**注意**: 作業はNext.jsプロジェクト（`next-frontend-app`）で行います。

1.  **環境変数の設定**
    -   Next.jsプロジェクトのルートに`.env.local`ファイルを作成し、以下を記述します。
        ```.env
        # .env.local
        NEXT_PUBLIC_API_BASE_URL=http://localhost/api
        ```
    -   Next.jsの開発サーバーを再起動します（`Ctrl+C`で停止後、`npm run dev`）。

2.  **商品一覧ページの作成**
    -   `src/app/products/page.tsx`を作成し、以下のコードを貼り付けます。

        ```tsx
        // src/app/products/page.tsx

        interface Product {
          id: number;
          name: string;
          description: string;
          price: number;
          created_at: string;
          updated_at: string;
        }

        async function getProducts(): Promise<Product[]> {
          const url = `${process.env.NEXT_PUBLIC_API_BASE_URL}/products`;
          const res = await fetch(url, { cache: "no-store" });
          if (!res.ok) {
            throw new Error("Failed to fetch products");
          }
          return res.json();
        }

        function ProductCard({ product }: { product: Product }) {
          return (
            <div className="border rounded-lg p-6 shadow-md bg-white">
              <h2 className="text-2xl font-semibold mb-2">{product.name}</h2>
              <p className="text-gray-600 mb-4">{product.description}</p>
              <p className="text-xl font-bold text-right text-gray-800">
                &yen;{product.price.toLocaleString()}
              </p>
            </div>
          );
        }

        export default async function ProductsPage() {
          const products = await getProducts();

          return (
            <main className="container mx-auto p-8 bg-gray-50 min-h-screen">
              <h1 className="text-4xl font-bold mb-10 text-center text-gray-800">
                商品一覧
              </h1>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            </main>
          );
        }
        ```

3.  **最終確認**
    -   ブラウザで`http://localhost:3000/products`にアクセスします。
    -   Laravelのデータベースから取得した商品データが、カード形式で綺麗に表示されていれば、このハンズオンは成功です！

## ✨ まとめ

お疲れ様でした！このハンズオンを通して、以下のことができるようになりました。

-   Laravelで基本的なJSON APIを構築する
-   Next.jsのServer ComponentからAPIを呼び出す
-   CORSエラーを解決する
-   取得したデータをReactコンポーネントとして画面に表示する

これは、Laravel + Next.jsによるヘッドレスアプリケーション開発の最も基本的な、しかし最も重要な流れです。この流れをマスターすれば、あとはAPIの機能を拡張したり、フロントエンドのUIをリッチにしたりと、様々な応用が可能になります。

次のチャプターでは、このアプリケーションにログイン・ログアウトといった「認証機能」を実装していきます。
