# 6-1-5: Chapter 1 ハンズオン: TypeScriptで関数を書く

## 🎯 このハンズオンの目的

このハンズオンでは、TypeScriptの基本的な型を使って、型安全な関数を作成します。実際にコードを書きながら、型の恩恵を体験しましょう。

## 準備

まず、TypeScriptを実行できる環境を準備します。

```bash
# プロジェクトディレクトリを作成
mkdir ts-practice && cd ts-practice

# package.jsonを初期化
npm init -y

# TypeScriptをインストール
npm install typescript ts-node --save-dev

# tsconfig.jsonを生成
npx tsc --init
```

## 課題1: ユーザー情報を表示する関数

ユーザー情報を受け取り、フォーマットされた文字列を返す関数を作成してください。

### 要件

1. `User`インターフェースを定義する（name: string, age: number, email?: string）
2. `formatUser`関数を作成し、ユーザー情報を整形して返す
3. emailが存在する場合のみ、メールアドレスを含める

### 解答例

`src/user.ts`ファイルを作成し、以下のコードを記述します。

```typescript
// User インターフェースの定義
interface User {
  name: string;
  age: number;
  email?: string; // オプショナル
}

// ユーザー情報をフォーマットする関数
function formatUser(user: User): string {
  let result = `名前: ${user.name}, 年齢: ${user.age}歳`;
  
  if (user.email) {
    result += `, メール: ${user.email}`;
  }
  
  return result;
}

// テスト
const user1: User = { name: "田中太郎", age: 25 };
const user2: User = { name: "鈴木花子", age: 30, email: "hanako@example.com" };

console.log(formatUser(user1)); // 名前: 田中太郎, 年齢: 25歳
console.log(formatUser(user2)); // 名前: 鈴木花子, 年齢: 30歳, メール: hanako@example.com
```

実行してみましょう。

```bash
npx ts-node src/user.ts
```

## 課題2: 配列を操作する関数

数値の配列を受け取り、様々な計算結果を返す関数を作成してください。

### 要件

1. `calculateStats`関数を作成する
2. 引数として数値の配列を受け取る
3. 戻り値として、合計、平均、最大値、最小値を含むオブジェクトを返す

### 解答例

`src/stats.ts`ファイルを作成します。

```typescript
// 統計情報の型定義
interface Stats {
  sum: number;
  average: number;
  max: number;
  min: number;
}

// 統計情報を計算する関数
function calculateStats(numbers: number[]): Stats {
  if (numbers.length === 0) {
    return { sum: 0, average: 0, max: 0, min: 0 };
  }

  const sum = numbers.reduce((acc, num) => acc + num, 0);
  const average = sum / numbers.length;
  const max = Math.max(...numbers);
  const min = Math.min(...numbers);

  return { sum, average, max, min };
}

// テスト
const scores: number[] = [85, 90, 78, 92, 88];
const result = calculateStats(scores);

console.log(`合計: ${result.sum}`);       // 合計: 433
console.log(`平均: ${result.average}`);   // 平均: 86.6
console.log(`最大: ${result.max}`);       // 最大: 92
console.log(`最小: ${result.min}`);       // 最小: 78
```

## 課題3: 商品の合計金額を計算する関数

商品リストを受け取り、合計金額を計算する関数を作成してください。

### 要件

1. `Product`インターフェースを定義する（name: string, price: number, quantity: number）
2. `calculateTotal`関数を作成し、商品リストの合計金額を返す
3. 税率（デフォルト10%）を引数で受け取れるようにする

### 解答例

`src/product.ts`ファイルを作成します。

```typescript
// 商品の型定義
interface Product {
  name: string;
  price: number;
  quantity: number;
}

// 合計金額を計算する関数（税率はデフォルト10%）
function calculateTotal(products: Product[], taxRate: number = 0.1): number {
  const subtotal = products.reduce((acc, product) => {
    return acc + product.price * product.quantity;
  }, 0);

  const total = subtotal * (1 + taxRate);
  return Math.floor(total); // 小数点以下切り捨て
}

// テスト
const cart: Product[] = [
  { name: "TypeScript入門書", price: 2980, quantity: 1 },
  { name: "プログラミングノート", price: 500, quantity: 3 },
  { name: "マウスパッド", price: 1200, quantity: 1 }
];

console.log(`合計金額（税込）: ${calculateTotal(cart)}円`); // 合計金額（税込）: 6578円
console.log(`合計金額（税率8%）: ${calculateTotal(cart, 0.08)}円`); // 合計金額（税率8%）: 6458円
```

## ✨ まとめ

このハンズオンでは、以下のことを実践しました。

- `interface`を使ったオブジェクトの型定義
- オプショナルプロパティ（`?`）の活用
- 配列の型定義と操作
- 関数の引数と戻り値の型指定
- デフォルト引数の使用

TypeScriptの型システムにより、関数の使い方が明確になり、間違った使い方をするとコンパイル時にエラーが検出されることを体験できたと思います。

次のチャプターでは、TypeScriptの開発環境設定について学んでいきましょう。
