# FavvMenuz — COMPLETE FULL-STACK IMPLEMENTATION PROMPT

You are an autonomous senior full-stack engineer, Django architect, frontend designer and DevOps engineer. Your task is to build **FavvMenuz**, a complete, polished, runnable and deployable full-stack project in the current repository.

Treat this as a serious software engineering portfolio project built by a solo developer. The result must demonstrate sound architecture, reliable backend engineering, practical GenAI integration, a distinctive user interface, Docker-based deployment and sensible automation.

**Do not just give me a plan, pseudocode, snippets, or a list of files. Create and implement the actual project files.** Make reasonable assumptions without asking follow-up questions. If the workspace already contains files, inspect them first and preserve useful existing work. If it is empty, create the structure below.

Implement all required functionality in this task. Do not leave core functionality as TODOs, nonfunctional buttons, mocked network requests presented as real results, or placeholder API implementations.

---

# 1. Product Description

## What is FavvMenuz?

FavvMenuz is an AI-powered restaurant and menu discovery platform that allows users to find dishes based on natural-language requests, budget, cuisine, dietary preferences, ingredients, location and other relevant preferences.

Examples of queries:

- “Find spicy vegetarian food under ₹350 near Sector 62.”
- “I want something similar to paneer tikka but less oily.”
- “Show me Jain-friendly dinner options within 3 km.”
- “Find affordable Chinese food with vegetarian options.”
- “Suggest a filling dinner for two under ₹700.”
- “Find dishes without peanuts and exclude places where ingredient information is unavailable.”

The application turns these requests into structured search constraints, retrieves matching records from a relational database, ranks the results and presents grounded explanations.

The application is a discovery and recommendation product, **not a real ordering or delivery service**.

## Problem being solved

Conventional restaurant search often requires users to navigate many filters and compare individual menu items manually. Simple keyword search is poor at interpreting queries expressed in natural language.

FavvMenuz should bridge that gap by combining:
1. Structured restaurant and menu data.
2. Deterministic database filtering.
3. Geographic distance calculations.
4. Optional LLM-powered query interpretation.
5. Transparent relevance ranking.
6. A polished, interactive discovery interface.

## Data policy

We have not finalized an external dataset. Therefore, create a **completely synthetic, deterministic demo dataset**.

Do not scrape or copy actual restaurant listings, menus, prices, ratings, reviews or other proprietary content.

Create fictional restaurant names, fictional menu descriptions, synthetic prices and explicitly labelled demo ratings. Generate plausible coordinates around a synthetic Noida demo geography, using a small set of fictional localities and reference points.

Every synthetic record must be marked internally as demo data. The UI must visibly state that restaurants, menu information, prices, ratings and availability are simulated and are not real-world listings.

Do not claim that the app reflects real restaurant availability, live prices, actual user reviews or real ordering capabilities.

---

# 2. Mandatory Technology Stack

Use the following stack unless a genuine compatibility problem prevents it. If a compatibility issue occurs, choose the simplest compatible alternative and document it.

## Backend

- Python
- Django
- Django REST Framework
- Django's built-in authentication system
- Django ORM
- Pydantic for validating structured LLM outputs where appropriate
- Gunicorn as the production WSGI server
- `httpx` for outbound LLM API requests
- `django-redis` for Redis-backed caching
- PostgreSQL driver compatible with the selected Django version
- Pytest or Django's built-in testing framework for a small set of meaningful tests

Prefer a conventional Django project with separately organized applications. Do not build a collection of unnecessary microservices.

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Framer Motion or its maintained successor, if necessary
- `lucide-react` for icons
- React Router
- A lightweight API client built using the native Fetch API
- A sensible form validation approach without excessive dependencies

Pin compatible dependency versions, generate a lockfile, and ensure the build works from a clean installation.

## Database

Use PostgreSQL as the primary database.

Use ordinary latitude and longitude fields and calculate distances using the Haversine formula in Python for the small synthetic dataset. This is sufficient for the MVP and avoids the extra setup of PostGIS.

Keep database access through Django models and the ORM. Add reasonable indexes and constraints where appropriate.

Do not introduce MongoDB, Elasticsearch, a dedicated vector database or another database engine.

## Cache

Use a standalone Redis container via Docker Compose.

Use Redis for:
- Caching repeated query interpretations when safe.
- Caching anonymous search results for a short period.
- Avoiding redundant LLM calls for identical normalized queries.

Caching must fail gracefully. If Redis becomes unavailable, search should continue without caching wherever possible.

Never cache personalized responses across users. Define cache keys carefully, include relevant filters and dataset versioning where necessary, and use reasonable expiration times.

Do not add Celery or background workers for the initial MVP. Search and LLM interpretation can be synchronous with strict timeouts.

## LLM integration

Implement a provider abstraction around an OpenAI-compatible chat-completions endpoint.

Configuration must be supplied through environment variables:

- `LLM_PROVIDER`
- `LLM_BASE_URL`
- `LLM_API_KEY`
- `LLM_MODEL`
- `LLM_TIMEOUT_SECONDS`

Do not hardcode API keys, and do not assume a particular provider is always available.

The application must work without a paid LLM API key. Implement a deterministic rule-based query parser and clearly identify when fallback mode is being used.

When a key and provider configuration are available, the application should use the configured LLM to interpret natural-language searches.

