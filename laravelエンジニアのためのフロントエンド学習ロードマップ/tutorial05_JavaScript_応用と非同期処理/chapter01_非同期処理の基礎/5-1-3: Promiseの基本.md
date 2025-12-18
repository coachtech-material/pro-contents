# 5-1-3: Promiseの基本

## 🎯 このセクションで学ぶこと

- Promiseの基本概念を理解する
- `then`, `catch`, `finally` の使い方を学ぶ
- Promiseチェーンで複数の非同期処理を連結する方法を学ぶ

## はじめに

前のセクションで、コールバック関数を使った非同期処理は「コールバック地獄」になりやすいという問題を見ました。Promiseは、この問題を解決するためにES6で導入された機能です。Promiseを使うと、非同期処理をより読みやすく、管理しやすく書けるようになります。

## 1. Promiseとは

Promiseは、「将来のある時点で結果が得られる処理」を表すオブジェクトです。Promiseには3つの状態があります。

| 状態 | 説明 |
|------|------|
| pending（保留中） | 処理がまだ完了していない |
| fulfilled（成功） | 処理が成功して結果が得られた |
| rejected（失敗） | 処理が失敗してエラーが発生した |

## 2. Promiseの基本的な使い方

### Promiseの作成

```javascript
const promise = new Promise((resolve, reject) => {
  // 非同期処理
  setTimeout(() => {
    const success = true;
    
    if (success) {
      resolve("成功しました！"); // 成功時
    } else {
      reject("エラーが発生しました"); // 失敗時
    }
  }, 1000);
});
```

### then, catch, finally

```javascript
promise
  .then((result) => {
    // 成功時の処理
    console.log(result); // "成功しました！"
  })
  .catch((error) => {
    // 失敗時の処理
    console.error(error);
  })
  .finally(() => {
    // 成功・失敗に関わらず実行される処理
    console.log("処理完了");
  });
```

## 3. 実践的な例: データ取得

```javascript
// データを取得する関数（Promiseを返す）
function fetchUser(userId) {
  return new Promise((resolve, reject) => {
    console.log(`ユーザー ${userId} のデータを取得中...`);
    
    setTimeout(() => {
      // 成功をシミュレート
      if (userId > 0) {
        resolve({
          id: userId,
          name: "山田太郎",
          email: "yamada@example.com"
        });
      } else {
        reject("無効なユーザーIDです");
      }
    }, 1500);
  });
}

// 使用例
fetchUser(1)
  .then((user) => {
    console.log("ユーザー情報:", user);
  })
  .catch((error) => {
    console.error("エラー:", error);
  });

// 出力:
// ユーザー 1 のデータを取得中...
// （1.5秒後）
// ユーザー情報: { id: 1, name: "山田太郎", email: "yamada@example.com" }
```

## 4. Promiseチェーン

`then`の中で新しいPromiseを返すと、処理を連結できます。これを「Promiseチェーン」と呼びます。

```javascript
// 複数の関数を定義
function fetchUser(userId) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ id: userId, name: "山田太郎" });
    }, 1000);
  });
}

function fetchPosts(userId) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { id: 1, title: "最初の投稿" },
        { id: 2, title: "2番目の投稿" }
      ]);
    }, 1000);
  });
}

function fetchComments(postId) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { id: 1, text: "素晴らしい！" },
        { id: 2, text: "参考になりました" }
      ]);
    }, 1000);
  });
}

// Promiseチェーンで連結
fetchUser(1)
  .then((user) => {
    console.log("ユーザー:", user.name);
    return fetchPosts(user.id);
  })
  .then((posts) => {
    console.log("投稿数:", posts.length);
    return fetchComments(posts[0].id);
  })
  .then((comments) => {
    console.log("コメント数:", comments.length);
  })
  .catch((error) => {
    console.error("エラー:", error);
  });

// 出力（各1秒間隔）:
// ユーザー: 山田太郎
// 投稿数: 2
// コメント数: 2
```

コールバック地獄と比較すると、Promiseチェーンはフラットで読みやすいことがわかります。

## 5. Promise.all と Promise.race

### Promise.all

複数のPromiseを並列で実行し、すべてが完了するのを待ちます。

```javascript
const promise1 = fetchUser(1);
const promise2 = fetchUser(2);
const promise3 = fetchUser(3);

Promise.all([promise1, promise2, promise3])
  .then((results) => {
    console.log("全ユーザー:", results);
    // [{ id: 1, ... }, { id: 2, ... }, { id: 3, ... }]
  })
  .catch((error) => {
    // いずれかが失敗した場合
    console.error("エラー:", error);
  });
```

### Promise.race

複数のPromiseのうち、最初に完了したものの結果を取得します。

```javascript
const slow = new Promise((resolve) => {
  setTimeout(() => resolve("遅い処理"), 3000);
});

const fast = new Promise((resolve) => {
  setTimeout(() => resolve("速い処理"), 1000);
});

Promise.race([slow, fast])
  .then((result) => {
    console.log("勝者:", result); // "速い処理"
  });
```

## 6. コールバックとPromiseの比較

```javascript
// コールバック版（読みにくい）
fetchUser(1, (user) => {
  fetchPosts(user.id, (posts) => {
    fetchComments(posts[0].id, (comments) => {
      console.log(comments);
    });
  });
});

// Promise版（読みやすい）
fetchUser(1)
  .then((user) => fetchPosts(user.id))
  .then((posts) => fetchComments(posts[0].id))
  .then((comments) => console.log(comments))
  .catch((error) => console.error(error));
```

## ✨ まとめ

Promiseは、非同期処理を扱うための強力な機能です。`then`で成功時の処理、`catch`でエラー処理、`finally`で後処理を記述できます。Promiseチェーンを使うと、複数の非同期処理を読みやすく連結できます。

次のチャプターでは、Promiseをさらに直感的に書ける「async/await」について学んでいきましょう。
