# Tutorial 11: 品質保証とチーム開発

## Chapter 1: テストの基礎

### Chapter 1 ハンズオン: はじめてのユニットテストとコンポーネントテスト

🎯 **このハンズオンで達成すること**

-   Laravel (Pest) でシンプルなクラスのユニットテストを書き、実行できるようになる。
-   Next.js (Jest + RTL) でReactコンポーネントのテストを書き、実行できるようになる。
-   バックエンドとフロントエンド、両方のテストサイクルの基本を体験する。

--- 

🖼️ **完成イメージ**

このハンズオンでは、具体的なUIの変更はありません。代わりに、ターミナル上でテストが成功（パス）することを確認します。緑色の「PASS」という文字が、あなたの書いたコードが正しく動作していることの証明です。

**Laravel (Pest) の実行結果イメージ:**
```
   PASS  Tests\Unit\CalculatorTest
  ✓ it adds two numbers correctly

  Tests:  1 passed
```

**Next.js (Jest) の実行結果イメージ:**
```
 PASS  src/components/__tests__/Greeting.test.tsx
  Greeting Component
    ✓ renders a greeting message

Test Suites: 1 passed, 1 total
Tests:       1 passed, 1 total
```

--- 

### Part 1: Laravel (Pest) でのユニットテスト

#### 🧠 先輩エンジニアの思考プロセス

「簡単な計算クラスのテストを書いて」と言われたら、こう考える。

1.  **テスト対象の特定:** まず、テストしたいのは何か？ `Calculator`クラスの`add`メソッドだな。
2.  **テストファイルの作成:** `artisan`コマンドを使うのが定石だ。`php artisan make:test CalculatorTest --unit`で、`tests/Unit`にファイルを作成する。
3.  **テストケースの設計:** `add`メソッドが正しく動くことをどう確認するか？
    -   正の数同士の足し算: `1 + 2 = 3`
    -   負の数を含む足し算: `-1 + 5 = 4`
    -   ゼロとの足し算: `0 + 10 = 10`
    よし、まずは一番シンプルな「正の数同士」のケースからテストを書こう。
4.  **テストの実装 (Arrange-Act-Assert):**
    -   **Arrange:** `Calculator`クラスのインスタンスを作成する。
    -   **Act:** `add(1, 2)`を呼び出す。
    -   **Assert:** 結果が`3`であることを`expect()`で表明する。`expect($result)->toBe(3)`だな。
5.  **テストの実行:** `php artisan test --filter CalculatorTest`で、今書いたテストだけを実行して、素早く結果を確認する。パスすればOK！

--- 

#### 🏃 実践: Step by Stepで実装しよう

##### Step 1: テスト対象のクラスを作成

まず、簡単な計算を行う`Calculator`クラスを`app/Services`ディレクトリに作成します。（ディレクトリがなければ作成してください）

```php
// app/Services/Calculator.php

namespace App\Services;

class Calculator
{
    public function add(int $a, int $b): int
    {
        return $a + $b;
    }
}
```

##### Step 2: テストファイルの作成

`artisan`コマンドでユニットテストファイルを生成します。

```bash
php artisan make:test CalculatorTest --unit
```

`tests/Unit/CalculatorTest.php`が作成されます。

##### Step 3: テストの記述

作成されたテストファイルを以下のように編集します。

```php
<?php

// tests/Unit/CalculatorTest.php

use App\Services\Calculator;

test("it adds two numbers correctly", function () {
    // Arrange: テストの準備
    $calculator = new Calculator();

    // Act: テスト対象の実行
    $result = $calculator->add(2, 3);

    // Assert: 結果の表明
    expect($result)->toBe(5);
});
```

##### Step 4: テストの実行

ターミナルでテストを実行します。

```bash
# すべてのテストを実行
php artisan test

# CalculatorTestだけを実行
php artisan test --filter CalculatorTest
```

ターミナルにテストがパスしたことが表示されれば成功です。

--- 

### Part 2: Next.js (Jest + RTL) でのコンポーネントテスト

#### 🧠 先輩エンジニアの思考プロセス

「挨拶メッセージを表示するコンポーネントのテストを書いて」と言われたら、こう考える。

1.  **テスト対象の特定:** `Greeting`コンポーネントだな。`name`というpropを受け取って、「Hello, {name}!」と表示するシンプルなやつだ。
2.  **テストファイルの作成:** コンポーネントと同じ階層に`__tests__`ディレクトリを作って、その中に`Greeting.test.tsx`という名前で作成するのが一般的だ。
3.  **テストケースの設計:** このコンポーネントが正しく動くことをどう確認するか？
    -   `name` propを渡したときに、その名前を含んだ挨拶が表示されること。これだけで十分だろう。
4.  **テストの実装 (Render-Query-Assert):**
    -   **Render:** `render(<Greeting name="Alice" />)`でコンポーネントを描画する。
    -   **Query:** `screen`オブジェクトを使って、表示された要素を取得する。`getByText`で「Hello, Alice!」というテキストを探すのが一番簡単で、ユーザーの視点に近いな。`screen.getByText(/hello, alice/i)`のように正規表現で、大文字小文字を無視するように書くのが堅牢だ。
    -   **Assert:** 取得した要素がちゃんとドキュメント内に存在することを`expect(element).toBeInTheDocument()`で表明する。
5.  **テストの実行:** `npm test`を実行して結果を確認。パスすればOK！

--- 

#### 🏃 実践: Step by Stepで実装しよう

##### Step 1: テスト環境のセットアップ

（このハンズオンでは、すでにJestとRTLがセットアップされていることを前提とします。セットアップがまだの場合は、Section 3の手順に従ってください。）

##### Step 2: テスト対象のコンポーネントを作成

`src/components`ディレクトリに`Greeting.tsx`を作成します。

```tsx
// src/components/Greeting.tsx

import React from "react";

interface GreetingProps {
  name: string;
}

export const Greeting = ({ name }: GreetingProps) => {
  return <h1>Hello, {name}!</h1>;
};
```

##### Step 3: テストファイルの作成

`src/components`ディレクトリ内に`__tests__`ディレクトリを作成し、さらにその中に`Greeting.test.tsx`を作成します。

```tsx
// src/components/__tests__/Greeting.test.tsx

import { render, screen } from "@testing-library/react";
import { Greeting } from "../Greeting";

describe("Greeting Component", () => {
  it("renders a greeting message with the provided name", () => {
    // Render: コンポーネントを描画
    render(<Greeting name="Bob" />);

    // Query: 画面から要素を取得
    const greetingElement = screen.getByText(/hello, bob/i);

    // Assert: 要素が存在することを表明
    expect(greetingElement).toBeInTheDocument();
  });
});
```

##### Step 4: テストの実行

ターミナルでテストを実行します。

```bash
npm test
```

テストがパスし、`Greeting.test.tsx`が成功したことが表示されれば完了です。

--- 

✨ **まとめ**

-   Laravel (Pest) では、`artisan`でテストファイルを作成し、`test()`と`expect()`を使ってシンプルにユニットテストを記述した。
-   Next.js (Jest + RTL) では、`render`でコンポーネントを描画し、`screen`オブジェクトを使ってユーザーの視点に近い形で要素をクエリし、表明を行った。

このハンズオンを通じて、バックエンドとフロントエンド、それぞれの環境でテストを書く基本的な流れを体験しました。これが、品質の高いアプリケーションを構築するための第一歩です。
