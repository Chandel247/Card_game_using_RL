# Copilot instructions for this repository

Short, actionable guidance to help an AI assistant work productively in this repo.

1. Project layout (what matters)
   - Core Python modules live under `game/`. Key files:
     - `game/card.py` — defines a lightweight Card model (fields: `name`, `card_type`, `cost`, `atk`, `defense`, `hp`, `max_hp`) and methods `take_damage()` and `is_alive()`.
     - `game/player.py` — defines a Player model; file appears incomplete/truncated in the workspace. Expect attributes: `name`, `hp`, `shield`, `deck`, `hand`, `active_monster`, `bench` and methods like `draw_card()` and `retreat_card()`.

2. Big-picture architecture and intent
   - This is a small, single-process Python codebase representing a simple card/board game simulation.
   - Game state is kept in plain Python objects (Card, Player). There is no framework, no package layout, and no external services.
   - Keep changes minimal and idiomatic: focus on small, well-scoped edits to classes in `game/`.

3. Project-specific patterns and gotchas
   - Minimal typing is used in hints (e.g., `List[Card]`) but imports (from `typing`) may be missing — check for `NameError` or unfinished files before running.
   - `Card` stores both monster-specific and effect-specific fields in the same class. Branch on `card_type == 'monster'` vs other types.
   - Methods are small and stateful (mutate `hp`, `active_monster`, etc.). Prefer in-place updates and preserve existing attribute names.

4. Examples to reuse in patches or tests
   - Construct a monster card:
     - `Card("Goblin", "monster", atk=3, defense=1, hp=2, cost=1)`
   - Call damage and liveness checks:
     - `d = c.take_damage(4)` — returns actual damage after defense. `c.is_alive()` returns `True/False`.
   - Player creation (note: `player.py` expects a list of Card objects):
     - `p = Player("Alice", [Card(...), Card(...)])`

5. Editing guidance for AI
   - Preserve public attributes on `Card` (names above). If adding helpers, keep them private (`_helper_name`) unless broadly useful.
   - When editing `player.py`, first ensure imports exist (`from typing import List`) and that the file is not truncated; run a quick syntax check (see verification below) before changing behavior.
   - Avoid changing semantics of `take_damage()` and `is_alive()` without updating callers — they are the canonical behavior.

6. How to run or validate changes (discoverable steps)
   - There is no test harness in the repo. To sanity-check edits locally, run a small Python snippet from repo root, for example:
     ```python
     from game.card import Card
     from game.player import Player

     c = Card("Goblin", "monster", atk=3, defense=1, hp=2)
     print(c.take_damage(4), c.is_alive())
     p = Player("A", [c])
     print(p.name, len(p.deck))
     ```
   - If `player.py` raises import or syntax errors, open it and complete missing definitions before deeper changes.

7. Integration points and external deps
   - There are no external services or third-party dependencies used in the repository as-is. Treat this as pure Python code.

8. When to ask for clarification
   - If `player.py` is intentionally partial (e.g., the project expects you to implement methods), ask which behaviors to implement (draw rules, bench limits, retreats).
   - If you need a testing convention (pytest vs unittest) — request preference; none is present.

9. Minimal checklist for PRs
   - Run a syntax check (run file with `python -m py_compile <file>` or `python -c 'import game.card; import game.player'`).
   - Include one short example snippet showing the change in action (like the snippet above).
   - If you add typing imports, add them only where necessary and keep changes small.

If any part of `game/player.py` is intentionally incomplete, say so in the PR and ask what gameplay rules (draw/retreat) should be implemented. Reply here with any unclear areas and I will iterate on this guidance.
