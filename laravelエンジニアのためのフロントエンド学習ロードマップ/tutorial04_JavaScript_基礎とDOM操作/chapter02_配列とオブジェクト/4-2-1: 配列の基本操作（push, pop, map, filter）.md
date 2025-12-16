# 4-2-1: 配列の基本操作（push, pop, map, filter）

## 🎯 このセクションで学ぶこと

- JavaScriptの配列の基本的な作成方法とアクセス方法を理解する
- `push`, `pop` を使って配列の末尾に要素を追加・削除できるようになる
- `map`, `filter` を使って配列を操作し、新しい配列を作成できるようになる

## 導入

配列は、複数の値を順番に格納できるデータ構造です。JavaScriptでは、配列を操作するための便利なメソッドが多数用意されています。このセクションでは、特に重要な `push`, `pop`, `map`, `filter` を学びます。

## 詳細解説

### 配列の作成とアクセス

```javascript
// 配列の作成
const fruits = ["Apple", "Banana", "Cherry"];

// インデックスを使ったアクセス
console.log(fruits[0]); // "Apple"
console.log(fruits.length); // 3
```

### `push` と `pop`

- **`push()`**: 配列の末尾に1つ以上の要素を追加します。
- **`pop()`**: 配列の末尾の要素を削除し、その要素を返します。

```javascript
const numbers = [1, 2, 3];
numbers.push(4);
console.log(numbers); // [1, 2, 3, 4]

const lastNumber = numbers.pop();
console.log(lastNumber); // 4
console.log(numbers); // [1, 2, 3]
```

### `map` と `filter`

- **`map()`**: 配列の各要素に対して関数を実行し、その結果からなる新しい配列を作成します。
- **`filter()`**: 配列の各要素に対して関数を実行し、その関数が `true` を返した要素だけを集めた新しい配列を作成します。

```javascript
const numbers = [1, 2, 3, 4, 5];

// 各要素を2倍にした新しい配列を作成
const doubled = numbers.map(num => num * 2);
console.log(doubled); // [2, 4, 6, 8, 10]

// 偶数だけを集めた新しい配列を作成
const evens = numbers.filter(num => num % 2 === 0);
console.log(evens); // [2, 4]
```

## 💡 TIP

- `map` や `filter` は元の配列を変更せず、新しい配列を返す「非破壊的メソッド」です。一方、`push` や `pop` は元の配列を変更する「破壊的メソッド」です。

## ✨ まとめ

- 配列は複数の値を順番に格納するデータ構造
- `push`, `pop` は配列の末尾を操作する
- `map`, `filter` は配列から新しい配列を作成する
