---
description: "Learning plan and development roadmap for the ClimbBeta project"
---

# ClimbBeta — Learning & Development Plan

> **Purpose:** This is your personal learning guide for building ClimbBeta from scratch. It breaks down the project into focused learning phases, each with specific goals, concepts to master, and hands-on exercises. The emphasis is on understanding *why* things work, not just making them work.

---

## Learning Philosophy

- **Build from first principles** — Don't copy-paste. Type each line and understand it.
- **Break it, then fix it** — Intentionally make mistakes to learn what error messages mean.
- **Read the docs** — Before asking "how", check the official Flask and SQLAlchemy docs.
- **Test everything** — Every new feature starts with a test.
- **Teach it back** — If you can explain your code in plain English, you understand it.

---

## Your Starting Point

You are starting fresh with this project. The codebase currently exists with:
- A working Flask app factory
- SQLAlchemy models with some broken/outdated references
- Broken tests and seed scripts
- A polymorphic model design that needs cleanup

**Your goal:** Not just to fix bugs, but to deeply understand each component well enough to rebuild it from memory.

---

## Phase 0 — Foundations & First Fixes

> **Theme:** Understand the existing codebase and make it work.

### Goals

1. Understand the Flask app lifecycle — from `run.py` to HTTP response
2. Understand SQLAlchemy models — how Python classes become database tables
3. Fix the broken code so tests pass
4. Write your first tests

### Concepts to Master

| Concept | Why It Matters | Key File |
|---|---|---|
| Flask app factory pattern | How the app is created and configured | `app/__init__.py` |
| SQLAlchemy ORM basics | How models map to tables | `app/models/` |
| Polymorphic inheritance | One table for multiple feature types | `climbing_gym_features.py` |
| Flask-SQLAlchemy setup | How `db` connects app and models | `app/__init__.py` |
| `ForeignKey` relationships | Linking tables together | All model files |
| `db.session` lifecycle | Add, commit, query, remove | Seed & test files |
| Python `unittest` basics | Setup, teardown, assertions | `tests/base_test.py` |
| Debugging techniques | Print statements, error tracebacks | Terminal |

### Hands-On Exercises

1. **Read `app/__init__.py` aloud** — Trace the flow:
   - Where does `create_app()` get called? (check `run.py`)
   - When are tables created?
   - How does `register_routes(app)` work?

2. **Inspect the model hierarchy** — Draw a diagram:
   ```
   BaseModel → Franchiser
            → ClimbingGym → has features →
            → ClimbingGymFeature → ClimbingBoard (polymorphic)
   ```

3. **Fix one file at a time:**
   - Start with `database/seed.py` — fix `board_type` to `board_model`, `is_adjustable` to `adjustable`, `angle_of_incline` to `angle`
   - Run `python database/seed.py` — does it succeed? What does the error say if not?
   - Fix `app/models/__init__.py` — remove the broken `features = relationship(...)` and `boards = association_proxy(...)` lines
   - Fix `app/models/association_tables.py` — decide: keep it or remove it?

4. **Fix and run tests:**
   - Fix `tests/test_models.py` — update `ClimbingBoard` attribute names
   - Fix `tests/test_routes.py` — remove `ClimbingGymFeatures` reference, use new polymorphic approach
   - Run `python -m unittest tests/test_models.py`
   - Run `python -m unittest tests/test_routes.py`
   - Celebrate when they all pass! 🎉

5. **Experiment in a Python shell:**
   ```python
   from app import create_app, db
   app = create_app()
   with app.app_context():
       db.create_all()
       # Play with models here
       from app.models import *
       f = Franchiser(name=eFranchiser.CITY_BOULDERING)
       db.session.add(f)
       db.session.commit()
       print(Franchiser.query.all())
   ```

### Checkpoint — Phase 0 Complete When:

- [ ] `python database/seed.py` runs without errors
- [ ] `python -m unittest discover tests` passes all tests
- [ ] You can explain the difference between `ClimbingGymFeature` and `ClimbingBoard` in your own words
- [ ] You understand why `board_type` was renamed to `board_model`

---

## Phase 1 — Data Pipeline & Models

