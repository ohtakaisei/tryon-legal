# TryOn 規約・プライバシーポリシー

バーチャル試着アプリ **TryOn**（iOS）の法務文書を GitHub Pages で公開するリポジトリです。
アプリ本体のソースコードは含みません。

## 公開ページ

| ページ | ファイル | 用途 |
|---|---|---|
| ホーム | `index.html` | 各文書への入口 |
| 利用規約 | `terms.html` | App Store のペイウォールと設定画面からリンク |
| プライバシーポリシー | `privacy.html` | App Store Connect の Privacy Policy URL に登録 |
| お問い合わせ・削除依頼 | `support.html` | App Store Connect の Support URL に登録 |

## 更新の手順

1. HTML を編集する
2. 各ページ冒頭の「最終更新日」を更新する（規約本文を変えた場合は必須）
3. `main` ブランチへ push すると GitHub Pages が自動で再デプロイする

利用規約・プライバシーポリシーを**実質的に変更する場合**は、規約の定めに従い
効力発生日の相当期間前にアプリ内またはこのサイトで告知すること。

## アプリ側の参照箇所

アプリからのリンクは `TryOn/Features/Paywall/PaywallView.swift` の `LegalLinks` に定義。
URL を変更した場合はそちらも合わせて更新する。
