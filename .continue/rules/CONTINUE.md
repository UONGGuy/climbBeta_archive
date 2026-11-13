---
description: "Comprehensive project guide for ClimbBeta - a Flask-based climbing gym directory web application"
globs: ["**/*.py", "**/*.html", "**/*.js", "**/*.json"]
---

# ClimbBeta Project Guide

## Project Overview

**ClimbBeta** is a Flask-based web application that serves as a comprehensive directory of climbing gyms in **London, UK**. The app allows users to browse climbing gyms, view detailed information about each gym — including available climbing boards, training equipment, facilities, and more — with future plans for user ratings/reviews and authentication.

### Key Technologies

| Technology | Purpose |
|---|---|
| **Python 3.13+** | Core programming language |
| **Flask 3.1** | Web framework (routes, templates, request handling) |
| **SQLAlchemy 2.0** | ORM (Object Relational Mapper) for database interactions |
| **Flask-SQLAlchemy 3.1** | Flask integration layer for SQLAlchemy |
| **Flask-Migrate 4.1** | Database migration support (Alembic under the hood) |
| **SQLite** | Database engine (development & production) |
| **Jinja2** | Template engine for HTML rendering |
| **unittest** | Testing framework |

### High-Level Architecture

```
┌──────────────────────────────────────────────────┐
│                   Flask App                      │
│  ┌──────────────┐    ┌──────────────────────┐    │
│  │   routes.py  │───▶│   Templates (Jinja2)  │    │
│  │  (Views/URLs) │    │   - base.html        │    │
│  └──────┬───────┘    │   - index.html        │    │
│         │            │   - climbing_gym.html │    │
│         ▼            └──────────────────────┘    │
│  ┌──────────────────────────────────────┐        │
│  │           models/                    │        │
│  │  ┌──────────┐  ┌─────────────────┐  │        │
│  │  │ base.py  │  │  climbing_gyms.py│  │        │
│  │  │ enums.py │  │  gym_features.py│  │        │
│  │  │ enum_tools│  │  association.py│  │        │
│  └──────────────────────────────────────┘        │
│         │                                        │
│         ▼                                        │
│  ┌──────────────┐    ┌──────────────────────┐    │
│  │  SQLAlchemy   │───▶│      SQLite DB       │    │
│  │    (ORM)      │    │   (climbbeta.db)     │    │
│  └──────────────┘    └──────────────────────┘    │
│                                                  │
│  ┌──────────────────────────────────────┐        │
│  │       configuration (config/)        │        │
│  │   - development.py                   │        │
│  │   - production.py                    │        │
│  │   - testing.py                       │        │
│  └──────────────────────────────────────┘        │
└──────────────────────────────────────────────────┘
```

The application follows a **Model-View-Controller (MVC)** pattern with Flask, where:
- **Models** (`app/models/`): Define the database schema and business logic
- **Views** (`app/templates/`): Jinja2 HTML templates
- **Controllers** (`app/routes.py`): Handle HTTP requests and orchestrate responses

---

## Getting Started

### Prerequisites

- **Python 3.8+** (3.13 recommended)
- **pip** (Python package manager) or **conda** (Anaconda)
- **Git** (for version control)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/UONGGuy/climbBeta.git
   cd climbBeta
   ```

2. **Create and activate a virtual environment** (choose one):

   **Option A — pip + venv**:
   ```bash
   python -m venv venv
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

   **Option B — conda**:
   ```bash
   conda env create -f environment.yml
   conda activate climbBeta
   ```

3. **Set up the database** (must run before first use):
   ```bash
   python database/seed.py
   ```
   This creates all tables and populates them with seed data (franchisers, climbing gyms, boards).

4. **Run the application**:
   ```bash
   # Option A:
   python run.py

   # Option B:
   flask run
   ```
   Visit **`http://127.0.0.1:5000`** in your browser.

### Basic Usage

| URL | Description |
|---|---|
| `http://127.0.0.1:5000/` | Home page — lists all climbing gyms |
| `http://127.0.0.1:5000/climbing_gym/1` | Details page for a specific gym (by ID) |

### Running Tests

Run all unit tests with:
```bash
python -m unittest discover tests
```

---

## Project Structure

