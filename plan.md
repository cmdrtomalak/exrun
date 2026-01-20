# Multi-Language Exercise Runner - Plan

A Rustlings-style exercise runner that supports multiple programming languages (Python, JavaScript, TypeScript, HTML/CSS, PyTorch) with unit test gating.

**Built with Python 3.13 and managed via [uv](https://github.com/astral-sh/uv).**

## Goals

1. **Language agnostic** - Detect language from file extension or config and run appropriate test harness
2. **Sequential gating** - Exercises unlock only after previous ones pass
3. **Watch mode** - Rerun tests on file save (like Rustlings)
4. **Unified CLI experience** - Same commands regardless of language
5. **Easy authoring** - Simple format for creating new exercise sets
6. **uv-native** - Uses uv for dependency management, virtual envs, and running

---

## Architecture

```
exercises_runner/
├── pyproject.toml        # uv/PEP 621 project config
├── uv.lock               # Locked dependencies
├── src/
│   └── exrun/
│       ├── __init__.py
│       ├── __main__.py   # Entry point (python -m exrun)
│       ├── cli.py        # CLI with typer/click
│       ├── runner.py     # Core orchestration logic
│       ├── watcher.py    # File system watcher (watchfiles)
│       ├── progress.py   # Progress tracking (JSON state file)
│       ├── exercise.py   # Exercise metadata parsing
│       └── adapters/     # Language-specific adapters
│           ├── __init__.py
│           ├── base.py       # Abstract adapter interface
│           ├── python.py     # pytest adapter
│           ├── javascript.py # jest/vitest adapter (via subprocess)
│           ├── typescript.py # vitest + tsc adapter
│           ├── html_css.py   # playwright adapter
│           └── pytorch.py    # pytest + torch adapter
├── tests/
│   └── ...
└── README.md
```

---

## Project Configuration (.exrun.toml)

Similar to workshop runner's `.wr.toml`, exrun uses a root config file to locate the exercise tree:

```toml
# .exrun.toml (in project root or home directory)

[project]
exercises_path = "./exercises"    # Path to exercise tree (relative or absolute)
# Or point to a remote course:
# exercises_path = "https://github.com/user/learn-python-exercises.git"

[defaults]
language = "python"
test_runner = "pytest"
```

The runner searches for `.exrun.toml` in:
1. Current directory
2. Parent directories (up to git root or home)
3. `~/.config/exrun/config.toml` (global defaults)

---

## Exercise Structure

Each exercise set lives in its own directory, with `progress.db` (SQLite) for tracking:

```
my_python_course/
├── exercises.toml            # Course metadata
├── progress.db               # SQLite database for progress tracking
├── exercises/
│   ├── 01_variables/
│   │   ├── exercise.toml     # Exercise metadata
│   │   ├── problem.md        # Instructions shown to user
│   │   ├── src/
│   │   │   └── main.py       # Student edits this (has TODO markers)
│   │   └── tests/
│   │       └── test_main.py  # Unit tests (hidden or visible)
│   ├── 02_functions/
│   │   ├── exercise.toml
│   │   ├── problem.md
│   │   ├── src/
│   │   │   └── main.py
│   │   └── tests/
│   │       └── test_main.py
│   └── ...
```

### exercises.toml (Course Config)

```toml
[course]
name = "Learn Python"
version = "1.0.0"
language = "python"           # primary language
test_runner = "pytest"        # pytest | jest | vitest | custom

[settings]
show_hints = true
max_attempts_before_hint = 3
```

### exercise.toml (Per-Exercise Config)

```toml
[exercise]
name = "Variables"
order = 1
difficulty = "beginner"

[test]
command = "pytest"            # override course default if needed
timeout_seconds = 30

[hints]
enabled = true
hints = [
  "Remember to use the = operator for assignment",
  "Python variables don't need type declarations"
]
```

---

## Language Detection & Test Harness Mapping

| Extension(s)         | Language   | Default Test Runner    | Alt Runners           |
|----------------------|------------|------------------------|-----------------------|
| `.py`                | Python     | pytest                 | unittest, doctest     |
| `.js`                | JavaScript | vitest / jest          | mocha                 |
| `.ts`, `.tsx`        | TypeScript | vitest / jest          | mocha                 |
| `.html`, `.css`      | HTML/CSS   | playwright             | puppeteer, cypress    |
| `.py` + torch import | PyTorch    | pytest + GPU detection | -                     |

Detection priority:
1. Explicit config in `exercise.toml`
2. Course-level config in `exercises.toml`
3. Auto-detect from file extensions in `src/`

---

## CLI Commands

All commands run via `uv run`:

```bash
# Start watch mode (main usage)
uv run exrun watch

# Watch mode with auto-advance (no "ready to continue?" prompt)
uv run exrun watch --keep-going

# Run specific exercise
uv run exrun run 01_variables

# Re-run all previously completed exercises (regression check)
uv run exrun run --recheck

# Recheck and keep going through all exercises
uv run exrun run --recheck --keep-going

# Check current progress
uv run exrun status

# Reset progress (start over)
uv run exrun reset

# Skip to next exercise (escape hatch)
uv run exrun skip

# List all exercises with status
uv run exrun list

# Verify entire course (for authors)
uv run exrun verify --all

# Initialize new course
uv run exrun init --language python --name "My Course"
```

### Key Flags

| Flag           | Description                                                    |
|----------------|----------------------------------------------------------------|
| `--recheck`    | Re-run all previously passed exercises to verify they still pass |
| `--keep-going` | Auto-advance to next exercise without prompting user           |
| `--from N`     | Start from exercise N (skip earlier exercises)                 |
| `--only N`     | Run only exercise N                                            |

Or install globally and run directly:

```bash
uv tool install .
exrun watch --keep-going
```

---

## Core Features

### 1. Watch Mode

- Uses `watchfiles` for efficient file watching
- On save: run tests for current exercise
- On pass: auto-advance to next exercise (if `--keep-going`), display problem.md
- On fail: show test output, hints after N attempts
- Without `--keep-going`: prompt "Press Enter to continue to next exercise..."

### 2. Progress Tracking (SQLite)

Progress is stored in `progress.db` inside the exercise directory (like workshop runner):

```sql
-- progress.db schema

CREATE TABLE exercises (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    order_num INTEGER NOT NULL,
    status TEXT DEFAULT 'pending',  -- pending | passed | skipped
    attempts INTEGER DEFAULT 0,
    first_passed_at TIMESTAMP,
    last_attempt_at TIMESTAMP
);

CREATE TABLE attempts (
    id INTEGER PRIMARY KEY,
    exercise_id INTEGER REFERENCES exercises(id),
    passed BOOLEAN NOT NULL,
    output TEXT,
    duration_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hints_shown (
    exercise_id INTEGER REFERENCES exercises(id),
    hint_index INTEGER,
    shown_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (exercise_id, hint_index)
);
```

**Why SQLite over JSON?**
- Atomic writes (no corruption on crash)
- Query history easily (`--recheck` can check last pass time)
- Scales to large exercise sets
- Standard library support (`sqlite3`)

### 3. Test Result Parsing

Each language adapter must:
- Execute the test command
- Parse stdout/stderr for pass/fail
- Extract individual test names and results
- Return structured result:

```python
from dataclasses import dataclass

@dataclass
class TestFailure:
    test_name: str
    message: str
    location: str | None = None

@dataclass
class TestResult:
    passed: bool
    tests_run: int
    tests_passed: int
    failures: list[TestFailure]
    output: str
```

### 4. Exercise Gating Logic

```
if current_exercise.tests_pass():
    mark_complete(current_exercise)
    current_exercise = next_exercise()
    display(current_exercise.problem_md)
else:
    increment_attempts()
    if attempts >= hint_threshold:
        show_next_hint()
    display(test_failures)
```

---

## HTML/CSS Testing Approach

Since HTML/CSS don't have traditional unit tests:

1. **Visual regression** - Compare rendered output to reference screenshot
2. **DOM assertions** - Check for expected elements, classes, attributes
3. **Computed styles** - Verify CSS properties are correctly applied

Example test (using Playwright):

```javascript
test('button has correct styling', async ({ page }) => {
  await page.goto('file://' + exercisePath + '/index.html');
  
  const button = page.locator('button.primary');
  await expect(button).toBeVisible();
  await expect(button).toHaveCSS('background-color', 'rgb(0, 123, 255)');
  await expect(button).toHaveCSS('border-radius', '4px');
});
```

---

## PyTorch-Specific Features

- Detect CUDA availability, run tests on CPU if GPU unavailable
- Tensor shape assertions
- Gradient checking utilities
- Model architecture validation

Example test:

```python
def test_model_architecture():
    model = solution.MyModel()
    
    # Check layer types
    assert isinstance(model.fc1, nn.Linear)
    assert model.fc1.in_features == 784
    assert model.fc1.out_features == 128
    
    # Check forward pass shape
    x = torch.randn(32, 784)
    out = model(x)
    assert out.shape == (32, 10)
```

---

## Implementation Phases

### Phase 1: MVP (2 weeks)
- [ ] Project setup with `uv init` and pyproject.toml
- [ ] CLI skeleton with typer
- [ ] Python + pytest adapter
- [ ] Watch mode with watchfiles
- [ ] Progress tracking (SQLite `progress.db`)
- [ ] Exercise parsing (TOML config with tomllib)
- [ ] Rich terminal output

### Phase 2: Multi-Language (2 weeks)
- [ ] JavaScript/TypeScript + vitest adapter (subprocess)
- [ ] Language auto-detection
- [ ] Hint system
- [ ] Better error formatting with rich

### Phase 3: HTML/CSS + Polish (2 weeks)
- [ ] Playwright adapter for HTML/CSS
- [ ] Course authoring tools (`exrun init`, `exrun verify`)
- [ ] Progress visualization (rich tables/panels)
- [ ] Documentation

### Phase 4: Advanced (ongoing)
- [ ] PyTorch adapter with GPU handling
- [ ] Remote exercise fetching (git-based courses)
- [ ] Browser-based UI option (optional web dashboard)
- [ ] Exercise analytics for authors

---

## Technology Choices

| Component        | Choice              | PyPI Package         |
|------------------|---------------------|----------------------|
| Python Version   | 3.13+               | -                    |
| Package Manager  | uv                  | -                    |
| CLI Framework    | typer               | `typer[all]`         |
| File Watcher     | watchfiles          | `watchfiles`         |
| TUI/Rich Output  | rich                | `rich`               |
| Config Parsing   | tomllib             | stdlib (3.11+)       |
| Progress Store   | SQLite              | stdlib `sqlite3`     |
| Subprocess       | subprocess          | stdlib               |
| Async (optional) | asyncio             | stdlib               |

### Why Python 3.13 + uv?
- **Modern Python features** - Pattern matching, type hints, dataclasses
- **uv is fast** - Near-instant dependency resolution and venv creation
- **Easy contributions** - Python is accessible to most developers
- **Native pytest integration** - No subprocess needed for Python exercises
- **Cross-platform** - Works on Linux, macOS, Windows
- **Script-friendly** - Can also run as `uv run exrun.py` for single-file mode

### pyproject.toml

```toml
[project]
name = "exrun"
version = "0.1.0"
description = "Multi-language exercise runner with test gating"
requires-python = ">=3.13"
dependencies = [
    "typer[all]>=0.12",
    "watchfiles>=0.21",
    "rich>=13.7",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.4",
    "mypy>=1.10",
]
playwright = [
    "playwright>=1.44",
]

[project.scripts]
exrun = "exrun.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/exrun"]

[tool.ruff]
target-version = "py313"
line-length = 100

[tool.mypy]
python_version = "3.13"
strict = true
```

---

## Prior Art & Inspiration

| Tool              | Language(s)     | Notes                                    |
|-------------------|-----------------|------------------------------------------|
| Rustlings         | Rust            | Watch mode, sequential exercises         |
| wr (workshop runner)| Rust          | Used by "100 Exercises to Learn Rust"   |
| Exercism          | Multi           | Web platform, per-language test runners  |
| Codecademy        | Multi           | Web-based, not local                     |
| freeCodeCamp      | JS/Web          | Web-based curriculum                     |

**Key differentiator**: Local-first, language-agnostic, author-friendly exercise authoring.

---

## Open Questions

1. **Should exercises be git submodules or embedded?**
   - Git allows easy updates, but adds complexity
   - Embedded simpler but harder to update courses

2. **How to handle exercises that need external dependencies?**
   - Auto-detect from requirements.txt / package.json?
   - Require author to specify in exercise.toml?

3. **Should the runner install dependencies automatically?**
   - Convenient but potentially dangerous
   - Could prompt user: "This exercise needs numpy. Install? [y/N]"

4. **Support for interactive exercises (REPL-style)?**
   - Beyond MVP but useful for some teaching scenarios

---

## Next Steps

1. Initialize project with `uv init exrun`
2. Set up pyproject.toml with dependencies
3. Implement CLI skeleton with typer
4. Build Python/pytest adapter first
5. Add watchfiles integration for watch mode
6. Test with a sample 5-exercise Python course
7. Iterate based on UX feedback

## Quick Start (Development)

```bash
# Initialize project
cd exercises_runner
uv init --name exrun --python 3.13

# Add dependencies
uv add typer[all] watchfiles rich

# Add dev dependencies
uv add --dev pytest ruff mypy

# Run the CLI
uv run exrun --help

# Or run as module
uv run python -m exrun --help
```
