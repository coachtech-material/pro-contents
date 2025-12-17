# 5-3-1: try-catchによるエラーハンドリング

## 🎯 このセクションで学ぶこと

- `try...catch` 構文を使って、プログラム実行中に発生するエラーを捕捉し、適切に処理できるようになる
- `async/await` と組み合わせた非同期処理のエラーハンドリング方法を習得する

## 導入

プログラムを書いていると、予期せぬエラーはつきものです。例えば、ネットワーク接続が切れてAPIからデータを取得できなかったり、存在しない変数を参照しようとしたり。エラーが発生したときにプログラムがクラッシュしてしまうのを防ぎ、ユーザーに状況を伝えたり、代替処理を行ったりするのが**エラーハンドリング**です。

このセクションでは、JavaScriptの基本的なエラーハンドリング構文である `try...catch` を学びます。

## 詳細解説

### `try...catch` の基本構文

`try...catch` 構文は、エラーが発生する可能性のあるコードブロックを `try` ブロックで囲み、エラーが発生した場合の処理を `catch` ブロックに記述します。

```javascript
try {
  // エラーが発生する可能性のあるコード
  console.log("tryブロックの処理を開始します");
  
  // 意図的にエラーを発生させる
  undefinedFunction(); 
  
  console.log("この行は実行されません");

} catch (error) {
  // エラーが発生した場合に実行されるコード
  console.error("エラーが発生しました！");
  console.error(error); // 発生したエラーオブジェクト
}

console.log("try...catchブロックの外の処理は続行されます");
```

**実行結果:**
```
tryブロックの処理を開始します
エラーが発生しました！
ReferenceError: undefinedFunction is not defined
    at ...
try...catchブロックの外の処理は続行されます
```

`try` ブロック内でエラーが発生すると、その時点から `try` ブロックの実行は中断され、直ちに `catch` ブロックに処理が移ります。`catch` ブロックは、発生したエラー情報を含む**エラーオブジェクト**を引数として受け取ります。

### `async/await` と `try...catch`

`async/await` を使った非同期処理のエラーハンドリングは、`try...catch` と非常に相性が良いです。`await` したPromiseが `rejected`（失敗）状態になると、`try...catch` はそれを同期的なエラーと同様に捕捉できます。

前のチャプターで作成した `fetch` の例にエラーハンドリングを追加してみましょう。

```javascript
async function fetchUsers() {
  try {
    // 意図的に無効なURLを指定してエラーを発生させる
    const response = await fetch("https://jsonplaceholder.typicode.com/invalid-url");

    // fetchは404のようなHTTPエラーでは例外をスローしない
    // response.okプロパティで成功したかを確認する必要がある
    if (!response.ok) {
      // サーバーからのエラーレスポンスをエラーとして扱う
      throw new Error(`HTTPエラー: ${response.status}`);
    }

    const users = await response.json();
    console.log(users);

  } catch (error) {
    // ネットワークエラーや、throwされたエラーがここで捕捉される
    console.error("データの取得に失敗しました:", error);
  }
}

fetchUsers();
```

この例では、2種類のエラーを捕捉しています。

1.  **ネットワークエラー**: `fetch` 自体が失敗した場合（例: DNS解決に失敗、オフラインなど）。この場合、`await fetch(...)` がPromiseを `rejected` にし、`catch` ブロックが実行されます。
2.  **HTTPエラーステータス**: `fetch` は、サーバーが404（Not Found）や500（Internal Server Error）のようなエラーステータスを返しても、それをネットワークエラーとは見なしません。リクエスト自体は完了しているため、Promiseは `fulfilled` になります。そのため、`response.ok` プロパティ（ステータスコードが200-299の範囲なら `true`）をチェックし、`false` であれば `throw new Error(...)` を使って意図的にエラーを発生させ、`catch` ブロックに処理を移しています。

### `finally` ブロック

`try...catch` には、`finally` ブロックを追加することもできます。`finally` ブロック内のコードは、`try` ブロックでエラーが発生したかどうかに関わらず、**必ず最後に実行されます**。

```javascript
try {
  // ...
} catch (error) {
  // ...
} finally {
  console.log('処理が完了しました');
}
```

ローディング表示を終了させる処理など、成功・失敗にかかわらず実行したい後処理を記述するのに便利です。

## 💡 TIP

- Laravelなどのサーバーサイドフレームワークでは、例外（Exception）を `throw` してエラーを処理するのが一般的です。JavaScriptの `throw` と `try...catch` は、その概念と非常によく似ており、PHPの経験がある方には馴染みやすいでしょう。

## ✨ まとめ

- `try` ブロックにエラーの可能性がある処理を記述する。
- `catch` ブロックでエラーを捕捉し、エラー発生時の処理を記述する。
- `async/await` と組み合わせることで、非同期処理のエラーも同期処理のように捕捉できる。
- `fetch` を使う際は、`response.ok` をチェックしてHTTPエラーステータスをハンドリングすることが重要。
- `finally` ブロックは、エラーの有無にかかわらず最後に必ず実行される。
