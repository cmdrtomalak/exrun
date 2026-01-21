# exrun - Multi-Language Exercise Runner

A Rustlings-style exercise runner that supports multiple programming languages with unit test gating.

## Features

- **Language agnostic** - Python, JavaScript, TypeScript, HTML/CSS, PyTorch, React
- **Sequential gating** - Exercises unlock only after previous ones pass
- **Watch mode** - Rerun tests on file save (like Rustlings)
- **Unified CLI** - Same commands regardless of language
- **Progress tracking** - SQLite-based progress persistence
- **Convention over configuration** - Minimal setup, order determined by directory names

## Installation

```bash
# Clone and install with uv
git clone <repo>
cd exercises_runner
uv sync

# Or install globally
uv tool install .
```

## Quick Start

```bash
# Navigate to an exercise course
cd sample_pytorch_course

# Start watch mode (main usage)
uv run exrun watch

# Or with auto-advance (no prompts)
uv run exrun watch --keep-going
```

## CLI Commands

```bash
# Watch mode - rerun tests on file changes
uv run exrun watch
uv run exrun watch --keep-going    # Auto-advance without prompts

# Run specific exercise
uv run exrun run 01_tensor_basics

# Run current exercise
uv run exrun run

# Re-run all previously passed exercises (regression check)
uv run exrun run --recheck

# Check current progress
uv run exrun status

# List all exercises
uv run exrun list

# Reset progress
uv run exrun reset           # Reset all
uv run exrun reset 01_hello  # Reset specific exercise

# Skip current exercise
uv run exrun skip

# Verify all exercises pass (for authors)
uv run exrun verify --all

# Initialize new course
uv run exrun init --language python --name "My Course"
```

## Creating a Course

### Directory Structure

Exercises are discovered automatically based on directory structure. Order is determined by numeric prefixes in directory names (e.g., `01_`, `02_`).

```
my_course/
├── exrun.toml               # Course configuration
├── exercises/
│   ├── 01_intro/
│   │   ├── problem.md       # Instructions (optional)
│   │   ├── src/
│   │   │   └── main.py      # Student code (with TODOs)
│   │   └── tests/
│   │       └── test_main.py # Unit tests
│   ├── 02_variables/
│   │   └── ...
│   └── 03_functions/
│       └── ...
```

### Nested Exercises

You can organize exercises into sections using nested directories:

```
my_course/
├── exrun.toml
├── exercises/
│   ├── 01_basics/
│   │   ├── 01_hello/        # Order: 1.1
│   │   │   ├── src/
│   │   │   └── tests/
│   │   └── 02_variables/    # Order: 1.2
│   │       └── ...
│   └── 02_advanced/
│       ├── 01_functions/    # Order: 2.1
│       └── 02_classes/      # Order: 2.2
```

### exrun.toml

The only configuration file needed. All fields except `exercises_path` are optional:

```toml
[course]
name = "Learn Python"
version = "1.0.0"
language = "python"
test_runner = "pytest"
exercises_path = "./exercises"

[settings]
timeout_seconds = 30    # Optional: default test timeout
```

### Exercise Naming Convention

- Directory names determine order: `01_hello` runs before `02_world`
- Display names are derived from directory names: `01_hello_world` → "Hello World"
- An exercise directory must contain either `src/` or `tests/` to be recognized

### Adding Hints

Add hints as comments at the bottom of test files. Students can scroll down to see them:

```python
def test_hello():
    assert hello() == "Hello, World!"


# ============================================================================
# HINTS (scroll down if you're stuck)
# ============================================================================
#
#
#
#
#
#
# Hint 1: Define a function using 'def hello():'
#
# Hint 2: Return a string using: return "Hello, World!"
```

## Supported Languages

| Language   | Test Runner              | File Extensions     |
|------------|--------------------------|---------------------|
| Python     | pytest                   | `.py`               |
| PyTorch    | pytest                   | `.py` + torch       |
| JavaScript | vitest/jest              | `.js`               |
| TypeScript | vitest + tsc             | `.ts`, `.tsx`       |
| React      | vitest + testing-library | `.jsx`, `.tsx`      |
| HTML/CSS   | Playwright               | `.html`, `.css`     |

Language is auto-detected from file extensions if not specified in `exrun.toml`.

## Sample Courses

### PyTorch Course (5 exercises)

1. **Tensor Basics** - Creating and inspecting tensors
2. **Tensor Operations** - Arithmetic and matrix operations
3. **Linear Layer** - Understanding nn.Linear
4. **Simple Network** - Building an MLP
5. **Training Loop** - Loss, optimizer, and training

```bash
cd sample_pytorch_course
uv run exrun watch
```

### React Course (3 exercises)

1. **Hello Component** - Creating your first React component
2. **Props** - Passing data to components
3. **State** - Managing component state with useState

```bash
cd sample_react_course
npm install  # First time only
uv run exrun watch
```

### TypeScript Course (4 exercises)

1. **Basic Types** - Type annotations, arrays, tuples
2. **Functions** - Typed functions, optional/default params, closures
3. **Interfaces** - Object shapes, optional/readonly properties
4. **Generics** - Type-safe reusable functions

```bash
cd sample_typescript_course
npm install  # First time only
uv run exrun watch
```

### HTML/CSS Course (5 exercises)

1. **HTML Basics** - Semantic HTML structure
2. **CSS Fundamentals** - Selectors, colors, typography
3. **Layout & Positioning** - Flexbox, Grid, positioning
4. **Responsive Design** - Media queries, mobile-first
5. **Interactive Components** - Transitions, animations, hover effects

```bash
cd sample_html_css_course
npm install  # First time only
uv run exrun watch
```

## Development

```bash
# Install dev dependencies
uv sync --all-extras

# Run linter
uv run ruff check src/

# Run type checker
uv run mypy src/

# Run tests
uv run pytest tests/
```

## License

MIT