Handle request timeouts, HTTP errors, rate limits, malformed JSON, unexpected fields and invalid schema output. Never make application startup depend on access to the LLM provider.

---

# 3. High-Level Architecture

Keep the application modular but deployable as a small number of Docker containers on a single Linux host.

The logical architecture must contain the following components.

## A. Frontend and presentation service

Responsibilities:
- Render the React user interface.
- Handle client-side routing and responsive layouts.
- Collect search queries and user preferences.
- Call the backend API.
- Manage transient UI state and display loading, empty, success and error states.
- Handle session-based authentication correctly.
- Show whether AI mode or deterministic fallback mode was used.

The frontend must not contain API secrets, database credentials, LLM API keys or privileged authorization logic.

## B. Django API and application service

Responsibilities:
- Expose REST endpoints.
- Validate requests and responses.
- Enforce permissions.
- Execute restaurant and menu searches.
- Manage saved favorites.
- Integrate the AI interpretation layer.
- Apply ranking and filtering rules.
- Coordinate database and cache access.
- Return predictable error responses.

Use Django REST Framework serializers and a consistent response/error convention. Keep views small and put business logic into reusable service modules.

## C. Authentication service

Implement authentication using Django's built-in user model and session authentication.

Required functionality:
- Registration.
- Login.
- Logout.
- Current-user endpoint.
- Password hashing using Django's standard authentication machinery.
- Session invalidation on logout.
- CSRF protection on unsafe requests.
- Authentication-required access to favorites and account-specific data.

The frontend and backend must share the same origin in the normal Docker deployment.

Use HttpOnly session cookies and appropriate production cookie security settings. Configure trusted hosts and CSRF origins correctly.

Do not store authentication tokens in localStorage. Do not build a custom authentication system.

OAuth login is not required for the MVP.

## D. AI/query interpretation service

Implement a dedicated logical service module responsible for converting natural-language text into a validated `SearchPlan`.

This service should:
1. Receive the user's query.
2. Invoke the configured LLM if enabled.
3. Request structured JSON matching the expected schema.
4. Validate the response.
5. Reject unsupported fields and invalid values.
6. Normalize the search plan.
7. Fall back to deterministic parsing when the LLM is missing or fails.
8. Return the normalized plan and the mode used.

The LLM must never generate executable SQL or control database access directly.

## E. Search and ranking service

Responsibilities:
- Apply hard constraints in the database.
- Filter menu items by price and dietary attributes.
- Match cuisines, dish names, ingredients and locality.
- Calculate distance when a location and radius are specified.
- Rank the remaining candidates.
- Generate deterministic match reasons.
- Return results with the facts used to support those reasons.

Hard constraints must not be relaxed silently to produce more results.

If no results match, explain that clearly and suggest which filters the user could change. Never claim a dish satisfies a dietary restriction unless the dataset explicitly supports that claim.

## F. Database service

PostgreSQL stores:
- Restaurant records.
- Menu items.
- Dietary attributes.
- User favorites.
- Any minimal user preferences needed by the product.

Use Django migrations, foreign keys, indexes and constraints.

## G. Cache service

Redis stores non-sensitive, short-lived cached data.

Keep Redis private to the Docker network. Do not expose it to the public internet.

## H. Logging and health service

Implement:
- A basic health endpoint.
- A readiness check that verifies database connectivity.
- A simple cache connectivity status.
- Standard application logging to stdout/stderr.
- Request correlation identifiers where practical.
- Error logging for failed LLM requests and fallback activation.
- Request-duration logging where useful for debugging.

Do not log passwords, session identifiers, API keys, authorization headers or unnecessary raw user prompts.

Do not implement a production monitoring platform, Prometheus, Grafana, a metrics dashboard or extensive p50/p95 reporting. This is a solo portfolio project.

Use Docker logs and basic AWS Lightsail monitoring as the default operational approach. CloudWatch integration can be added later if needed.

---

# 4. Required Repository Structure

Use the following structure and create all necessary files, configuration, package manifests and initialization files.

