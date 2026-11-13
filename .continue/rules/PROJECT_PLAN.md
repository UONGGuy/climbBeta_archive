---
description: "Project planning and milestone tracking for ClimbBeta"
---
# ClimbBeta — Project Plan

> **Last Updated:** 2025  
> **Project Status:** Alpha — Core models, routes, and templates are functional. Several pieces need refactoring, cleanup, and extension.

---

## Table of Contents

1. [Project Vision & Goals](#1-project-vision--goals)
2. [Current State Assessment](#2-current-state-assessment)
3. [Immediate Fixes (Phase 0)](#3-immediate-fixes-phase-0)
4. [Phase 1 — Core Stabilisation](#4-phase-1--core-stabilisation)
5. [Phase 2 — Feature Expansion](#5-phase-2--feature-expansion)
6. [Phase 3 — User System & Reviews](#6-phase-3--user-system--reviews)
7. [Phase 4 — Admin Panel & Deployment](#7-phase-4--admin-panel--deployment)
8. [Phase 5 — Polish & Scale](#8-phase-5--polish--scale)
9. [Technology Roadmap](#9-technology-roadmap)
10. [Testing Strategy](#10-testing-strategy)

---

## 1. Project Vision & Goals

**ClimbBeta** is a comprehensive directory of climbing gyms in **London, UK**. The long-term vision includes:

- A searchable, filterable directory of every climbing gym in London
- Detailed gym profiles with boards, training equipment, facilities, opening hours, pricing
- User ratings and reviews
- Waiver links directory
- Beginner safety information page
- User authentication (optional)
- Admin panel for content management
- Static CSS styling for a polished look

---

## 2. Current State Assessment

### ✅ What Works

| Component | Status | Notes |
|---|---|---|
| **Flask app factory** (`app/__init__.py`) | ✅ Functional | Creates app, registers routes, initiates DB |
| **Base model** (`app/models/base_model.py`) | ✅ Functional | `BaseModel` with auto-increment `id` + `__repr__` |
| **Franchiser model** (`app/models/climbing_gyms.py`) | ✅ Functional | Uses `eFranchiser` enum |
| **ClimbingGym model** (`app/models/climbing_gyms.py`) | ✅ Functional | Has `franchiser` relationship + `features` relationship |
| **ClimbingGymFeature base** (`app/models/climbing_gym_features.py`) | ✅ Functional | Polymorphic base for features |
| **ClimbingBoard subclass** (`app/models/climbing_gym_features.py`) | ✅ Functional | Uses `eClimbBoard` enum, single-table inheritance |
| **Enums** (`app/models/enums.py`) | ✅ Functional | Auto-generated from JSON via `enum_tools.py` |
| **Routes** (`app/routes.py`) | ✅ Functional | Homepage + gym details route |
| **Templates** (`app/templates/`) | ✅ Functional | `base.html`, `index.html`, `climbing_gym.html` |
| **Config files** (`config/`) | ✅ Functional | Dev, prod, test configs |
| **Base test case** (`tests/base_test.py`) | ✅ Functional | In-memory SQLite test setup/teardown |
| **Tests: models** (`tests/test_models.py`) | ⚠️ Partially working | Uses old attribute names (`board_type`, `is_adjustable`, `angle_of_incline`) |
| **Tests: routes** (`tests/test_routes.py`) | ❌ Broken | References non-existent `ClimbingGymFeatures` class |
| **Seed script** (`database/seed.py`) | ❌ Broken | Uses old attribute names on `ClimbingBoard` |
| **GymBuilder** (`database/gym_builder.py`) | ❌ Broken | References non-existent `ClimbingGymFeatures` association table |
| **check_tables.py** | ❌ Broken | Uses old attribute names on `ClimbingBoard` |
| **run_data_pipeline.py** | ⚠️ Needs work | `generate_enums` import path likely wrong |

### 🔴 Critical Issues

1. **Old attribute names on `ClimbingBoard`**: The model was refactored from `board_type` → `board_model`, `is_adjustable` → `adjustable`, `angle_of_incline` → `angle`, but several files still use the old names:
   - `database/seed.py` — uses `board_type=`, `is_adjustable=`, `angle_of_incline=`
   - `tests/test_models.py` — uses `board_type=`, `is_adjustable=`, `angle_of_incline=`
   - `tests/test_routes.py` — uses old attribute names
   - `check_tables.py` — uses old attribute names
   - `.continue/rules/CONTINUE.md` — documentation shows old names

2. **Missing `ClimbingGymFeatures` association table**: `database/gym_builder.py` and `tests/test_routes.py` reference `ClimbingGymFeatures`, which was replaced by the polymorphic `ClimbingGymFeature` → `ClimbingBoard` design. It now exists only as a commented-out placeholder in `app/models/association_tables.py`.

3. **Relationship setup incomplete**: `app/models/__init__.py` has commented-out relationship definitions and a broken `features`/`boards` setup at the bottom.

4. **Seed script outdated**: Only seeds 2 franchisers, 3 gyms, and 1 board — does not use the JSON data pipeline.

---

## 3. Immediate Fixes (Phase 0)

> **Goal:** Get the app into a fully working, test-passing state with the current model design.

### 3.1 Fix `ClimbingBoard` Attribute Names Across Codebase

Update **all** references from old to new attribute names:

| Old (broken) | New (correct) |
|---|---|
| `board_type` | `board_model` |
| `is_adjustable` | `adjustable` |
| `angle_of_incline` | `angle` |

**Files to update:**

- `database/seed.py` — lines creating `ClimbingBoard` objects
- `tests/test_models.py` — `test_climbing_board_creation` and `test_climbing_gym_with_boards`
- `tests/test_routes.py` — `setUp` method
- `check_tables.py` — if it prints board attributes
- `.continue/rules/CONTINUE.md` — documentation examples

### 3.2 Fix or Remove `ClimbingGymFeatures` References

**Options:**
- **Option A:** Remove `ClimbingGymFeatures` entirely (since the polymorphic design replaces it). Update `gym_builder.py` and `test_routes.py` to use the new model structure.
- **Option B:** Keep `ClimbingGymFeatures` as a proper association table for additional feature metadata. This requires implementing it properly.

**Recommended: Option A** — the polymorphic `ClimbingGymFeature` → `ClimbingBoard` design is already in place and is cleaner.

### 3.3 Fix Relationship Setup in `app/models/__init__.py`

Replace the broken commented-out code at the bottom with proper relationship definitions:

```python
# app/models/__init__.py
from app.models.association_tables import *
from app.models.climbing_gyms import *
from app.models.climbing_gym_features import *
from app.models.enums import *
```

Remove the orphaned `features = relationship(...)` and `boards = association_proxy(...)` lines at the bottom.

### 3.4 Fix and Expand `database/seed.py`

Update `seed.py` to:
1. Use current `ClimbingBoard` attribute names
2. Populate from `ClimbingGymsData.json` using the data pipeline
3. Include more comprehensive seed data

### 3.5 Fix Tests

- **`tests/test_models.py`**: Update `test_climbing_board_creation` and `test_climbing_gym_with_boards` to use new attribute names
- **`tests/test_routes.py`**: Remove `ClimbingGymFeatures` reference, use the polymorphic `ClimbingBoard` approach instead

### 3.6 Fix `database/gym_builder.py`

Rewrite to work with the **polymorphic** `ClimbingGymFeature` → `ClimbingBoard` design instead of the `ClimbingGymFeatures` association table.

---

## 4. Phase 1 — Core Stabilisation

> **Goal:** Build a robust data pipeline, improve templates, and ensure all core features work end-to-end.

### 4.1 Complete the Data Pipeline

- [ ] Fix `run_data_pipeline.py` to properly call `generate_enums` and `populate_database`
- [ ] Implement the `populate_database` function in `database/seed.py` to parse `ClimbingGymsData.json` and create all gyms, features, boards, and franchisers
- [ ] Validate JSON data against expected schema

### 4.2 Improve Templates

- [ ] Add **CSS styling** (`app/static/style.css`) — create the `static/` directory
- [ ] Enhance `climbing_gym.html` to display:
  - Gym name and franchiser
  - All features (boards, activities, etc.)
  - Address, opening hours, pricing (once models are extended)
- [ ] Add a navigation bar with links to home, about, beginner info

### 4.3 Expand Models

| Model | Priority | Description |
|---|---|---|
| **ClimbingGym address fields** | High | Street, city, postcode, coordinates |
| **ClimbingGym opening hours** | Medium | JSON field or separate model |
| **ClimbingGym pricing** | Medium | JSON field or separate model |
| **ClimbingActivity** (new feature subclass) | Medium | Polymorphic subclass for bouldering, lead, top-rope, auto-belay |
| **ClimbingGymFeature** → more subtypes | Low | Spray walls, training boards, campus boards, etc. |
| **ClimbingGym photos** | Low | URL/image path storage |

---

## 5. Phase 2 — Feature Expansion

> **Goal:** Add user-facing features beyond the basic directory.

### 5.1 Filtering & Search

- [ ] Add a search bar on `index.html` to filter gyms by name
- [ ] Add filter options: by franchiser, by board type, by climbing activity, by location
- [ ] Implement server-side filtering with query parameters

### 5.2 Beginner Safety Page

- [ ] Create `beginner_safety.html` template
- [ ] Add route `/beginner-info`
- [ ] Populate with climbing safety information, equipment tips, and gym etiquette

### 5.3 Waiver Links Directory

- [ ] Add `waiver_url` field to `ClimbingGym` model
- [ ] Display waiver link on gym details page
- [ ] Create a waiver directory page listing all gyms with waiver links

### 5.4 Map Integration

- [ ] Add latitude/longitude fields to `ClimbingGym`
- [ ] Embed a map view (e.g., Leaflet.js) on the homepage showing all gyms
- [ ] Include a map on individual gym detail pages

---

## 6. Phase 3 — User System & Reviews

> **Goal:** Add user accounts and community features.

### 6.1 User Authentication

- [ ] Add `User` model with:
  - Username, email, password (hashed)
  - Profile fields (optional: bio, avatar, favourite gyms)
  - Role field (admin, user)
- [ ] Implement registration, login, logout (Flask-Login)
- [ ] Add authentication decorators for protected routes

### 6.2 User Ratings & Reviews

- [ ] Add `Review` model:
  - `user_id`, `gym_id`, `rating` (1–5), `text`, `created_at`
- [ ] Display reviews on gym detail page
- [ ] Allow logged-in users to submit/delete their own reviews
- [ ] Calculate and display average rating per gym

### 6.3 User Favourites

- [ ] Add many-to-many `user_favourite_gyms` association table
- [ ] Allow logged-in users to bookmark/favourite gyms
- [ ] Add a "My Favourites" page

---

## 7. Phase 4 — Admin Panel & Deployment

> **Goal:** Equip admins to manage content and deploy the app to production.

### 7.1 Admin Panel

- [ ] Create admin routes under `/admin/`
- [ ] Admin dashboard: overview statistics
- [ ] CRUD for gyms, franchisers, features, boards
- [ ] CRUD for user management
- [ ] Admin-only decorators

### 7.2 Deployment Preparation

- [ ] Verify `config/production.py` settings
- [ ] Set `DEBUG=False`, secure secret key via environment variable
- [ ] Configure `SQLALCHEMY_DATABASE_URI` for production
- [ ] Set up static file serving for production
- [ ] Test on InfinityFree or chosen hosting platform

### 7.3 Migration Support

- [ ] Install and configure **Flask-Migrate** (Alembic)
- [ ] Create initial migration
- [ ] Document migration workflow

---

## 8. Phase 5 — Polish & Scale

> **Goal:** Refine UX/UI, improve performance, and prepare for scaling.

### 8.1 UI/UX Improvements

- [ ] Responsive design (mobile-first)
- [ ] Dark mode toggle
- [ ] Loading spinners, toast notifications
- [ ] Enhanced gym cards with images and quick stats

### 8.2 Performance Optimisation

- [ ] Add database indexing on frequently queried columns
- [ ] Implement caching (Flask-Caching) for static pages
- [ ] Optimise SQL queries (eager loading with `joinedload`)

### 8.3 Data Expansion

- [ ] Extend `ClimbingGymsData.json` with complete London gym data
- [ ] Add gyms outside London (UK-wide, then international)
- [ ] Community contribution workflow for adding new gyms

### 8.4 API (Future)

- [ ] RESTful API for gym data (Flask-RESTful or similar)
- [ ] API authentication with tokens
- [ ] Rate limiting

---

## 9. Technology Roadmap

| Phase | Dependencies to Add | Purpose |
|---|---|---|
| **Phase 0** | None (fix existing) | |
| **Phase 1** | None (use Jinja2/CSS) | |
| **Phase 2** | Leaflet.js (CDN) | Map integration |
| **Phase 3** | Flask-Login, Flask-WTF, bcrypt/werkzeug | Authentication, forms, password hashing |
| **Phase 4** | Flask-Migrate, Gunicorn (prod) | DB migrations, WSGI server |
| **Phase 5** | Flask-Caching, Flask-RESTful (optional) | Performance, API |

---

## 10. Testing Strategy

### Current Test Coverage

| Test File | Status | Tests |
|---|---|---|
| `tests/test_models.py` | ⚠️ Partially broken | 4 tests (franchiser, board, gym, gym+boards) |
| `tests/test_routes.py` | ❌ Broken | 2 tests (index, gym details) |

### Testing Goals

- **Phase 0:** All existing tests pass with current model design
- **Phase 1:** Add tests for:
  - Data pipeline (JSON → DB)
  - All model relationships (gym → features → boards)
  - Template rendering with various data states
- **Phase 2+:** Test-driven development for all new features:
  - Write tests before implementing new models/routes
  - Aim for 80%+ code coverage

### Testing Best Practices

1. Use `BaseTestCase` for all tests (in-memory SQLite, fresh per test)
2. Test edge cases: empty database, missing gym, invalid IDs
3. Test both successful and failure scenarios
4. Use descriptive test names (`test_<feature>_<scenario>_<expected>`)
5. Keep tests independent (no shared state between tests)

---

## Appendix A: File Cleanup Checklist

Files that need attention after Phase 0:

| File | Action Needed |
|---|---|
| `database/seed.py` | Fix `ClimbingBoard` attrs, expand seed data |
| `database/gym_builder.py` | Rewrite for polymorphic model |
| `app/models/__init__.py` | Remove broken relationship lines |
| `app/models/association_tables.py` | Either implement or remove |
| `tests/test_models.py` | Fix `ClimbingBoard` attrs |
| `tests/test_routes.py` | Fix `ClimbingGymFeatures` ref + attrs |
| `check_tables.py` | Fix `ClimbingBoard` attrs |
| `run_data_pipeline.py` | Fix imports, implement `populate_database` |
| `.continue/rules/CONTINUE.md` | Update documentation examples |

## Appendix B: Quick Start Commands

```bash
# Reset database
python database/drop_tables.py

# Seed with test data
python database/seed.py

# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests/test_models.py

# Run app
python run.py

# Generate enums from JSON
python app/models/enum_tools.py database/ClimbingGymsData.json app/models/enums.py

# Run data pipeline
python run_data_pipeline.py --json database/ClimbingGymsData.json

# Check database contents
python check_tables.py
```

---

*This project plan was generated by analysing the ClimbBeta codebase. It reflects the current state of the code and proposes a phased approach to development. Priority should be given to Phase 0 fixes to establish a stable foundation.*