```
climbBeta/
│
├── .continue/rules/           # Continue.dev project rules (this file)
├── .gitignore                 # Git ignore rules
├── README.md                  # Main README
├── requirements.txt           # pip dependencies
├── environment.yml            # conda dependencies
│
├── run.py                     # Application entry point (creates app & runs)
├── run_data_pipeline.py       # CLI tool: generates enums & populates DB from JSON
├── check_tables.py            # Utility: prints all database records
│
├── app/                       # Core application package
│   ├── __init__.py            # Flask app factory (create_app), DB initialization
│   ├── routes.py              # URL routing and view functions
│   │
│   ├── models/                # SQLAlchemy ORM models
│   │   ├── __init__.py        # Imports all models & defines relationships
│   │   ├── base_model.py      # Abstract base class (BaseModel) with ID + __repr__
│   │   ├── climbing_gyms.py   # Franchiser + ClimbingGym models
│   │   ├── climbing_gym_features.py  # ClimbingGymFeature + ClimbingBoard
│   │   ├── enums.py           # Enumerated types (auto-generated)
│   │   ├── enum_tools.py      # Script to generate enums from JSON source
│   │   └── association_tables.py  # Many-to-many (currently WIP/placeholder)
│   │
│   └── templates/             # Jinja2 HTML templates
│       ├── base.html          # Base template (header, footer, main block)
│       ├── index.html         # Homepage — list of gyms
│       └── climbing_gym.html  # Gym details page
│
├── config/                    # Environment-specific configurations
│   ├── __init__.py            # Initialization
│   ├── development.py         # Dev config (DEBUG=True, SQLite file)
│   ├── production.py          # Production config (DEBUG=False, SQLite file)
│   └── testing.py             # Test config (DEBUG=False, :memory: SQLite)
│
├── database/                  # Database scripts and data
│   ├── __init__.py            # Placeholder
│   ├── seed.py                # Populates database with seed data
│   ├── drop_tables.py         # Drops and recreates all tables
│   ├── gym_builder.py         # Builder pattern for complex gym creation
│   └── ClimbingGymsData.json  # Source data (all London climbing gyms)
│
├── instance/                  # Runtime instance folder (SQLite DB file created here)
│
├── tests/                     # Unit tests
│   ├── __init__.py
│   ├── base_test.py           # BaseTestCase class (setUp/tearDown with test config)
│   ├── conftest.py            # Test configuration + fixtures
│   ├── test_models.py         # Tests for model creation and relationships
│   └── test_routes.py         # Tests for route responses and content
│
└── .continue/                 # Continue.dev configuration
    └── rules/
        └── CONTINUE.md        # This file
```

### Key Configuration Files

| File | Purpose |
|---|---|
| `config/development.py` | Dev settings — `DEBUG=True`, `SQLALCHEMY_DATABASE_URI='sqlite:///climbbeta.db'` |
| `config/production.py` | Production settings — `DEBUG=False`, same SQLite path |
| `config/testing.py` | Test settings — `DEBUG=False`, `:memory:` SQLite database |
| `requirements.txt` | Python dependencies (pip) |
| `environment.yml` | Conda environment definition |
| `.gitignore` | Excludes `__pycache__/`, `*.db`, environment folders |

---

## Development Workflow

### Coding Standards & Conventions

- **Python**: Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- **Imports**: Group standard library, third-party, then local imports
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_CASE` for constants
- **SQLAlchemy Models**: Use `Mapped` type annotations with `mapped_column()` (SQLAlchemy 2.0 style)
- **Templates**: Use Jinja2 template inheritance via `{% extends %}` blocks
- **Enums**: Use `BaseEnum` with custom `__str__` for human-readable display

### Testing Approach

- **Framework**: Python's built-in `unittest`
- **Setup**: `BaseTestCase` creates a fresh app with the testing config and an **in-memory SQLite database** for each test
- **Teardown**: Drops all tables and disposes of the engine after each test
- **Running tests**:
  ```bash
  python -m unittest discover tests
  # OR
  python -m unittest tests/test_models.py
  python -m unittest tests/test_routes.py
  ```
- **Guideline**: Write a test for each new model/route. Use the existing `test_models.py` and `test_routes.py` as templates.

### Build & Deployment Process

**Current deployment target**: [InfinityFree](https://www.infinityfree.net/) (free hosting)

1. **Prepare the application** for deployment:
   - Set `config/production.py` as the active config
   - Ensure all routes work without `DEBUG=True`
   - Test with `python run.py`

2. **Deployment checklist** (to be confirmed/expanded):
   - [ ] Update `SQLALCHEMY_DATABASE_URI` if using a different database
   - [ ] Configure static file serving (CSS, JS)
   - [ ] Set up environment variables for secrets
   - [ ] Test on the target hosting platform

### Contribution Guidelines

1. **Fork** the repository on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make changes** with clear, descriptive commit messages
4. **Write/update unit tests** for new functionality
5. **Run tests** locally to ensure no regressions: `python -m unittest discover tests`
6. **Submit a pull request** against the main branch

---

## Key Concepts

### Domain Model & Entity Hierarchy

```
Franchiser (e.g., "City Bouldering")
    │
    └── ClimbingGym (e.g., "City Bouldering Aldgate")
            │
            └── ClimbingGymFeature (base)
                    │
                    └── ClimbingBoard (polymorphic subclass)
                            ├── board_model (eClimbBoard)
                            ├── adjustable (bool)
                            └── angle (float)