```text
FavvMenuz/
├── README.md
├── DEPLOY.md
├── .env.example
├── .gitignore
├── .dockerignore
├── docker-compose.yml
├── docker-compose.prod.yml
├── Makefile
│
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements.txt
│   ├── manage.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   └── apps/
│       ├── __init__.py
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   ├── apps.py
│       │   ├── urls.py
│       │   ├── views.py
│       │   └── tests.py
│       │
│       ├── catalog/
│       │   ├── __init__.py
│       │   ├── apps.py
│       │   ├── models.py
│       │   ├── admin.py
│       │   ├── serializers.py
│       │   ├── views.py
│       │   ├── urls.py
│       │   ├── services.py
│       │   ├── management/
│       │   │   ├── __init__.py
│       │   │   └── commands/
│       │   │       ├── __init__.py
│       │   │       └── seed_demo_data.py
│       │   └── tests.py
│       │
│       ├── accounts/
│       │   ├── __init__.py
│       │   ├── serializers.py
│       │   ├── views.py
│       │   ├── urls.py
│       │   ├── models.py
│       │   ├── services.py
│       │   └── tests.py
│       │
│       └── search/
│           ├── __init__.py
│           ├── serializers.py
│           ├── views.py
│           ├── urls.py
│           ├── models.py
│           ├── services.py
│           ├── ranking.py
│           ├── distance.py
│           ├── cache.py
│           ├── tests.py
│           │
│           └── ai/
│               ├── __init__.py
│               ├── schemas.py
│               ├── prompts.py
│               ├── provider.py
│               ├── parser.py
│               └── tests.py
│
├── frontend/
│   ├── Dockerfile
│   ├── Caddyfile
│   ├── package.json
│   ├── package-lock.json
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tsconfig.app.json
│   ├── eslint.config.js
│   │
│   ├── public/
│   │   ├── favicon.svg
│   │   └── logo.svg
│   │
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── vite-env.d.ts
│       ├── types/
│       │   ├── api.ts
│       │   ├── restaurant.ts
│       │   └── search.ts
│       ├── api/
│       │   ├── client.ts
│       │   ├── auth.ts
│       │   ├── restaurants.ts
│       │   ├── search.ts
│       │   └── favorites.ts
│       ├── hooks/
│       │   ├── useAuth.ts
│       │   ├── useSearch.ts
│       │   └── useFavorites.ts
│       ├── components/
│       │   ├── layout/
│       │   ├── search/
│       │   ├── restaurant/
│       │   ├── menu/
│       │   ├── auth/
│       │   ├── common/
│       │   └── ui/
│       ├── pages/
│       │   ├── HomePage.tsx
│       │   ├── SearchPage.tsx
│       │   ├── RestaurantPage.tsx
│       │   ├── FavoritesPage.tsx
│       │   ├── LoginPage.tsx
│       │   ├── RegisterPage.tsx
│       │   └── NotFoundPage.tsx
│       ├── styles/
│       │   └── index.css
│       └── utils/
│           ├── format.ts
│           └── validation.ts
│
├── scripts/
│   ├── backup_db.sh
│   └── restore_db.sh
│
└── .github/
    └── workflows/
        └── ci-cd.yml
```

You may add small supporting files where genuinely necessary, but avoid introducing directories or packages without a clear purpose.

Do not create files that are empty merely to match the structure. Every required file must have valid contents.

---

# 5. Data Model and Synthetic Dataset

Implement a sensible relational data model.

## Restaurant

Required fields:
- ID.
- Fictional name.
- Unique slug.
- Short description.
- Cuisine labels.
- Fictional locality.
- Latitude and longitude.
- Optional price band.
- Synthetic rating and review count.
- Synthetic-data flag.
- Creation and update timestamps.

## MenuItem

Required fields:
- ID.
- Restaurant foreign key.
- Name.
- Slug if needed.
- Category.
- Description.
- Price stored as integer paise.
- Ingredients as a structured list or appropriately normalized related data.
- Dietary tags.
- Spice level.
- Optional allergen information.
- Optional image asset path or supported local illustration identifier.
- Synthetic-data flag.
- Availability field representing simulated demo status only.

## Dietary information

Support explicit tags such as:
- Vegetarian.
- Vegan.
- Jain-friendly.
- Dairy-free.
- Gluten-free, if explicitly known in the synthetic record.

Allergen exclusions must be conservative. If the data cannot establish that a dish excludes an allergen, do not claim that it does.

## Favorites

Create a user-to-restaurant or user-to-menu-item relationship. Use a clear constraint to prevent accidental duplicate favorites.

Only the owning authenticated user may read or modify their favorites.

## Seed data command

Implement:

```bash
python manage.py seed_demo_data
```

Requirements:
- Create approximately 50 fictional restaurants.
- Create approximately 500–800 menu items.
- Include a mixture of Indian, Chinese, South Indian, Continental, dessert and beverage categories.
- Include realistic but synthetic price ranges.
- Include meaningful ingredient lists and dietary tags.
- Include sufficient variation for budget and dietary filtering.
- Use a fixed random seed.
- Generate plausible latitude/longitude values around fictional Noida localities.
- Produce diverse but consistent records.
- Ensure that repeated execution is deterministic and does not create duplicate records.
- Provide a clearly documented `--reset` option for destructive reseeding.

Do not create a default superuser with a hardcoded password.

Do not rely on the database having internet access to seed records.

## Synthetic imagery

The initial dataset is synthetic. Use a set of attractive, reusable local illustrations, SVGs, CSS compositions or bundled images with valid usage rights.

Do not make the entire UI depend on random image services or fragile external image URLs.

Use intentional imagery or illustrations for food categories, restaurant cards and empty states. Make image failures degrade gracefully.

---

# 6. Natural-Language Search and LLM

This is a central project feature. Implement it properly, but do not overcomplicate the AI infrastructure.

## SearchPlan schema

Create a validated schema capable of expressing:
- Search keywords.
- Cuisine preferences.
- Included ingredients.
- Excluded ingredients.
- Dietary tags.
- Minimum price.
- Maximum price.
- Spice preference.
- Requested locality.
- Maximum distance in kilometres.
- Sort preference.

Use nullable or optional fields where a user has not provided a constraint.

Constrain categorical fields to supported values. Enforce numeric limits and sensible defaults.

The LLM should output only this structured search plan. It must never invent actual search results or directly generate SQL.

## Example query interpretation

Input:

“Show me spicy vegetarian dishes below ₹350 near Sector 62.”

