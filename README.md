# Project ISO 2026

I built this with Claude Code in a single session. It's a quiz game: you see an ISO standard symbol, you pick the correct label from four options. Simple concept, ~5,000 icons deep.

---

## What It Is

ISO publishes thousands of standardized symbols across safety, transportation, healthcare, and public information. Most people recognize maybe a dozen. I turned that into a game.

The icon is the question. The correct label is the answer. That's it.

---

## How It Works

Each round presents an ISO symbol and four candidate labels. Pick the right one. The game tracks correct answers across a session and persists high scores locally.

The library covers ~5,000 symbols across safety, transportation, healthcare, public information, and packaging categories. More than enough to keep you honest.

<!-- PLACEHOLDER: Screenshot or demo GIF if available -->

---

## Why I Built It

I wanted something scoped tightly enough to finish in one sitting, with a clear definition of done, that produced something I could actually use. This checked all three boxes.

I stood it up in three prompts. A complete, playable game from a focused session with Claude Code.

---

## Technology Stack

- **Language**: Python
- **Framework**: PyQt6 (desktop GUI)
- **Icon Library**: ~5,000 ISO standard symbols, bundled locally
- **Built with**: Claude Code (Anthropic)

---

## What This Demonstrates

Three prompts to a working desktop app. Scoped, complete, playable. The mobile port and the planned server component live in [`mobile_icon_id`](#).

---

## Related

| Project | What it is |
|---|---|
| [Mobile Icon ID](https://github.com/thrudnar/mobile_icon_id) | I ported this to React Native/Expo using Cursor. It's on my phone. The architecture is more interesting: 500-image packs, config-driven switching, a planned server component for the full library. |
| [TerrAIn](https://github.com/thrudnar/terrain) | A production job hunting pipeline I designed and built with Claude Code. Five pipeline stages, three provider adapters, 152 tests, published at v0.8. |
