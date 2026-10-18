# code-refactor

An agent skill that restructures, rewrites, or ports existing code to another language **while proving behavior is preserved** — with characterization tests, parity fixtures and staged, verifiable steps instead of big-bang changes.

一个 Agent 技能：重构、重写或把现有代码移植到另一种语言，并用特征测试、对拍样例和分步验证**证明行为不变**。

## Modes / 模式

| Mode | When | How behavior is proven |
|---|---|---|
| **refactor** | Same language, the structure is the problem: split a god module into a package, untangle circular imports, move modules, change a signature across all callers, migrate an internal API step by step | Existing code survives and moves in small mechanical steps; tests stay green between steps |
| **rewrite** | Same language, the code isn't worth evolving: unreadable legacy, a dead framework, "rewrite from scratch" | The old implementation becomes the oracle: characterization tests first, then a parity check old vs new |
| **port** | The target language differs (Python → Go/Rust, TS → Go/Rust, Java → Kotlin, C → Rust, …) | Shared fixtures and a modest differential run against both implementations; numeric, string, error, ordering and concurrency semantics are mapped explicitly |

Prefer refactor over rewrite whenever an incremental path exists. "Port and clean it up" is two projects: port first, refactor later. For tidying a single function or snippet, use [simplify-code](https://github.com/linkxzhou/simplify-code).

## Language pairs / 语言对

Mapping tables in `references/port-pairs.md`:

- Python ↔ Go · Python ↔ Rust
- JavaScript/TypeScript → Rust · Rust → TypeScript
- TypeScript ↔ Go
- Java ↔ Kotlin
- C → Rust · Rust → C (FFI surface)
- JavaScript → TypeScript (gradual typing)

Other pairs follow the general playbook in `references/port-playbook.md`.

## Install / 安装

```bash
npx skills add linkxzhou/code-refactor
```

Or clone it into your skills folder:

```bash
git clone --depth 1 https://github.com/linkxzhou/code-refactor.git ~/.claude/skills/code-refactor
```

## Structure / 结构

```
SKILL.md        # Skill definition: mode choice, safety gates, step-by-step workflows, report format
references/     # Port pairs, port playbook, refactoring catalog, rewrite checklist, safety net, templates, sources
evals/          # Eval cases, trigger evals and fixtures
```

## Evals / 评测

8 cases covering all three modes (Python module split, callback→async refactor plan, legacy JS rewrite, and ports Python→Go, Java→Kotlin, C→Rust, Python→Rust, TS→Go), graded against behavior-focused assertions:

| Configuration | Assertions passed |
|---|---|
| With skill | **42 / 48** |
| Baseline (no skill) | 35 / 48 |

## Sources / 来源

The wording is original; ideas were synthesized from popular refactoring, migration and porting skills and literature. See [`references/sources.md`](references/sources.md) for the full list with links and licenses.

## License

MIT — see [LICENSE](LICENSE).
