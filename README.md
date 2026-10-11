# TryOn 規約・プライバシーポリシー

バーチャル試着アプリ **TryOn**（iOS 版・Android 版）の法務文書を GitHub Pages で公開するリポジトリです。
アプリ本体のソースコードは含みません。

## 公開ページ

| ページ | ファイル | 用途 |
|---|---|---|
| ホーム | `index.html` | 各文書への入口 |
| 利用規約 | `terms.html` | ペイウォールと設定画面からリンク |
| プライバシーポリシー | `privacy.html` | App Store Connect の Privacy Policy URL・Play Console のプライバシー ポリシーに登録 |
| お問い合わせ・削除依頼 | `support.html` | App Store Connect の Support URL に登録 |
| アカウントとデータの削除 | `delete.html` | Play Console のデータ セーフティの「アカウントの削除の URL」に登録（iOS・Android の手順、ウェブからの依頼、消えるもの・残るもの） |
| よくある質問 | `faq.html` | アプリの「よくある質問」の Web 版（下の「FAQ の作り直し」） |

英語版は各ファイル名に `_en` を付けたもの（日本語版が正）。

## 更新の手順

1. HTML を編集する
2. 各ページ冒頭の「最終更新日」を更新する（規約本文を変えた場合は必須）
3. `main` ブランチへ push すると GitHub Pages が自動で再デプロイする

利用規約・プライバシーポリシーを**実質的に変更する場合**は、規約の定めに従い
効力発生日の相当期間前にアプリ内またはこのサイトで告知すること。

## FAQ の作り直し

`faq.html`・`faq_en.html` は手で直さない。原稿は TryOn のリポジトリ（`tools/faq/faq_content.py` と、
Android の言い換え `tools/android/android_strings.json` の `android_faq_*`）。原稿を直したら:

```bash
python3 _tools/build_faq_web.py            # TryOn が ~/Desktop/Personal/App/TryOn に無いときは --tryon <場所>
```

TryOn の `tools/faq/build_faq.py` もこの2ファイルを書き出すが、Android の答えを載せない。
アプリの文言を作り直すために `build_faq.py` を実行したら、続けて上のスクリプトも実行すること。
最終更新日は `_tools/build_faq_web.py` の `UPDATED` で変える。

## アプリ側の参照箇所

アプリからのリンクは `TryOn/Features/Paywall/PaywallView.swift` の `LegalLinks` に定義。
URL を変更した場合はそちらも合わせて更新する。