> **Theme:** Build a proper data ingestion pipeline and expand the data model.

### Goals

1. Complete the `populate_database` function in `seed.py` to load data from `ClimbingGymsData.json`
2. Fix `run_data_pipeline.py` to work end-to-end
3. Add new model fields (address, hours, pricing)
4. Add a new polymorphic feature type (`ClimbingActivity`)

### Concepts to Master

| Concept | Why It Matters |
|---|---|
| JSON parsing in Python | How to read structured data |
| Builder design pattern | Complex object construction |
| Polymorphic inheritance in SQLAlchemy | Adding new feature types |
| Data validation | Ensuring data integrity before saving |
| `db.drop_all()` vs `db.create_all()` | When to reset vs migrate |

### Hands-On Exercises

1. **Build the `populate_database` function:**
   - Open `database/ClimbingGymsData.json` — understand the structure
   - In `database/seed.py`, implement the function to:
     1. Read the JSON
     2. Create or find franchisers
     3. Create gyms and link them to franchisers
     4. Create boards and features and link them to gyms
   - Run it: `python database/seed.py`
   - Verify with `python check_tables.py` (after fixing it)

2. **Fix `run_data_pipeline.py`:**
   - Why does `from app.models.enums import generate_enums` fail?
   - Should `generate_enums` be importable from `app.models.enums` or is it in `enum_tools.py`?
   - Fix the import and test the pipeline

3. **Create a new model — `ClimbingActivity`:**
   - Make it a polymorphic subclass of `ClimbingGymFeature`
   - It should have an `activity_type` field using `eClimbActivities` enum
   - Example: `ClimbingActivity(activity_type=eClimbActivities.BOULDERING)`
   - Write tests for it before implementing

4. **Add address fields to `ClimbingGym`:**
   ```python
   street: Mapped[str] = mapped_column(db.String(200), nullable=True)
   city: Mapped[str] = mapped_column(db.String(100), nullable=True)
   postcode: Mapped[str] = mapped_column(db.String(20), nullable=True)
   ```
   - Run `python database/drop_tables.py` to rebuild the schema
   - Update seed data to include addresses

### Checkpoint — Phase 1 Complete When:

- [ ] `python run_data_pipeline.py --json database/ClimbingGymsData.json` works
- [ ] `ClimbingActivity` is a working polymorphic type with tests
- [ ] `ClimbingGym` has address fields and seed data includes them
- [ ] You can explain the builder pattern and why it's useful

---

## Phase 2 — Templates, CSS & Routes

> **Theme:** Make the app look good and feel polished.

### Goals

1. Create `app/static/` directory with CSS styling
2. Enhance `index.html` with search/filter UI
3. Enhance `climbing_gym.html` with full gym details
4. Add new routes for beginner info and waiver links

### Concepts to Master

| Concept | Why It Matters |
|---|---|
| Jinja2 template inheritance | DRY HTML with `{% block %}` |
| Flask static files | Serving CSS, JS, images |
| Flask route parameters | `<int:gym_id>` and query strings |
| Server-side search | Filtering database results |

### Hands-On Exercises

1. **Create `app/static/style.css`:**
   - Start with a clean, minimal design
   - Use CSS custom properties (variables) for colours
   - Style: navigation bar, gym cards, gym detail page
   - Link it in `base.html`

2. **Enhance `index.html`:**
   ```html
   <form action="/" method="get">
     <input type="text" name="search" placeholder="Search gyms..." />
     <button type="submit">Search</button>
   </form>
   ```
   - In `routes.py`, check `request.args.get('search')` and filter `ClimbingGym.query.filter()`

3. **Enhance `climbing_gym.html`:**
   - Display gym name, franchiser name, address
   - List all features/boards with details (board type, angle, adjustable?)
   - List climbing activities
   - Style it with cards or a table

4. **Add `/beginner-info` route and template:**
   - Create `beginner_safety.html` extending `base.html`
   - Add content about climbing safety, etiquette, gear
   - Link to it from the navigation bar

### Checkpoint — Phase 2 Complete When:

- [ ] The app has a styled, consistent look
- [ ] You can search gyms by name on the homepage
- [ ] Gym details page shows all features and boards
- [ ] `/beginner-info` page exists and is linked from navigation

---

## Phase 3 — User Authentication

> **Theme:** Add user accounts with registration, login, and session management.

### Goals

1. Create a `User` model with hashed passwords
2. Implement registration and login routes
3. Add authentication with Flask-Login
4. Protect routes that require login

### Concepts to Master

| Concept | Why It Matters |
|---|---|
| Password hashing (werkzeug) | Never store plain-text passwords |
| Session management | How Flask-Login tracks logged-in users |
| Flask-WTF forms | CSRF protection, form validation |
| Login decorators | `@login_required` for protected views |

### Hands-On Exercises

1. **Install Flask-Login and Flask-WTF:**
   ```bash
   pip install flask-login flask-wtf
   ```

2. **Create the `User` model in `app/models/user.py`:**
   ```python
   from flask_login import UserMixin
   from werkzeug.security import generate_password_hash, check_password_hash
   
   class User(UserMixin, BaseModel):
       __tablename__ = "users"
       username: Mapped[str] = mapped_column(unique=True)
       email: Mapped[str] = mapped_column(unique=True)
       password_hash: Mapped[str] = mapped_column()
       
       def set_password(self, password):
           self.password_hash = generate_password_hash(password)
       
       def check_password(self, password):
           return check_password_hash(self.password_hash, password)
   ```

3. **Implement registration:**
   - Create `register.html` template with form
   - Route `/register` handles GET (show form) and POST (create user)
   - Validate username/email uniqueness
   - Log the user in after successful registration

4. **Implement login/logout:**
   - Create `login.html` template
   - Route `/login` — authenticate and start session
   - Route `/logout` — clear session
   - Add login/logout links to navigation

### Checkpoint — Phase 3 Complete When:

- [ ] Users can register with username + email + password
- [ ] Passwords are hashed (not stored in plain text)
- [ ] Users can log in and out
- [ ] `/profile` page shows the logged-in user's info (requires login)

---

## Phase 4 — Reviews & Favourites

> **Theme:** Add community features — ratings, reviews, and favouriting gyms.

### Goals

1. Add `Review` model (user can review a gym once)
2. Display reviews on gym detail page
3. Allow logged-in users to add/delete their own reviews
4. Let users favourite/bookmark gyms

### Concepts to Master

| Concept | Why It Matters |
|---|---|
| One-to-many relationships | A user has many reviews |
| Unique constraints | One review per user per gym |
| Many-to-many relationships | Users favourite many gyms |
| Database queries with filters | `Review.query.filter_by(...)` |

### Hands-On Exercises

1. **Create the `Review` model:**
   ```python
   class Review(BaseModel):
       __tablename__ = "reviews"
       user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"))
       gym_id: Mapped[int] = mapped_column(db.ForeignKey("climbing_gyms.id"))
       rating: Mapped[int] = mapped_column()  # 1-5
       text: Mapped[str] = mapped_column(db.Text)
       created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
       
       __table_args__ = (db.UniqueConstraint("user_id", "gym_id"),)
   ```

2. **Create review form and routes:**
   - `/gym/<id>/review` — POST only, creates a review
   - Display existing reviews on gym detail page
   - Calculate and show average rating

3. **Create favourites (many-to-many):**
   - Create `favourite_gyms` association table
   - Add `favourite_gyms = relationship(...)` to User model
   - `/gym/<id>/favourite` toggle route
   - `/my-favourites` page

### Checkpoint — Phase 4 Complete When:

- [ ] Users can leave reviews (rating + text) on gyms
- [ ] A user can only review a gym once
- [ ] Average rating shows on gym detail page
- [ ] Users can favourite/unfavourite gyms
- [ ] `/my-favourites` shows favourited gyms

---

## Phase 5 — Admin Panel & Deployment

> **Theme:** Build an admin interface and prepare for production.

### Goals

1. Create admin routes for CRUD operations on gyms
2. Add admin-only decorators
3. Configure the app for production deployment
4. Set up Flask-Migrate for database migrations

### Concepts to Master