The resulting plan should represent:
- Vegetarian requirement.
- Maximum price of ₹350.
- High spice preference.
- Sector 62 locality.
- Relevant food keywords if present.
- Distance constraint only if the user specified a distance.

The final numeric and dietary constraints must be applied deterministically.

## Provider abstraction

The configured LLM adapter should:
- Make HTTP requests to the configured OpenAI-compatible endpoint.
- Use environment-based model and endpoint settings.
- Apply request timeouts.
- Validate returned JSON.
- Handle invalid output and HTTP failures.
- Avoid unbounded retries.
- Never log API keys.
- Return a predictable error or fallback result.

The deterministic fallback parser should understand common expressions for:
- Maximum and minimum price.
- Vegetarian and vegan preferences.
- Recognized cuisines.
- Supported localities.
- Common dish and ingredient keywords.
- Spice levels.
- Distance expressions.

If the parser cannot understand part of a query, ignore only the unrecognized part, display the active parsed filters and allow users to edit the filters manually.

Clearly display a small status indicator explaining whether the search used:
- AI-assisted interpretation.
- Rule-based fallback.

Do not pretend the LLM was used when it was not.

## Search pipeline

The pipeline must be:

1. Receive query and explicit filters.
2. Resolve user-supplied filters and query intent.
3. Validate the `SearchPlan`.
4. Apply hard filters through Django ORM queries.
5. Compute geographic distances for the bounded set of candidates.
6. Rank candidates deterministically.
7. Produce explanation text based on actual matched fields.
8. Return the resulting records and search-mode metadata.

A semantic embedding model is not required for the initial release.

Do not introduce a vector database or a complex multi-agent workflow.

## Ranking

Implement a simple explainable scoring function that prioritizes:
- Matches on requested dish names or ingredients.
- Cuisine preference matches.
- Preference and tag matches.
- Price suitability.
- Distance suitability where provided.
- Available synthetic rating data as a secondary factor.

Explicit constraints must always take priority over the ranking score.

If the user specifies a maximum price, do not return more expensive items merely because their relevance score is higher.

Explain match reasons using actual database fields—for example, “Matches your vegetarian preference and ₹350 budget.”

Do not let the LLM invent restaurant attributes, availability, ingredients, reviews or prices.

---

# 7. Backend API Requirements

Implement functional, documented endpoints.

Use the `/api/` namespace consistently.

## Health
- `GET /healthz/` — basic service health and database readiness.

## Restaurants and menu
- `GET /api/restaurants/` — paginated restaurant list, with useful filters.
- `GET /api/restaurants/<slug>/` — restaurant detail and its menu.
- `GET /api/menu-items/` — paginated menu search with deterministic filters.

## Search
- `POST /api/search/` — natural-language interpretation and discovery.
- `GET /api/search/suggestions/` — optional simple predefined query suggestions.

The search response should include:
- Parsed search plan.
- Search mode (`ai` or `fallback`).
- Results.
- Total result count where appropriate.
- Match reasons.
- A useful message for empty results.

Use consistent numeric and null representations. Ensure that money and dietary attributes have predictable serialization.

