# Tutorial 11: 品質保証とチーム開発

## Chapter 1: テストの基礎

### Section 2: Laravelでのユニットテスト (Pest)

🎯 **このセクションで学ぶこと**

-   LaravelのデフォルトのテストフレームワークであるPestの基本的な書き方を習得する。
-   `artisan`コマンドを使って、新しいテストファイルを簡単に作成できるようになる。
-   `test()`関数と`expect()`関数を使って、シンプルなユニットテストを記述できるようになる。
-   インメモリデータベースを設定し、実際のデータベースを汚すことなく高速にテストを実行する方法を理解する。

--- 

### イントロダクション：エレガントなPHPテストフレームワーク Pest

Laravelは、バージョン8から**Pest**というテストフレームワークをデフォルトで採用しています。Pestは、PHPUnitをベースに、よりシンプルで表現力豊かなAPIを提供することを目指して作られました。その文法は、JavaScriptのテストフレームワーク（Jestなど）にインスパイアされており、可読性が高く、書くのが楽しくなるように設計されています。

このセクションでは、Pestを使ってLaravelアプリケーションのユニットテストを書く基本的な方法を学びます。

--- 

### 🚀 はじめてのPestテスト

Laravelプロジェクトには、すでにテストを記述するためのディレクトリと、いくつかのサンプルテストが用意されています。

-   `tests/Feature`: 機能テスト（インテグレーションテストに近い）を配置するディレクトリ。
-   `tests/Unit`: ユニットテストを配置するディレクトリ。

`tests/Unit/ExampleTest.php`を開いてみましょう。

```php
<?php

test("that true is true", function () {
    expect(true)->toBeTrue();
});
```

これがPestの最も基本的なテストの形です。

-   `test("説明文", function() { ... })`: 個々のテストケースを定義します。第一引数には、そのテストが何を検証しているのかを自然言語で記述します。
-   `expect(値)`: テスト対象の値を指定します。これは「期待値」を検証するためのチェーンの始まりです。
-   `->toBeTrue()`: `expect()`に渡された値が`true`であることを表明（アサーション）します。これを**マッチャー**と呼びます。

#### テストの実行

プロジェクトのルートディレクトリで、以下の`artisan`コマンドを実行してみましょう。

```bash
php artisan test
```

コマンドを実行すると、Pestが`tests`ディレクトリ内のすべてのテストを探し出して実行し、結果を表示します。

```
   PASS  Tests\Unit\ExampleTest
  ✓ that true is true

   PASS  Tests\Feature\ExampleTest
  ✓ the application returns a successful response

  Tests:  2 passed
  Time:   0.10s
```

このように、すべてのテストがパスした（成功した）ことがわかります。

--- 

### ⚙️ 新しいテストの作成

`artisan`コマンドを使えば、新しいテストファイルを簡単に生成できます。

```bash
# ユニットテストを作成
php artisan make:test StringUtilsTest --unit

# フィーチャーテストを作成
php artisan make:test PostCreationTest
```

`--unit`オプションを付けると`tests/Unit`に、付けないと`tests/Feature`にファイルが作成されます。

では、`StringUtilsTest`を使って、文字列を操作するシンプルなクラスをテストしてみましょう。

まず、テスト対象のクラスを作成します。

```php
// app/Utils/StringUtils.php

namespace App\Utils;

class StringUtils
{
    public static function toUpperCase(string $str): string
    {
        return strtoupper($str);
    }
}
```

次に、生成された`tests/Unit/StringUtilsTest.php`を編集して、このクラスの`toUpperCase`メソッドをテストします。

```php
<?php

use App\Utils\StringUtils;

test("it converts a string to uppercase", function () {
    // 準備 (Arrange)
    $input = "hello world";

    // 実行 (Act)
    $result = StringUtils::toUpperCase($input);

    // 表明 (Assert)
    expect($result)->toBe("HELLO WORLD");
});
```

このテストは、以下の3つのステップ（**Arrange-Act-Assert** パターン）で構成されています。

