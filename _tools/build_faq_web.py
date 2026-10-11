#!/usr/bin/env python3
"""よくある質問の Web 版（faq.html・faq_en.html）を、TryOn の原稿から書き出す。Android の答えも載せる。

原稿は TryOn のリポジトリにある（このスクリプトは読むだけ）:
- tools/faq/faq_content.py … iOS と共通の質問と答え（tools/faq/build_faq.py を通して読む）
- tools/android/android_strings.json … Android 向けに言い換えた答え（android_faq_<カテゴリ>_<質問>_a）と質問（_q）。
  Android の FAQ 画面（android/.../settings/FaqIndex.kt）が使っているものと同じ

TryOn の tools/faq/build_faq.py も Web 版を書き出すが、そちらは Android の答えを載せない。
このスクリプトはアプリ側のファイル（FAQ.xcstrings・FAQIndex.swift）には触らず、このリポジトリの2ファイルだけを書く。
（`_` で始まるフォルダーなので、GitHub Pages（Jekyll）では公開されない）

使い方: python3 _tools/build_faq_web.py [--tryon <TryOn のリポジトリ>]
"""
import argparse
import html
import importlib.util
import json
import pathlib

LEGAL = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_TRYON = pathlib.Path.home() / "Desktop/Personal/App/TryOn"

UPDATED = {"ja": "最終更新日: 2026年10月11日", "en": "Last updated: October 11, 2026"}
PLATFORM_NOTE = {
    "ja": "iPhone と Android で操作が違う質問は、それぞれの答えを載せています。",
    "en": "Where steps differ between iPhone and Android, both answers are shown.",
}
LABEL = {"ios": "iPhone", "android": "Android"}
DELETE_LINK = {"ja": ("delete.html", "アカウントの削除"), "en": ("delete_en.html", "Account deletion")}
DESCRIPTION = {
    "ja": "TryOn（iPhone・Android）のよくある質問。試着・似合う診断・クレジット・購入と解約・アカウント・プライバシーについて。",
    "en": "TryOn FAQ (iPhone and Android): try-on, Fit Report, credits, purchases and cancellation, account and privacy.",
}
# Android の言い換えが端末を問わない書き方になっていて、iPhone の答えと分けなくてよいもの（「iPhone」→「スマートフォン」だけの違い）。
SHARED_ANDROID_WORDING = {("privacy", "others")}
# Android の文言のうち FAQ の質問・答えではないもの（画面の読み上げ用）。
NOT_ITEMS = {"android_faq_expanded", "android_faq_collapsed"}


