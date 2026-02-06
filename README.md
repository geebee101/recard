# 🎴 Lexicard

**Lexicard** (a.k.a pre-recard.social) is a powerful, lightweight Spaced Repetition System (SRS) prototype designed specifically for mastering Thai lexicon and idioms. Built with **NiceGUI** and **FastAPI**, it offers a reactive, modern interface for disciplined language learning.

---

## 🏗️ Major Components

- **`lexicard/models.py`**: Robust data structure definitions using Pydantic. Handles serialization to JSON and data ingestion from Excel spreadsheets.
- **`lexicard/probbucket.py`**: The core SRS engine. Implements a weighted probability system that dynamically prioritizes cards based on your learning history (Known, Review, Learn).
- **`lexicard/front_commons.py`**: A unified UI framework providing a consistent design language, HSL-based theming, and shared layout components.
- **`lexicard/auth.py`**: Custom authentication middleware protecting study routes and managing session-specific data.
- **`lexicard/main.py`**: The application's central nervous system, managing routing and server initialization.

---

## 🚀 Running the Application

Lexicard uses `uv` for lightning-fast dependency management and execution.

### Development Mode
To start the application with hot-reloading enabled:
```bash
uv run lexicard
```
Alternatively:
```bash
python -m lexicard.main
```

### Background Server mode
To run the server in the background and log output (useful for debugging networking/state):
```bash
python start_server.py
```

---

## 🧪 Testing Infrastructure

We maintain a rigorous testing suite covering both backend logic and user interaction.

### Run All Tests
```bash
uv run pytest
```

### Run with Coverage Report
To see which parts of the codebase are currently validated:
```bash
uv run pytest --cov=lexicard --cov-report=term-missing
```

---

## 🏆 Project Bragging Rights

We take stability seriously. As of our latest development cycle:

- **Current Code Coverage**: `~68%` 🚀
- **Architecture**: Full tab-specific session isolation.
- **UI Architecture**: Component-based frame system for infinite scalability.

---

## 🛠️ Tech Stack

- **[NiceGUI](https://nicegui.io/)**: For the reactive Python-based frontend.
- **[FastAPI](https://fastapi.tiangolo.com/)**: High-performance backend routing.
- **[Pydantic v2](https://docs.pydantic.dev/)**: Strict data validation and schema management.
- **[uv](https://github.com/astral-sh/uv)**: Next-generation Python package installer and runner.

---

## 📂 Project Structure

```text
lexicard/
├── lexicard/            # Core source code
│   ├── main.py          # Entry point
│   ├── models.py        # Data structures
│   ├── probbucket.py    # SRS logic
│   └── page_*.py        # Individual UI pages
├── tests/               # Pytest suite (Unit & UI)
├── _workfiles/          # Development logs & reviews
└── pyproject.toml       # Project configuration
```

---

## 🗺️ Roadmap

- [ ] Transition from JSON to SQLite/PostgreSQL for large-scale data.
- [ ] Full multi-user isolation and Cloud synchronization.
- [ ] Mobile-native packaging via NiceGUI's desktop/pwa modes.
- [ ] Advanced "Missing Word" and "Audio Transcription" practice modes.
