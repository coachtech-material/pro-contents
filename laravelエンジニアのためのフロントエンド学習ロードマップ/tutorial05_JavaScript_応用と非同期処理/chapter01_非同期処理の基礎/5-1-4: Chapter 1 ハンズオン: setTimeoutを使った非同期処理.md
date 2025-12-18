# 5-1-4: Chapter 1 ハンズオン: setTimeoutを使った非同期処理

## 🎯 このハンズオンの目的

このハンズオンでは、Chapter 1で学んだ非同期処理の基礎を実践します。`setTimeout`とPromiseを使って、非同期処理の動作を体験しましょう。

## 準備

作業用のHTMLファイルを作成します。

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>非同期処理の練習</title>
</head>
<body>
  <h1>非同期処理の練習</h1>
  <div id="output"></div>
  <script src="async-practice.js"></script>
</body>
</html>
```

## 課題1: 実行順序を予測する

以下のコードの実行順序を予測し、実際に実行して確認してください。

```javascript
console.log("A");

setTimeout(() => {
  console.log("B");
}, 0);

console.log("C");

setTimeout(() => {
  console.log("D");
}, 1000);

console.log("E");
```

### 解答

```
A
C
E
B（0ミリ秒後でも、同期処理の後に実行される）
D（1秒後）
```

`setTimeout`は0ミリ秒を指定しても、同期処理がすべて完了した後に実行されます。これはJavaScriptの「イベントループ」の仕組みによるものです。

## 課題2: カウントダウンタイマーを作成する

指定した秒数からカウントダウンし、0になったら「完了！」と表示するタイマーを作成してください。

### 要件

1. `countdown(seconds)` 関数を作成
2. 1秒ごとに残り秒数を表示
3. 0になったら「完了！」を表示

### 解答例

```javascript
function countdown(seconds) {
  console.log(`カウントダウン開始: ${seconds}秒`);
  
  for (let i = seconds; i >= 0; i--) {
    setTimeout(() => {
      if (i > 0) {
        console.log(i);
      } else {
        console.log("完了！");
      }
    }, (seconds - i) * 1000);
  }
}

countdown(5);

// 出力:
// カウントダウン開始: 5秒
// 5（即座に）
// 4（1秒後）
// 3（2秒後）
// 2（3秒後）
// 1（4秒後）
// 完了！（5秒後）
```

## 課題3: Promiseを使ったデータ取得シミュレーション

APIからデータを取得する処理をシミュレートする関数を作成してください。

### 要件

1. `fetchData(id)` 関数を作成（Promiseを返す）
2. 1秒後にデータを返す
3. idが0以下の場合はエラーを返す

### 解答例

```javascript
function fetchData(id) {
  return new Promise((resolve, reject) => {
    console.log(`データ取得中... (ID: ${id})`);
    
    setTimeout(() => {
      if (id <= 0) {
        reject(new Error("無効なIDです"));
      } else {
        resolve({
          id: id,
          title: `データ ${id}`,
          createdAt: new Date().toISOString()
        });
      }
    }, 1000);
  });
}

// 成功パターン
fetchData(1)
  .then((data) => {
    console.log("取得成功:", data);
  })
  .catch((error) => {
    console.error("エラー:", error.message);
  });

// 失敗パターン
fetchData(-1)
  .then((data) => {
    console.log("取得成功:", data);
  })
  .catch((error) => {
    console.error("エラー:", error.message);
  });
```

## 課題4: Promiseチェーンを使った連続処理

ユーザー情報を取得し、そのユーザーの投稿一覧を取得し、最初の投稿のコメントを取得する処理を作成してください。

### 解答例

```javascript
// ユーザー取得
function getUser(userId) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ id: userId, name: "山田太郎" });
    }, 500);
  });
}

// 投稿取得
function getPosts(userId) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { id: 1, userId: userId, title: "最初の投稿" },
        { id: 2, userId: userId, title: "2番目の投稿" }
      ]);
    }, 500);
  });
}

// コメント取得
function getComments(postId) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { id: 1, postId: postId, text: "素晴らしい記事です！" },
        { id: 2, postId: postId, text: "参考になりました" }
      ]);
    }, 500);
  });
}

// Promiseチェーンで連結
console.log("処理開始");

getUser(1)
  .then((user) => {
    console.log("ユーザー取得:", user.name);
    return getPosts(user.id);
  })
  .then((posts) => {
    console.log("投稿取得:", posts.length, "件");
    return getComments(posts[0].id);
  })
  .then((comments) => {
    console.log("コメント取得:", comments.length, "件");
    comments.forEach((comment) => {
      console.log(`  - ${comment.text}`);
    });
  })
  .catch((error) => {
    console.error("エラー:", error);
  })
  .finally(() => {
    console.log("処理完了");
  });
```

## 課題5: Promise.allを使った並列処理

複数のユーザーのデータを同時に取得し、全員の名前を表示してください。

### 解答例

```javascript
function getUser(userId) {
  return new Promise((resolve) => {
    const names = ["田中", "佐藤", "鈴木", "高橋", "渡辺"];
    setTimeout(() => {
      resolve({
        id: userId,
        name: names[userId - 1] || `ユーザー${userId}`
      });
    }, Math.random() * 1000); // ランダムな遅延
  });
}

// 5人のユーザーを並列で取得
const userPromises = [
  getUser(1),
  getUser(2),
  getUser(3),
  getUser(4),
  getUser(5)
];

console.log("全ユーザーを取得中...");

Promise.all(userPromises)
  .then((users) => {
    console.log("取得完了！");
    users.forEach((user) => {
      console.log(`  ID: ${user.id}, 名前: ${user.name}`);
    });
  })
  .catch((error) => {
    console.error("エラー:", error);
  });
```

## ✨ まとめ

このハンズオンでは、以下のことを実践しました。

- `setTimeout`を使った非同期処理の実行順序の理解
- Promiseを使った非同期処理の作成
- Promiseチェーンによる連続処理
- `Promise.all`を使った並列処理

次のチャプターでは、Promiseをより直感的に書ける`async/await`と、実際のAPI通信に使う`fetch API`について学んでいきましょう。
