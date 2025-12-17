# 6-3-5: 実践 🚀 チャプターハンズオン: ジェネリクスを使った共通部品を作成する

## 🎯 課題

このチャプターで学んだジェネリクス、Union型、型の絞り込みを駆使して、実務でよくある「APIレスポンスを扱う共通関数」を作成しましょう。

多くのWeb APIは、成功時にはデータを、失敗時にはエラー情報を含む、共通のラッパーオブジェクトでレスポンスを返します。今回は、そのような構造を型安全に扱うための部品を作成します。

### 完成要件

1.  **共通のAPIレスポンス型 `ApiResponse<T>` を作成する。**
    -   成功レスポンス `ApiSuccessResponse<T>` と失敗レスポンス `ApiErrorResponse` のUnion型とする。
    -   `ApiSuccessResponse<T>` は、ジェネリクス `T` で受け取ったデータ `data` と、ステータス `status: 'success'` を持つ。
    -   `ApiErrorResponse` は、エラーメッセージ `message` と、ステータス `status: 'error'` を持つ。

2.  **レスポンスを処理する関数 `handleResponse` を作成する。**
    -   この関数は `ApiResponse<T>` を引数に取る。
    -   `status` プロパティを使って型の絞り込みを行う。
    -   ステータスが `'success'` なら、`"Success! Data: "` に続けて `data` の内容をコンソールに出力する。
    -   ステータスが `'error'` なら、`"Error! Message: "` に続けて `message` をコンソールに出力する。

## 🛠️ 手順

1.  **型の定義**: まず、`ApiSuccessResponse<T>` と `ApiErrorResponse` の2つの `interface` (または `type`) を定義します。
2.  **Union型の作成**: `ApiResponse<T>` を、上記2つの型のUnion型として `type` エイリアスで定義します。
3.  **関数の実装**: `handleResponse` 関数をジェネリック関数として実装します。関数の内部で `if` 文を使い、`response.status` の値に応じて処理を分岐させます。
4.  **動作確認**: ユーザーデータと商品データを模したサンプルデータを作成し、`handleResponse` 関数を成功ケースと失敗ケースでそれぞれ呼び出し、期待通りの出力が得られるか確認します。

## 🏆 解答例

```typescript
// 1. 型の定義

// 成功時のレスポンス型。データ部分をジェネリクスTで受け取る
interface ApiSuccessResponse<T> {
  status: 'success';
  data: T;
}

// 失敗時のレスポンス型
interface ApiErrorResponse {
  status: 'error';
  message: string;
}

// 2. Union型の作成
type ApiResponse<T> = ApiSuccessResponse<T> | ApiErrorResponse;

// 3. レスポンスを処理するジェネリック関数の実装
function handleResponse<T>(response: ApiResponse<T>): void {
  // `status`プロパティの値に基づいて型を絞り込む (Discriminated Unions)
  if (response.status === 'success') {
    // このブロック内では、responseは `ApiSuccessResponse<T>` 型として扱われる
    console.log("Success! Data:", response.data);
  } else {
    // このブロック内では、responseは `ApiErrorResponse` 型として扱われる
    console.log("Error! Message:", response.message);
  }
}

// 4. 動作確認

// --- サンプルデータ ---
interface User {
  id: number;
  name: string;
}

interface Product {
  id: string;
  name: string;
  price: number;
}

// --- 成功ケースのシミュレーション ---
const userResponse: ApiResponse<User> = {
  status: 'success',
  data: { id: 1, name: 'Taro Yamada' }
};

const productResponse: ApiResponse<Product> = {
  status: 'success',
  data: { id: 'abc-123', name: 'Laptop', price: 150000 }
};

// --- 失敗ケースのシミュレーション ---
const errorResponse: ApiResponse<never> = { // データがないのでneverを指定
  status: 'error',
  message: 'Could not fetch data from the server.'
};

console.log("--- Handling User Response ---");
handleResponse(userResponse);

console.log("\n--- Handling Product Response ---");
handleResponse(productResponse);

console.log("\n--- Handling Error Response ---");
handleResponse(errorResponse);

/*
--- 期待される出力 ---

--- Handling User Response ---
Success! Data: { id: 1, name: 'Taro Yamada' }

--- Handling Product Response ---
Success! Data: { id: 'abc-123', name: 'Laptop', price: 150000 }

--- Handling Error Response ---
Error! Message: Could not fetch data from the server.

*/
```

### 💡 コードのポイント: Discriminated Unions

このハンズオンで使った `status` プロパティのように、Union型の各メンバーが共通して持つリテラル型（ここでは `'success'` と `'error'`）のプロパティは、**Discriminated Union（判別可能な合併型）** と呼ばれます。これを使うことで、TypeScriptは `if` 文や `switch` 文で非常に効率的かつ確実に型を絞り込むことができます。これは実務で頻繁に使われる、極めて重要なパターンです。