1.  **Arrange（準備）**: テストに必要な変数や状態を準備します。（`$input`を定義）
2.  **Act（実行）**: テスト対象のコード（メソッドや関数）を実行します。（`StringUtils::toUpperCase()`を呼び出し）
3.  **Assert（表明）**: 実行結果が期待通りであるかを検証します。（`expect()`で結果を表明）

再度`php artisan test`を実行すると、新しいテストが追加され、パスすることが確認できます。

--- 

### 🧪 データベースのテスト

モデルのテストなど、データベースとの連携が必要なテストを書く場合、ローカルの開発用データベースを直接使うのは避けたいところです。テストを実行するたびにデータが追加・削除され、データベースが汚れてしまうからです。

解決策は、テスト実行時だけ**インメモリデータベース**（SQLiteなど）を使用することです。

`phpunit.xml`ファイル（Pestは内部でPHPUnitを使っているため、この設定ファイルを参照します）を開き、`<php>`セクションを修正します。

```xml
<!-- phpunit.xml -->

<php>
    <env name="APP_ENV" value="testing"/>
    <env name="BCRYPT_ROUNDS" value="4"/>
    <env name="CACHE_DRIVER" value="array"/>
    <!-- <env name="DB_CONNECTION" value="sqlite"/> -->
    <!-- <env name="DB_DATABASE" value=":memory:"/> -->
    <env name="DB_CONNECTION" value="sqlite"/>
    <env name="DB_DATABASE" value=":memory:"/>
    <env name="MAIL_MAILER" value="array"/>
    <env name="QUEUE_CONNECTION" value="sync"/>
    <env name="SESSION_DRIVER" value="array"/>
    <env name="TELESCOPE_ENABLED" value="false"/>
</php>
```

コメントアウトされている`DB_CONNECTION`と`DB_DATABASE`の行を有効にします。

-   `DB_CONNECTION="sqlite"`: データベース接続としてSQLiteを使用する。
-   `DB_DATABASE=":memory:"`: データベースを物理的なファイルとしてではなく、メモリ上に作成する。

これにより、`php artisan test`を実行したときだけ、Laravelは自動的にメモリ上に新しいSQLiteデータベースを構築し、テスト終了後にはそのデータベースは破棄されます。これにより、テストは開発用データベースから完全に隔離され、高速に実行されます。

#### `RefreshDatabase` トレイト

データベースを使用するテストクラスでは、`Illuminate\Foundation\Testing\RefreshDatabase`トレイトを使用するのが一般的です。

```php
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PostCreationTest extends TestCase
{
    use RefreshDatabase; // このトレイトを追加

    public function test_a_post_can_be_created()
    {
        // ...
    }
}
```

このトレイトを追加すると、各テストケースが実行される**前**に、自動的にマイグレーションが実行され、テーブルが再作成されます。これにより、各テストは常にクリーンな状態のデータベースで実行され、他のテストの影響を受けなくなります。

--- 

✨ **まとめ**

-   **Pest**は、Laravelのデフォルトの、可読性が高くエレガントなテストフレームワークである。
-   テストは`php artisan test`コマンドで実行できる。
-   新しいテストファイルは`php artisan make:test`コマンドで生成する。
-   テストケースは`test()`関数で定義し、表明には`expect()`とマッチャー（例: `toBe()`）を使用する。
-   データベースのテストでは、`phpunit.xml`で**インメモリのSQLiteデータベース**を使用するように設定するのがベストプラクティスである。
-   `RefreshDatabase`トレイトを使うと、テストケースごとにデータベースがリセットされ、テストの独立性が保たれる。

📝 **学習のポイント**

-   [ ] `expect()`に用意されているマッチャーには、他にどのようなものがあるか、Pestの公式ドキュメントで調べてみましょう。（例: `toBeNull()`, `toContain()`, `toHaveCount()`など）
-   [ ] `php artisan test --filter <テスト名>` というコマンドを使うと、特定のテストだけを実行できます。その使い方を試してみましょう。
-   [ ] Laravelのモデルファクトリは、テスト用のダミーデータを生成するための非常に強力な機能です。`Post`モデルに対応するファクトリを作成し、それを使ってテスト内でダミーの投稿データを作成する方法を調べてみましょう。
