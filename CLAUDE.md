# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pyxelで作られたテキストアドベンチャーゲーム。学習目的のプロジェクト。

## Running

VSCodeのPyxel拡張（kitao.pyxel-vscode）で実行する。Pyodide（WebAssembly版Python）上で動作するため、`pip install`したパッケージは使えない。

## Architecture

- `game.py` — ゲーム本体。`SCENES`辞書でシナリオデータを定義し、`Game`クラスで更新・描画を行う
- `misaki_gothic.bdf` — 日本語フォント（美咲ゴシック）。`pyxel.Font()`で読み込む
- `pyxel_examples/` — Pyxel公式のサンプル集（参考用、ゲーム本体とは無関係）

## Key Constraints

- Pyodide環境のため外部パッケージ（PyxelUniversalFont等）は利用不可
- フォントは`pyxel.Font("misaki_gothic.bdf")`で読み込む