```

### Core Abstractions

| Concept | Description |
|---|---|
| **BaseModel** | Abstract base for all models. Provides auto-incrementing `id` PK and a `__repr__` method. |
| **Franchiser** | Company/chain that operates one or more climbing gyms. Stored in `franchisers` table. |
| **ClimbingGym** | A specific gym location. Has a name and belongs to one franchiser. |
| **ClimbingGymFeature** | Base class for polymorphic features (boards, spray walls, etc.). Uses single-table inheritance. |
| **ClimbingBoard** | A specific training board (Kilter, MoonBoard, Tension, etc.) with angle and adjustability. |
| **eFranchiser / eClimbBoard / eClimbActivities / etc.** | Python Enums auto-generated from the JSON data source (`ClimbingGymsData.json`). |
| **GymBuilder** | Implements the Builder pattern to construct complex Gym objects with all their features from a dictionary. |

### Design Patterns Used

| Pattern | Where | Purpose |
|---|---|---|
| **Factory** | `app/__init__.py` (`create_app()`) | Creates and configures the Flask app instance with config injection |
| **Builder** | `database/gym_builder.py` (`GymBuilder`) | Step-by-step construction of climbing gyms with associated features |
| **Template Method** | `app/templates/base.html` | Base template defining the common layout with `{% block %}` overrides |
| **Data Mapper** | SQLAlchemy ORM | Maps Python objects to database rows |
| **Polymorphic Inheritance** | `ClimbingGymFeature` → `ClimbingBoard` | SQLAlchemy single-table inheritance for shared feature attributes |

### Enum Generation Pipeline

```
ClimbingGymsData.json
        │
        ▼
  enum_tools.py          ← run_data_pipeline.py --json <file>
        │
        ▼
  app/models/enums.py    ← Python Enum classes generated
        │
        ▼
  database/seed.py       ← Uses enums + JSON to populate DB
```

---

## Common Tasks

### 1. Add a New Climbing Gym to the Database

**Option A** — Add to seed script (`database/seed.py`):
```python
# 1. Create or reuse a franchiser
new_franchiser = Franchiser(name=eFranchiser.YONDER)
db.session.add(new_franchiser)
db.session.commit()

# 2. Create the gym
new_gym = ClimbingGym(name="New Gym London", franchiser=new_franchiser)
db.session.add(new_gym)
db.session.commit()