## Authentication
- `GET /api/auth/csrf/`
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/`

Implement CSRF token bootstrapping and safe session-cookie handling for the React frontend.

## Favorites
- `GET /api/favorites/`
- `POST /api/favorites/`
- `DELETE /api/favorites/<id>/`

Unauthenticated users must receive appropriate authentication errors for protected operations.

Do not trust user IDs supplied by the browser. Always use the authenticated server-side user.

Use pagination where collection endpoints need it. Validate all query parameters and request bodies.

---

# 8. UI Design — Strong Neo-Brutalist Visual Identity

The frontend must be a major strength of the project. Do not produce a bland dashboard template or a generic AI chat interface.

Use a polished, colorful **neo-brutalist food-discovery visual language** with a distinctive design system.

## Visual direction

Use:
- Warm cream or off-white backgrounds.
- Electric yellow accents.
- Tomato red or coral.
- Cobalt blue.
- Fresh green for selected status indicators.
- Thick black borders.
- Hard-offset shadows.
- Confident, large typography.
- Bold section headers.
- High-contrast buttons.
- Playful geometric elements.
- Large food cards and expressive illustrations.
- Deliberate whitespace to balance the visually rich aesthetic.

Suggested design direction: editorial food magazine meets modern neo-brutalist web app.

Avoid:
- Generic purple AI gradients as the entire design.
- Default unstyled HTML controls.
- Endless white cards with subtle shadows.
- Tiny typography.
- Excessive rounded-pill components everywhere.
- Overcrowded screens.
- Decorative UI elements that do not serve a purpose.

The application should feel designed specifically for discovering food.

## Landing and search page

Include:
- Distinctive FavvMenuz branding and a custom logo treatment.
- A strong headline describing natural-language food discovery.
- A large search box with a visible submit action.
- Example queries that users can click.
- A small set of useful filter controls.
- Visually interesting featured categories or curated demo collections.
- Popular demo dishes and restaurants.
- A clear synthetic-data notice.

## Search results

Include:
- Query summary.
- Editable filters.
- Number of results.
- Sort control.
- Results displayed as visually appealing restaurant or dish cards.
- Dietary indicators.
- Price.
- Cuisine.
- Distance if relevant.
- Synthetic rating clearly marked as a demo value.
- Match explanations.
- Save/favorite interactions.
- Loading skeletons.
- Useful empty-result suggestions.
- Retry UI for errors.

Users should be able to refine a search without losing their current context.

## Restaurant details

Include:
- A strong visual header.
- Fictional restaurant information.
- Cuisine and locality.
- Synthetic data indicator.
- Menu categories.
- Dish descriptions and price display.
- Dietary labels and supported ingredients.
- Related dishes.
- Favorite action.

## Authentication

Create visually consistent login and registration pages.

Display validation errors clearly, use accessible labels, disable submitting buttons while requests are in progress and handle server errors without losing user-entered information.

## Favorites

Build a working saved-items page for authenticated users with:
- Saved restaurants and/or dishes.
- Removal actions.
- Helpful empty state.
- Authentication-aware navigation.

## Animation and interaction

Use Framer Motion or a compatible maintained library for:
- Entrance and staggered card animations.
- Page transitions.
- Filter and dialog transitions.
- Buttons and hover states.
- Search-result state transitions.
- Lightweight decorative animation.

Animations should enhance the experience and remain responsive. Respect `prefers-reduced-motion`. Avoid continuously running large animations that slow the application.

## Responsive design

The app must work at:
- 360px mobile width.
- Tablet width.
- Typical laptop width.
- Large desktop width.

Use mobile-first layouts, responsive grids, sensible navigation and appropriately sized touch targets.

Mobile responsiveness is mandatory. PWA installation and offline caching are not required for the initial release.

## Accessibility

Provide:
- Semantic HTML.
- Keyboard navigation.
- Focus-visible styles.
- Sufficient color contrast.
- Accessible form labels.
- Useful alt text.
- Reduced-motion support.
- Clear error messages.

## Frontend implementation quality

- Use reusable, typed React components.
- Centralize API calls.
- Use environment-independent relative API paths.
- Avoid `any` unless justified.
- Avoid large all-in-one components.
- Avoid unnecessary frontend state libraries.
- Handle loading, error and empty states.
- Use the proper authentication/session flow.
- Do not store API keys in frontend environment variables.
- Do not display fake results after failed API requests.

Use lucide-react icons consistently. Build reusable buttons, inputs, cards, badges, dialogs and layout primitives where useful.

---

# 9. Authentication and Security Rules

Implement the following security requirements without introducing unnecessary identity services:

1. Use Django's built-in authentication and secure password hashing.
2. Use session authentication for the same-origin web application.
3. Use CSRF protection for state-changing requests.
4. Mark production session cookies HttpOnly and Secure, and use appropriate SameSite settings.
5. Never disable CSRF globally to make the frontend work.
6. Validate host headers and configure trusted origins explicitly.
7. Keep secrets in environment variables.
8. Commit only `.env.example`, never `.env`.
9. Keep database and Redis ports private.
10. Add reasonable request-size and LLM-timeout limits.
11. Validate all incoming data.
12. Add lightweight throttling for the LLM-backed search endpoint using available Django/DRF mechanisms or Redis-backed counters.
13. Protect admin-only operations.
14. Prevent one user from accessing another user's favorites.
15. Do not log authentication secrets or full authorization headers.
16. Ensure synthetic data is clearly separated from user-specific data.
17. Avoid unnecessary collection of personal information.

For a public demo, browsing and searching must work without registration. Require a session only for account features.

---

# 10. Docker and Local Development

Create working Dockerfiles and Compose configurations.

## Backend Dockerfile

Use a suitable pinned Python base image.

Requirements:
- Install dependencies from `requirements.txt`.
- Use a non-root application user in the runtime image where practical.
- Set the working directory.
- Expose only the internal application port.
- Run the app with Gunicorn.
- Do not put secrets in image layers.
- Support environment-based configuration.
- Include proper signal handling.

## Frontend Dockerfile

Use a multi-stage build:
1. Build React assets with Node.
2. Serve the generated frontend using Caddy.

The final image must not ship the Node development toolchain unnecessarily.

## Caddy

Use Caddy to:
- Serve the frontend.
- Proxy `/api/*` and authentication routes to Django.
- Proxy Django admin routes.
- Proxy Django static assets correctly.
- Provide SPA fallback routing for frontend paths.
- Enable automatic HTTPS when a real domain is configured.
- Support local HTTP development without needing a domain.

Verify that `/admin/`, API requests, frontend deep links and static assets all work through the proxy.

## Docker Compose

The main application stack should contain only:
- `frontend` — production-built frontend served by Caddy.
- `backend` — Django/Gunicorn API.
- `db` — PostgreSQL.
- `redis` — cache.

Use persistent storage for PostgreSQL. Redis persistence is optional because the cache can be recreated.

Do not publish database or Redis ports to the public host in production.

Use service health checks and appropriate startup dependencies. Avoid brittle fixed sleep commands to wait for dependencies.

Add restart policies appropriate for the deployment.

Create `docker-compose.prod.yml` for production differences, including:
- Production host and cookie settings.
- Production ports.
- Caddy certificate/data volumes.
- Debug disabled.
- Production secret configuration.
- Appropriate restart policies.

Avoid making the production Compose file accidentally expose the database, Redis or Django debug server.

## Local developer workflow

The following workflow must be supported and documented:

```bash
cp .env.example .env
docker compose up --build -d
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_demo_data
docker compose exec backend python manage.py createsuperuser
```

The application should then be accessible locally at the configured URL, documented clearly in README.md.

The UI must work without configuring an LLM API key, using the deterministic fallback parser.

Provide useful Makefile shortcuts such as:

```bash
make up
make down
make logs
make migrate
make seed
make test
make createsuperuser
```

Every shortcut must invoke a real working command.

---

# 11. Environment Configuration

Create `.env.example` at the repository root.

Include documented placeholder variables for:
- Django secret key.
- Debug mode.
- Allowed hosts.
- CSRF trusted origins.
- PostgreSQL database name.
- PostgreSQL user.
- PostgreSQL password.
- Database host and port or a documented database URL convention.
- Redis URL.
- LLM provider.
- LLM base URL.
- LLM API key.
- LLM model.
- LLM timeout.
- Site address/domain.
- Session-cookie security flags.
- Any additional configuration genuinely required.

Use one consistent environment-variable naming convention throughout the entire project.

Support local Compose service names for the database and Redis. Production configuration must work when these services run as containers on the same Docker network.

Do not create a second incompatible environment configuration format.

Provide a reliable way to generate a Django secret key. Use clear documentation for the required commands.

When LLM credentials are missing, the app must start and function in fallback mode.

The README must explain that a third-party LLM API key may incur separate charges and that natural-language query content may be sent to the configured provider when AI mode is enabled.

Do not put real credentials or production `.env` files in GitHub.

---

# 12. Minimal Testing and Build Checks

This is a solo hobby and resume project, not a mission-critical financial system. Do not overengineer the test suite.

Implement a small, meaningful set of automated tests covering the main risk areas.

At minimum, verify:
- Health endpoint and basic database connectivity.
- Restaurant/menu search and pagination.
- Price constraints are respected.
- Dietary constraints are respected using explicit tags.
- Search still works when the LLM is disabled.
- Invalid LLM output does not crash the API.
- Session authentication works.
- Favorites are protected against cross-user access.
- Synthetic seeding is repeatable.

Keep the number of test cases modest and their purpose clear. Use fixtures or factories efficiently; do not require hundreds of synthetic cases for test coverage.

Do not build extensive mocks for every internal function or pursue a specific arbitrary code-coverage percentage.

For frontend checks, ensure:
- TypeScript type checking passes.
- ESLint passes.
- Production frontend build succeeds.

The main success criterion is that the app works end to end—not that it has a huge testing framework.

Do not implement load testing or p50/p95 benchmarking in the mandatory MVP.

---

# 13. GitHub Actions: CI and Deployment

Create a functional workflow under:

`.github/workflows/ci-cd.yml`

It must handle automated build/check and deployment workflows.

## CI triggers

Run on:
- Pull requests to `main`.
- Pushes to `main`.

## CI jobs

### Backend checks

- Set up a supported Python version.
- Install the backend dependencies.
- Start PostgreSQL and Redis services for integration tests.
- Configure test environment variables without real secrets.
- Run Django system checks.
- Verify that committed migrations are consistent with the models.
- Run the small backend test suite.

### Frontend checks

- Set up Node.
- Run `npm ci`.
- Run TypeScript checks.
- Run ESLint.
- Run the production build.

### Container validation

Build the backend and frontend Docker images to catch container-specific errors.

Do not push images to a registry unless the implementation genuinely needs one. The default deployment should not require ECR or another container registry.

## Deployment target

Deploy to a single AWS Lightsail Linux instance running Docker Compose.

Use GitHub Actions SSH deployment.

Deployment must occur only after the CI checks pass and only for the trusted `main` branch or an explicit production deployment trigger.

Use GitHub Actions secrets/environment variables for:
- Lightsail host.
- SSH username.
- SSH private key.
- Verified SSH known-hosts entry.
- Any additional necessary deployment configuration.

Use a `production` GitHub Actions environment if appropriate.

Do not disable SSH host-key verification. Do not execute deployment using unverified `ssh-keyscan` output produced during the deployment run.

Deployment steps should:
1. Connect to the configured host.
2. Transfer or update the project source.
3. Preserve the host's production `.env` file.
4. Build or rebuild images.
5. Start the database/cache services if needed.
6. Apply migrations.
7. Collect static assets where required.
8. Run the synthetic data seed idempotently.
9. Restart/update application containers.
10. Perform a basic HTTP health check.
11. Print useful diagnostic information if deployment fails.

Do not dump secrets into CI logs. Do not copy the production `.env` file from the runner.

Use a straightforward update strategy. Document that it is a single-host deployment and not a zero-downtime rolling deployment platform.

The workflow must be syntactically valid and its deployment commands must correspond exactly to the files and Compose services actually created.

---

# 14. AWS Deployment Strategy

Use **one AWS Lightsail Linux instance with Docker Engine and Docker Compose**.

Do not require:
- ECS or EKS.
- RDS.
- ElastiCache.
- ECR.
- A load balancer.
- A separate managed database.
- A separate object-storage service for the initial release.
- Dedicated monitoring infrastructure.

Run the frontend/Caddy, Django, PostgreSQL and Redis containers on the same host.

This is an appropriate architecture for a hobby/resume application with synthetic catalogue data. Document its trade-offs honestly: the database, cache and web application share one host, and there is no high availability or automatic horizontal scaling.

## Production configuration

- Use `DEBUG=False`.
- Generate a strong secret key.
- Use a strong PostgreSQL password.
- Store `.env` only on the server with restrictive file permissions.
- Expose ports 80 and 443 publicly.
- Restrict SSH port 22 to the developer's IP if practical.
- Keep database and Redis private.
- Use a static IP for the instance if needed.
- Configure a domain's DNS record to point at the instance when using automatic HTTPS.
- Use Caddy-managed TLS for the configured domain.
- Configure secure cookies for HTTPS deployment.
- Set `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` to valid values.
- Configure Docker restart policies.
- Provide a database backup and restoration procedure.

If a real domain is unavailable, document the local/IP-only limitations clearly rather than suggesting an insecure public login configuration.

## Database backups

Create simple `backup_db.sh` and `restore_db.sh` scripts.

They should:
- Create and restore PostgreSQL dumps.
- Require deliberate confirmation or an explicit argument before destructive restoration.
- Avoid printing database passwords.
- Document where backups are stored.
- Explain that a backup stored only on the same instance is not sufficient protection against instance loss.

Do not introduce mandatory S3 backup automation. Document an external backup as a manual operational precaution and leave automated off-host backups optional.

---

# 15. README.md Requirements

README.md is a primary project deliverable, not an afterthought.

Write it in this order.

## 1. Project introduction

Begin with a clear explanation of:
- What FavvMenuz is.
- Why it exists.
- What problems it solves.
- How natural-language restaurant/menu discovery works.

A reader must understand the product before seeing installation commands.

## 2. Features

List implemented features clearly, distinguishing core functionality from future ideas.

## 3. Screenshots or visual preview

Provide a section with appropriate image placeholders or instructions for adding screenshots after deployment. Do not include fabricated screenshot links.

## 4. Technology stack

Explain the purpose of Django, React, PostgreSQL, Redis, the LLM adapter, Docker, Caddy and AWS Lightsail.

## 5. Architecture

Provide a readable Mermaid diagram showing:

React UI / Caddy → Django API → search services → PostgreSQL

Also show the LLM provider and Redis cache as supporting components.

## 6. Repository structure

Document the major root, backend and frontend directories.

## 7. Prerequisites

List required software and versions, including Docker Engine, Docker Compose, Git and optional LLM API credentials.

## 8. Local setup

Provide complete copy-paste commands to clone, configure, build and start the application.

Explain migrations, seeding and superuser creation.

## 9. Configuration

Document every `.env.example` variable and whether it is required.

Explain:
- Django secret key generation.
- Database settings.
- Redis settings.
- LLM provider configuration.
- What happens when the API key is not configured.
- How to avoid leaking keys into Git.

## 10. Using the application

Describe browsing, example queries, filters, restaurant pages, favorites and authentication.

## 11. API reference

List core API endpoints and representative request/response examples.

## 12. Testing and quality checks

Give commands for backend tests, Django checks, frontend type checking, ESLint and production builds.

## 13. Synthetic data

Explain how the demo data is generated, how to reseed it, and why records do not represent real restaurants or live prices.

## 14. Security notes

Explain the session/CSRF mechanism, production secrets, public ports and limitations of a one-host deployment.

## 15. Limitations and future enhancements

Keep this section honest and do not claim unfinished features exist.

---

# 16. DEPLOY.md Requirements

Create a separate, detailed deployment manual titled `DEPLOY.md`.

It must enable a solo developer to deploy the application to AWS Lightsail without guessing missing steps.

Include these sections in order.

## 1. Deployment architecture

Explain the single-host Docker Compose architecture and its limitations.

## 2. AWS prerequisites

Explain:
- Creating a suitable Linux Lightsail instance.
- Attaching a static IP.
- Configuring firewall rules.
- Setting up SSH access.
- Connecting a domain if available.

Do not hardcode region-dependent pricing or promise a particular free-tier entitlement.

## 3. Install Docker and Compose

Provide OS-appropriate commands for the documented server OS, including verification steps.

## 4. Prepare the server

Create the application directory, install required tools, configure ownership and place the project files.

## 5. Configure production environment

Explain every required production `.env` value, permissions, secure secret generation, production host settings, HTTPS and cookie flags.

Do not commit or upload the production `.env` file through Git.

## 6. Deploy manually

Provide commands to build and start services, run database migrations, collect static files, seed demo data, create an administrator and verify the deployment.

Commands must match the actual Compose service names and configuration.

## 7. HTTPS and DNS

Explain how Caddy obtains and renews certificates, what domain configuration is needed, and what happens when no domain is configured.

## 8. GitHub Actions deployment

Explain how to set up the workflow and its repository/environment secrets, the expected SSH user and known-hosts configuration, and how deployment is triggered.

Explain how to restrict deployment to the trusted branch.

## 9. Operations

Include commands for:
- Checking application status.
- Viewing logs.
- Restarting services.
- Updating code.
- Applying migrations.
- Reseeding data.
- Running tests.
- Backing up the database.
- Restoring a backup.
- Diagnosing common startup, database, Redis and LLM errors.

## 10. Cost and security notes

Explain that Lightsail, LLM inference and other external services may incur costs. Tell the developer to check current pricing, monitor usage and remove unused resources.

Explain that the one-host deployment is suitable for a hobby/resume demo, not high availability or a production food-ordering platform.

---

# 17. Code Quality and Maintainability

Apply these requirements throughout the repository.

- Use type hints where appropriate.
- Keep modules cohesive.
- Avoid circular imports.
- Avoid giant views, components and settings files where responsibilities can be separated cleanly.
- Use reusable service functions.
- Handle external API errors.
- Validate data at boundaries.
- Use migrations rather than modifying schemas manually.
- Follow consistent formatting and naming.
- Avoid dead code and unnecessary dependencies.
- Keep secrets out of source control.
- Include `.gitignore` entries for `.env`, Python caches, virtual environments, Node modules, build output, logs and local backups.
- Ensure all documented commands are valid.
- Avoid importing packages that are not included in dependency files.
- Generate a valid lockfile.
- Handle empty results and failed requests intentionally.

Do not add a message queue, separate microservices, event bus, vector database, OAuth provider, telemetry platform or other infrastructure without a clear MVP requirement.

---

# 18. Optional Features

The following are explicitly optional. Do not let them delay or compromise the required MVP.

Implement them only if all mandatory requirements are working and sufficient time remains.

1. **PWA support:** installable app, app manifest and limited offline shell support.
2. **Google OAuth:** optional sign-in through a trusted provider.
3. **Semantic retrieval:** text embeddings and `pgvector` after establishing a keyword-search baseline.
4. **Personalized recommendations:** ranking adjustments based on user favorites and preferences.
5. **Map visualization:** use a compatible mapping library if a genuinely useful demo map can be added without mandatory paid API keys.
6. **CloudWatch logging:** optional centralized logs if the app grows beyond the basic Lightsail deployment.
7. **Scheduled off-host backups:** optional S3 or another suitable backup destination.
8. **Celery:** introduce only if genuine asynchronous tasks later justify a worker service.
9. **Advanced evaluation:** labelled relevance datasets, offline ranking comparisons and more extensive search benchmarks.
10. **Admin analytics:** basic counts of searches and popular filters, provided no unnecessary personal query data is stored.
11. **Semantic explanations:** richer AI-generated explanations, subject to strict grounding in retrieved data.

Keep these out of the critical startup path. There must be no broken placeholder controls for features that have not been implemented.

---

# 19. Final Implementation and Verification Checklist

Before declaring the project complete, verify the following.

## Application
- [ ] Django starts without errors.
- [ ] PostgreSQL is initialized through Compose.
- [ ] Redis can be used for caching.
- [ ] The synthetic seed command runs repeatedly without creating duplicates.
- [ ] Restaurant listing and detail endpoints work.
- [ ] Search works with structured filters.
- [ ] Natural-language query parsing works with a configured LLM.
- [ ] Fallback search works without an LLM key.
- [ ] Invalid provider output does not crash the service.
- [ ] Search results respect price and dietary constraints.
- [ ] Session authentication and CSRF protection work.
- [ ] Favorites are saved persistently and properly access-controlled.
- [ ] The admin interface works.
- [ ] The application gives understandable errors when dependencies fail.

## Frontend
- [ ] The UI is visually polished and recognizably neo-brutalist.
- [ ] The landing, search, restaurant, favorites, login and registration pages work.
- [ ] No important buttons are decorative-only.
- [ ] The search form submits to the actual backend.
- [ ] Loading, empty and error states work.
- [ ] Responsive layouts work at mobile, tablet and desktop sizes.
- [ ] The interface is accessible and respects reduced-motion preferences.
- [ ] Synthetic data is clearly labelled.

## Engineering
- [ ] Database migrations exist and can run from a clean database.
- [ ] The focused backend tests pass.
- [ ] Django system checks pass.
- [ ] Frontend type checking, ESLint and production build pass.
- [ ] Docker images build from a clean state.
- [ ] Compose services communicate through private networks.
- [ ] Health checks work.
- [ ] No real credentials are committed.

## Documentation and deployment
- [ ] README.md covers the project, features, structure, local use, configuration, tests and limitations.
- [ ] DEPLOY.md provides executable, end-to-end deployment instructions.
- [ ] `.env.example` contains all required variables with safe placeholders.
- [ ] GitHub Actions implements CI and the intended deployment workflow.
- [ ] Production deployment preserves `.env`.
- [ ] Database backup and restore commands are documented.
- [ ] Production configuration does not expose database or Redis ports.
- [ ] HTTPS, trusted hosts and cookies are configured correctly for a real domain.

## Final instruction

Work directly in the workspace and implement the complete project, rather than returning this checklist as a plan.

Perform the available checks, fix errors you discover, and verify that code, Docker configuration, tests, GitHub Actions, README.md and DEPLOY.md agree with each other.

If a real external service cannot be contacted because credentials or AWS infrastructure are unavailable, implement its integration, validate the relevant configuration and provide exact setup instructions. Do not claim that a deployment or external integration was actually exercised when it was not.

At completion, provide a concise engineering handoff with:
- What was implemented.
- The exact local startup commands.
- The required environment configuration.
- The test/build commands and their actual results.
- How to deploy through GitHub Actions.
- Any unresolved issues or external setup steps.

Prioritize a **working, coherent, visually polished and reproducibly deployable MVP** over adding extra technologies or claiming production-scale capabilities.