def load_build_faq(tryon: pathlib.Path):
    spec = importlib.util.spec_from_file_location("build_faq", tryon / "tools/faq/build_faq.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def android_overrides(tryon: pathlib.Path, sections) -> dict[tuple[str, str], dict[str, dict[str, str]]]:
    """(カテゴリ, 質問) → {"q": 訳 or なし, "a": 訳}。名前の決まりは xcstrings_to_android.py と同じ（ID を小文字に）。"""
    strings = json.loads((tryon / "tools/android/android_strings.json").read_text())["strings"]
    found: dict[tuple[str, str], dict[str, dict[str, str]]] = {}
    used: set[str] = set()
    for sid, _title, items in sections:
        for iid, *_ in items:
            base = f"android_faq_{sid}_{iid.lower()}"
            entry = {part: strings[f"{base}_{part}"] for part in ("q", "a") if f"{base}_{part}" in strings}
            if entry:
                assert "a" in entry, f"{base}: 質問だけ言い換えて答えが無い"
                found[(sid, iid)] = entry
                used.update(f"{base}_{part}" for part in entry)
    unused = {key for key in strings if key.startswith("android_faq_")} - used - NOT_ITEMS
    assert not unused, f"FAQ の項目に当たらない Android の文言: {sorted(unused)}"
    return found


def render_item(element_id: str, question: str, answers: list[tuple[str | None, str]]) -> str:
    paragraphs = "\n".join(
        f"  <p><strong>{html.escape(label)}</strong>: {html.escape(text)}</p>" if label else f"  <p>{html.escape(text)}</p>"
        for label, text in answers
    )
    return f'<details class="faq" id="{element_id}">\n  <summary>{html.escape(question)}</summary>\n{paragraphs}\n</details>'


def write_pages(build_faq, overrides) -> None:
    strings = build_faq.all_strings()
    sections = build_faq.SECTIONS
    for lang, page in build_faq.PAGE.items():
        t = lambda key: html.escape(strings[key][lang])  # noqa: E731
        other_file, other_lang, other_label = page["other"]
        toc = "\n".join(f'  <li><a href="#{sid}">{html.escape(title[lang])}</a></li>' for sid, title, _ in sections)
        body = []
        for sid, title, items in sections:
            body.append(f'<h2 id="{sid}">{html.escape(title[lang])}</h2>')
            for iid, *_ in items:
                question = strings[f"faq.{sid}.{iid}.q"][lang]
                answer = strings[f"faq.{sid}.{iid}.a"][lang]
                android = overrides.get((sid, iid))
                if android is None:
                    body.append(render_item(f"{sid}-{iid}", question, [(None, answer)]))
                elif (sid, iid) in SHARED_ANDROID_WORDING:
                    body.append(render_item(f"{sid}-{iid}", question, [(None, android["a"][lang])]))
                elif "q" in android:
                    # 質問も違う（ファミリー共有・サインイン）→ 端末ごとに別の質問にする。
                    body.append(render_item(f"{sid}-{iid}", question, [(LABEL["ios"], answer)]))
                    body.append(render_item(f"{sid}-{iid}-android", android["q"][lang], [(LABEL["android"], android["a"][lang])]))
                else:
                    body.append(render_item(
                        f"{sid}-{iid}", question, [(LABEL["ios"], answer), (LABEL["android"], android["a"][lang])]
                    ))
        support_file, support_label = page["support"]
        nav_items = list(page["nav"]) + [DELETE_LINK[lang]]
        nav = "\n".join(f'    <a href="{href}">{html.escape(label)}</a>' for href, label in nav_items)
        doc = f"""<!DOCTYPE html>
<html lang="{page['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t('faq.title')} | TryOn</title>
<meta name="description" content="{html.escape(DESCRIPTION[lang])}">
<link rel="stylesheet" href="style.css">
<link rel="alternate" hreflang="{other_lang}" href="{other_file}">
</head>
<body>

<header>
  <a class="app-name" href="index.html">TryOn</a>
  <h1>{t('faq.title')}</h1>
  <p class="meta">{UPDATED[lang]}</p>
  <p class="meta"><a href="{other_file}" lang="{other_lang}" hreflang="{other_lang}">{other_label}</a></p>
</header>

<main>

<p>{t('faq.lead')}</p>
<p class="meta">{html.escape(PLATFORM_NOTE[lang])}</p>
<ul class="faq-toc">
{toc}
</ul>

{chr(10).join(body)}

<div class="summary">
  <h2>{t('faq.contactTitle')}</h2>
  <p style="margin:0;">{t('faq.contactBody')} <a href="{support_file}">{html.escape(support_label)}</a></p>
</div>

</main>

<footer>
  <nav>
{nav}
    <a href="{other_file}" lang="{other_lang}" hreflang="{other_lang}">{other_label}</a>
  </nav>
  <p>© 2026 TryOn運営チーム</p>
</footer>

</body>
</html>
"""
        (LEGAL / page["file"]).write_text(doc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tryon", type=pathlib.Path, default=DEFAULT_TRYON, help="TryOn のリポジトリ")
    args = parser.parse_args()
    build_faq = load_build_faq(args.tryon)
    overrides = android_overrides(args.tryon, build_faq.SECTIONS)
    write_pages(build_faq, overrides)
    print("Android の答え", len(overrides), "問 →", ", ".join(f"{s}.{i}" for s, i in overrides))