# 3. Add features/boards
new_board = ClimbingBoard(
    board_type=eClimbBoard.MOONBOARD,
    adjustable=False,
    angle=40.0
)
db.session.add(new_board)
new_gym.boards.append(new_board)
db.session.commit()
```

**Option B** — Add to the JSON data file and re-run the data pipeline:
```bash
# 1. Edit database/ClimbingGymsData.json (add entry to "data" array)
# 2. Run the pipeline
python run_data_pipeline.py --json database/ClimbingGymsData.json
```

### 2. Add a New Enum Type (e.g., a New Board Brand)

```bash
# 1. Edit ClimbingGymsData.json
#    - Add the new brand to "Board climbing" entries and/or
#    - Add new dropdown options in "_dropdown_options"
# 2. Run enum generation
python app/models/enum_tools.py database/ClimbingGymsData.json app/models/enums.py
# 3. Verify the new enum appears in app/models/enums.py
```

### 3. Reset the Database

```bash
python database/drop_tables.py   # Drops all tables
python database/seed.py          # Recreates and seeds them
```

### 4. Add a New Page / Route

1. **Create a template** in `app/templates/`: `your_page.html` extending `base.html`
2. **Add a route** in `app/routes.py`:
   ```python
   @app.route('/your-page')
   def your_page():
       # Your logic here
       return render_template('your_page.html', data=some_data)
   ```
3. **Add a test** in `tests/test_routes.py` following the existing pattern

### 5. Run the Data Pipeline Manually

```bash
python run_data_pipeline.py --json database/ClimbingGymsData.json
# Add --validate to validate JSON first (validation logic TBD)
```

---

## Troubleshooting

| Issue | Likely Cause | Solution |
|---|---|---|
| `sqlite3.OperationalError: no such table` | Database not seeded | Run `python database/seed.py` |
| ImportError when running seed | Working directory wrong | Run from project root (`climbBeta/`) |
| `ModuleNotFoundError: No module named 'app'` | Python path issue | Add the project root to PYTHONPATH or run from the root directory |
| Database schema mismatch | Model changes without migration | Run `python database/drop_tables.py` to reset (⚠️ deletes data) |
| Tests fail with `RuntimeError: No application found` | Missing app context | Ensure tests use `base_test.py`'s `BaseTestCase` or create app context |
| Template not found | Wrong template path | Verify render_template path relative to `app/templates/` |
| Enum value not found | JSON data updated without re-running enum generation | Run `python app/models/enum_tools.py path/to/data.json app/models/enums.py` |
| Gunicorn/WSGI not configured | Deployment not yet set up | Use Flask's built-in dev server for now (`python run.py`) |

### Debugging Tips

- **Debug output**: The app prints diagnostic statements (e.g., `"Creating Flask app"`, `"Index route accessed"`) — check terminal/console output
- **Check database contents**: Run `python check_tables.py` to print all records
- **Inspect SQL queries**: Set `SQLALCHEMY_ECHO = True` in the config to log all SQL statements
- **Use Flask's interactive debugger**: When `DEBUG=True`, Flask shows an interactive debugger in the browser on errors

---

## References

### Documentation

| Resource | URL |
|---|---|
| **Flask Documentation** | https://flask.palletsprojects.com/ |
| **SQLAlchemy 2.0** | https://docs.sqlalchemy.org/ |
| **Flask-SQLAlchemy** | https://flask-sqlalchemy.palletsprojects.com/ |
| **Jinja2 Templates** | https://jinja.palletsprojects.com/ |
| **Python unittest** | https://docs.python.org/3/library/unittest.html |
| **Alembic / Flask-Migrate** | https://flask-migrate.readthedocs.io/ |

### Repository & Project

| Resource | URL |
|---|---|
| **GitHub Repository** | https://github.com/UONGGuy/climbBeta |
| **InfinityFree (deployment)** | https://www.infinityfree.net/ |

### Data Sources

- **ClimbingGymsData.json**: Manual research compilation of London climbing gyms. Contains gym names, franchisers, addresses, facilities, board specifications, opening hours, and more.

---

## Notes for Contributors

> **⚠️ Sections marked with "To be confirmed" or "TBD" need verification or completion. Please check the current codebase state before implementing.**

### Planned Features (from README)

- [ ] Page for beginners — climbing gym safety information
- [ ] Waiver links database for all relevant activities
- [ ] User ratings and reviews
- [ ] User authentication and authorization
- [ ] Admin panel for content management
- [ ] Static CSS file serving (`app/static/` directory — not yet created)

### Code That May Need Updates

- **`app/models/__init__.py`**: The `features` and `boards` relationship definitions at the bottom are commented-out work in progress
- **`association_tables.py`**: Currently a placeholder/WIP — the many-to-many relationship between gyms and boards needs to be properly implemented
- **`database/gym_builder.py`**: References `ClimbingGymFeatures` as an association table which may need synchronization with current models
- **`tests/test_routes.py`**: Uses `ClimbingGymFeatures` directly — may need updating when the association table is finalized
- **`check_tables.py`**: Currently references `ClimbingBoard` with old attribute names (`board_type`, `is_adjustable`, `angle_of_incline`) — needs updating for current model (which uses `board_model`, `adjustable`, `angle`)

---
*This guide was auto-generated from the ClimbBeta codebase. Last updated: 2025.*