| Concept | Why It Matters |
|---|---|
| Admin roles | Separating user permissions |
| CRUD operations | Create, Read, Update, Delete patterns |
| Migration management | Evolving database schema safely |
| Production configuration | Secret keys, debug off, error handling |
gg
### Hands-On Exercises

1. **Admin role check:**
   ```python
   def admin_required(f):
       @wraps(f)
       def decorated_function(*args, **kwargs):
           if not current_user.is_authenticated or not current_user.is_admin:
               abort(403)
           return f(*args, **kwargs)
       return decorated_function
   ```

2. **Admin routes:**
   - `/admin/gyms` — list all gyms
   - `/admin/gyms/new` — create new gym
   - `/admin/gyms/<id>/edit` — edit gym
   - `/admin/gyms/<id>/delete` — delete gym
   - Same for boards, franchisers, features

3. **Install and configure Flask-Migrate:**
   ```bash
   pip install flask-migrate
   ```
   - Initialize migrations
   - Create the initial migration
   - Learn `flask db upgrade`, `flask db downgrade`

4. **Production preparation:**
   - Set `SECRET_KEY` from environment variable
   - Ensure `DEBUG=False` in production
   - Test the app runs with `python run.py`
   - Research InfinityFree deployment steps

### Checkpoint — Phase 5 Complete When:

- [ ] Admin users can add/edit/delete gyms from a web interface
- [ ] Non-admin users get a 403 error for admin routes
- [ ] Flask-Migrate is set up and working
- [ ] You can run the app in "production mode"

---

## Phase 6 — Polish & Extend

> **Theme:** Refine the user experience and prepare for growth.

### Goals

1. Responsive design (mobile-friendly)
2. Dark mode toggle
3. Map integration with Leaflet.js
4. Performance optimisations

### Concepts to Master

| Concept | Why It Matters |
|---|---|
| Responsive CSS (media queries) | The app works on phones and tablets |
| JavaScript basics | Interactive features like dark mode |
| Leaflet.js | Embedding maps with gym markers |
| Database indexing | Faster queries as data grows |
| Flask-Caching | Reducing repeated work |

### Hands-On Exercises

1. **Add latitude/longitude to `ClimbingGym`:**
   - Add `latitude: Mapped[float]` and `longitude: Mapped[float]` fields
   - Seed some coordinates
   - Display a Leaflet.js map on the homepage with gym markers

2. **Dark mode toggle:**
   - Use CSS custom properties
   - Add a JavaScript toggle that switches `data-theme="dark"` on `<html>`

3. **Performance:**
   - Add indexes: `db.Index("idx_gym_name", ClimbingGym.name)`
   - Use `joinedload()` to eager-load relationships in queries

### Checkpoint — Phase 6 Complete When:

- [ ] The app looks good on mobile
- [ ] Users can toggle dark mode
- [ ] A map on the homepage shows all gym locations
- [ ] You understand what database indexes do

---

## Daily Practice Habits

| Duration | Activity |
|---|---|
| **15 min** | Read documentation (Flask, SQLAlchemy, Jinja2) |
| **30 min** | Write code (work on current phase) |
| **15 min** | Write tests or read existing tests |
| **10 min** | Review what you learned and write it down |

## When You Get Stuck

1. **Read the error message** — It tells you the file, line number, and what's wrong.
2. **Add print statements** — Print variables to see what's happening.
3. **Check the official docs** — Flask docs are excellent and thorough.
4. **Simplify** — Strip the problem down to the smallest failing case.
5. **Ask** — Explain what you tried and what happened.

## Progress Tracking

```
Phase 0: Foundations & First Fixes     [ ] Not started
Phase 1: Data Pipeline & Models        [ ] Not started
Phase 2: Templates, CSS & Routes       [ ] Not started
Phase 3: User Authentication           [ ] Not started
Phase 4: Reviews & Favourites          [ ] Not started
Phase 5: Admin Panel & Deployment      [ ] Not started
Phase 6: Polish & Extend               [ ] Not started
```

**Start with Phase 0 — understand the existing codebase first.**

---

*Happy climbing & happy coding! 🧗‍♂️💻*