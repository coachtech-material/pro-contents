# 10-1-2: Laravel Sailのセットアップ

## 🎯 このセクションで学ぶこと

-   Laravel Sailとは何か、その利点を理解する
-   Dockerがインストールされている環境で、新しいLaravelプロジェクトを作成する方法を学ぶ
-   Sailコマンドを使って、Dockerコンテナを起動・停止する方法を習得する

## 導入

バックエンドアプリケーションの開発を始めるにあたり、最初のステップは開発環境の構築です。PHP、Composer、データベースサーバー（MySQLなど）といった必要なソフトウェアを自分のPCに直接インストールするのは、環境差異やバージョンの問題を引き起こしやすく、手間がかかります。

そこで登場するのが**Laravel Sail**です。Sailは、Laravelのデフォルト開発環境であり、Dockerをベースにしています。Sailを使えば、いくつかの簡単なコマンドを実行するだけで、PHP、MySQL、Redisなど、Laravelアプリケーションの実行に必要なすべてのサービスを含んだDockerコンテナ環境を構築・管理できます。

**Sailの主な利点:**

-   **環境の統一**: チームメンバー全員が同じバージョンのソフトウェアで構成された、同じ開発環境を簡単に共有できます。
-   **PC環境のクリーン化**: 自分のPCに直接PHPやMySQLをインストールする必要がなく、環境を汚しません。
-   **簡単な操作**: `sail up`, `sail down` といった直感的なコマンドで、複雑なDockerコンテナを簡単に操作できます。

このセクションでは、Sailを使ってバックエンドとなるLaravelプロジェクトをセットアップします。

## 詳細解説

### 前提条件

-   **Docker Desktop**がインストールされ、実行中であること。
    -   まだインストールしていない場合は、公式サイトからダウンロードしてインストールしてください。
    -   [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
    -   [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
-   Windowsの場合は、**WSL2 (Windows Subsystem for Linux 2)** が有効になっていること。

### ステップ1: 新しいLaravelプロジェクトの作成

ターミナルを開き、プロジェクトを作成したいディレクトリに移動してください。そして、以下のコマンドを実行します。このコマンドは、Dockerを使って一時的なコンテナを起動し、その中で`laravel new`コマンドを実行して、`laravel-next-app`という名前の新しいLaravelプロジェクトを作成します。

```bash
# このコマンドは完了までに数分かかります
curl -s "https://laravel.build/laravel-next-app" | bash
```

コマンドが完了すると、`laravel-next-app`というディレクトリが作成されます。これが私たちのバックエンドアプリケーションのプロジェクトです。

### ステップ2: Sailの起動

次に、作成されたプロジェクトディレクトリに移動し、Sailを起動します。

```bash
# プロジェクトディレクトリに移動
cd laravel-next-app

# Sailをバックグラウンドで起動する
./vendor/bin/sail up -d
```

-   `./vendor/bin/sail`: Sailコマンド本体です。
-   `up`: Dockerコンテナを起動します。
-   `-d`: デタッチドモード。コンテナをバックグラウンドで実行します。これをつけないと、ターミナルがコンテナのログ出力に占有されてしまいます。

初回起動時は、Dockerイメージのダウンロードとビルドが行われるため、少し時間がかかります。コンテナが正常に起動すると、Laravelアプリケーション、MySQLデータベースなどがすべてコンテナ内で実行されている状態になります。

### ステップ3: 動作確認

ブラウザで `http://localhost` にアクセスしてください。Laravelのウェルカムページが表示されれば、バックエンドのセットアップは成功です！

![Laravel Welcome Page](https://raw.githubusercontent.com/coachtech-material/pro-contents/main/laravel%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E3%83%95%E3%83%AD%E3%83%B3%E3%83%88%E3%82%A8%E3%83%B3%E3%83%89%E5%AD%A6%E7%BF%92%E3%83%AD%E3%83%BC%E3%83%89%E3%83%9E%E3%83%83%E3%83%97/images/tutorial-10/laravel-welcome.png)

### よく使うSailコマンド

-   **コンテナの起動**: `./vendor/bin/sail up -d`
-   **コンテナの停止**: `./vendor/bin/sail down`
-   **Artisanコマンドの実行**: `./vendor/bin/sail artisan <command>` (例: `./vendor/bin/sail artisan migrate`)
-   **Composerコマンドの実行**: `./vendor/bin/sail composer <command>` (例: `./vendor/bin/sail composer require laravel/sanctum`)
-   **npmコマンドの実行**: `./vendor/bin/sail npm <command>` (例: `./vendor/bin/sail npm install`)
-   **コンテナ内に入る**: `./vendor/bin/sail shell`

毎回 `./vendor/bin/sail` と入力するのは少し面倒なので、エイリアスを設定すると便利です。

```bash
# .bashrc や .zshrc に追加
alias sail='[ -f sail ] && bash sail || bash vendor/bin/sail'
```

エイリアスを設定すれば、単に `sail up -d` や `sail artisan migrate` のようにコマンドを実行できるようになります。

## ✨ まとめ

-   Laravel Sailは、DockerをベースとしたLaravelの公式開発環境である。
-   `curl -s "https://laravel.build/your-app-name" | bash` コマンドで、新しいLaravelプロジェクトとSailのセットアップを簡単に行える。
-   `./vendor/bin/sail up -d` で開発環境（Dockerコンテナ）を起動し、`./vendor/bin/sail down` で停止する。
-   `sail`コマンドを経由することで、`artisan`や`composer`などのコマンドをコンテナ内で実行できる。

これで、バックエンドの準備が整いました。次のセクションでは、フロントエンドとなるNext.jsプロジェクトをセットアップします。
