# Synthetic User Persona Swarm
### AI-Powered Product Testing & Market Validation Platform

<p align="center">
  <strong>Simulating consumer perspectives to evaluate products before they reach the market.</strong>
</p>

---

## 1. Overview

Synthetic User Persona Swarm is an AI-powered product testing and market validation platform that simulates how different consumer segments might perceive, evaluate, and respond to a product.

Traditional market research, surveys, and user testing can be expensive, time-consuming, and limited by the number and diversity of participants. Products are often launched without adequately understanding the preferences, expectations, and purchasing behaviours of different target audiences.

This project addresses that challenge by generating diverse synthetic consumer personas and deploying independent AI agents to evaluate products from their respective perspectives.

The platform aggregates these evaluations into structured analytics, helping users identify potential target audiences, understand consumer preferences, evaluate pricing strategies, and discover opportunities for product improvement.

**Important:** The platform produces simulated consumer insights, not actual market research results or statistically validated predictions of real-world purchasing behaviour.

## 2. Key Features

### 2.1 Product Intelligence
- Submit products with descriptions, features, pricing, and category information.
- Define target audiences and intended market segments.
- Support product comparisons and alternative product configurations.

### 2.2 Synthetic Persona Generation
Generate diverse consumer profiles with characteristics such as:

- Age and demographics
- Occupation and income level
- Interests and lifestyle
- Personality traits
- Technical literacy
- Spending habits
- Brand loyalty
- Price sensitivity
- Purchasing motivations

### 2.3 Multi-Agent Consumer Simulation
- Create independent AI agents based on generated personas.
- Evaluate products from different consumer perspectives.
- Generate individual product feedback.
- Capture positive and negative product perceptions.
- Evaluate purchase intent and price acceptance.
- Execute multiple evaluations concurrently.

### 2.4 Market Evaluation & Analytics
- Calculate overall product appeal.
- Evaluate purchase intent.
- Analyze price acceptance.
- Identify preferred product features.
- Compare responses across demographic groups.
- Generate actionable product recommendations.

### 2.5 Interactive Analytics Dashboard
- Visualize product performance.
- Compare age-wise and interest-wise responses.
- Display consumer sentiment distributions.
- Explore individual persona evaluations.
- View pricing analysis and recommendations.

### 2.6 Advanced Testing (Planned)
- A/B product testing.
- Competitor comparison.
- Price optimization experiments.
- Advertisement evaluation.
- Website and UX testing.
- Regional consumer analysis.
- Multi-persona discussion and debate.

---

## 3. System Architecture

The platform follows a modular architecture consisting of five major stages.

```mermaid
flowchart TD
    A[User Submits Product] --> B[Product Analysis]
    B --> C[Persona Generator]
    C --> D[Generate Synthetic Consumers]
    D --> E[Multi-Agent Simulation]

    E --> F1[Consumer Agent 1]
    E --> F2[Consumer Agent 2]
    E --> F3[Consumer Agent 3]
    E --> F4[Consumer Agent N]

    F1 --> G[Response Collector]
    F2 --> G
    F3 --> G
    F4 --> G

    G --> H[Scoring & Evaluation Engine]
    H --> I[Segment Analysis]
    H --> J[Pricing Analysis]
    H --> K[Recommendation Engine]

    I --> L[Final Market Intelligence Report]
    J --> L
    K --> L

    L --> M[Interactive Dashboard]
```

### Module Responsibilities

| Module | Responsibility |
|---|---|
| Product Intelligence | Processes submitted product information |
| Persona Generator | Creates diverse synthetic consumer profiles |
| Agent Engine | Simulates independent consumer evaluations |
| Simulation Engine | Coordinates parallel agent execution |
| Evaluation Engine | Calculates scores and analyzes responses |
| Dashboard | Displays results and market insights |

---

## 4. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Next.js, React, TypeScript | User interface |
| Styling | Tailwind CSS, shadcn/ui | UI components and styling |
| Backend | Python, FastAPI | API and application logic |
| Data Validation | Pydantic v2 | Structured data validation |
| AI Integration | Gemini API / OpenAI API | Persona reasoning and evaluations |
| Agent Execution | Python asyncio / LangGraph | Multi-agent orchestration |
| Database | PostgreSQL | Persistent data storage |
| ORM | SQLAlchemy | Database operations |
| Analytics | Pandas, NumPy | Data processing and scoring |
| Visualization | Recharts | Interactive charts |
| Testing | Pytest, Vitest | Automated testing |
| Deployment | Vercel, Render / Railway | Application hosting |

The initial implementation will use a single LLM provider behind a provider-independent interface, allowing the model to be changed without rewriting the agent architecture.

---

## 5. Repository Structure

The project follows a monorepo architecture, maintaining the frontend, backend, AI engine, shared contracts, and documentation in a single GitHub repository.

```text
persona-pulse/
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   ├── dashboard/
│   │   ├── products/
│   │   └── simulations/
│   │
│   ├── components/
│   │   ├── product/
│   │   ├── personas/
│   │   ├── analytics/
│   │   └── common/
│   │
│   ├── lib/
│   ├── hooks/
│   ├── types/
│   ├── public/
│   ├── package.json
│   └── tsconfig.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── database/
│   │   └── utils/
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── pyproject.toml
│
├── ai_engine/
│   ├── personas/
│   ├── agents/
│   ├── simulation/
│   ├── evaluation/
│   ├── prompts/
│   ├── llm/
│   └── tests/
│
├── contracts/
│   ├── product.schema.json
│   ├── persona.schema.json
│   ├── simulation_request.schema.json
│   ├── simulation_result.schema.json
│   └── report.schema.json
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API_CONTRACT.md
│   ├── DATABASE_SCHEMA.md
│   ├── PERSONA_DESIGN.md
│   └── CONTRIBUTING.md
│
├── sample_data/
│   ├── products/
│   ├── personas/
│   └── simulations/
│
├── scripts/
│   ├── seed_database.py
│   └── generate_demo.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

### Directory Ownership

| Directory | Purpose |
|---|---|
| `frontend/` | User interface and dashboard |
| `backend/` | APIs, database, and application orchestration |
| `ai_engine/personas/` | Persona generation and validation |
| `ai_engine/agents/` | Consumer agent implementation |
| `ai_engine/llm/` | LLM provider integrations |
| `ai_engine/prompts/` | AI system prompts |
| `ai_engine/simulation/` | Simulation orchestration |
| `ai_engine/evaluation/` | Scoring and analytics |
| `contracts/` | Shared JSON schemas |
| `docs/` | Technical documentation |
| `sample_data/` | Test products, personas, and simulation data |

---

## 6. Team Structure & Task Allocation

The project is divided among four members, with each member responsible for an independent module.

### Person 1 — Frontend & UI/UX Development

**Ownership:** `frontend/`

Responsibilities:

1. Develop the landing page and application layout.
2. Build product submission forms.
3. Implement target audience selection.
4. Display generated personas.
5. Develop simulation progress interfaces.
6. Build the analytics dashboard.
7. Visualize product performance using charts.
8. Display individual persona feedback.
9. Integrate frontend components with backend APIs.

**Primary Technologies:**
- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- Recharts

**Deliverable:** A complete user interface capable of submitting products, initiating simulations, and displaying generated reports.

### Person 2 — Backend, Database & Integration

**Ownership:** `backend/`, `contracts/`, shared integration

Responsibilities:

1. Set up the FastAPI application.
2. Configure PostgreSQL and SQLAlchemy.
3. Design and implement database models.
4. Develop product CRUD operations.
5. Implement persona and simulation endpoints.
6. Connect the backend to the AI engine.
7. Connect simulation outputs to the evaluation engine.
8. Manage simulation status and progress.
9. Store generated personas, responses, and reports.
10. Handle API validation and error management.

**Primary Technologies:**
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Alembic

**Deliverable:** A functioning backend that coordinates all modules and provides consistent APIs.

### Person 3 — AI Persona Generation & Multi-Agent Engine

**Ownership:** `ai_engine/personas/`, `ai_engine/agents/`, `ai_engine/llm/`, `ai_engine/prompts/`

Responsibilities:

1. Design the synthetic persona data model.
2. Develop persona generation algorithms.
3. Create reusable persona archetypes.
4. Implement controlled demographic and behavioural variation.
5. Develop persona validation mechanisms.
6. Implement the base consumer agent.
7. Develop the agent factory.
8. Integrate the selected LLM provider.
9. Design prompts for independent product evaluation.
10. Ensure structured and consistent agent responses.

**Primary Technologies:**
- Python
- Gemini API / OpenAI API
- Pydantic
- asyncio

**Deliverable:** An AI engine capable of generating diverse synthetic consumers and simulating independent product evaluations.

### Person 4 — Simulation Orchestration, Scoring & Analytics

**Ownership:** `ai_engine/simulation/`, `ai_engine/evaluation/`

Responsibilities:

1. Develop the simulation manager.
2. Implement concurrent agent execution.
3. Collect and validate agent responses.
4. Track simulation progress and failed evaluations.
5. Develop the scoring engine.
6. Perform demographic and behavioural segmentation.
7. Implement sentiment analysis.
8. Develop pricing analysis.
9. Generate product recommendations.
10. Produce structured market intelligence reports.

**Primary Technologies:**
- Python
- asyncio
- Pandas
- NumPy
- Pydantic

**Deliverable:** An evaluation engine that converts individual synthetic consumer responses into structured product insights and analytics.

### Team Allocation Summary

| Module | Person 1 | Person 2 | Person 3 | Person 4 |
|---|---|---|---|---|
| Frontend | Owner | — | — | — |
| Backend | — | Owner | — | — |
| Database | — | Owner | — | — |
| API Contracts | Review | Maintainer | Review | Review |
| Persona Generation | — | — | Owner | — |
| Agent Development | — | — | Owner | — |
| LLM Integration | — | — | Owner | — |
| Simulation Execution | — | Integration | — | Owner |
| Scoring & Analytics | — | Integration | — | Owner |
| Documentation | Contribute | Maintainer | Contribute | Contribute |

**Ownership rule:** Each member works primarily within their assigned directories. Changes to shared contracts or interfaces must be discussed and approved by the affected module owners.

---

## 7. Shared Integration Contracts

All modules must follow standardized data formats to ensure seamless integration.

The JSON schemas in `contracts/` serve as the source of truth for communication between modules.

### 7.1 Product Schema

File: `contracts/product.schema.json`

A product contains:

- `product_id`
- `name`
- `description`
- `category`
- `price`
- `currency`
- `features`
- `target_audience`

### 7.2 Persona Schema

File: `contracts/persona.schema.json`

Each persona contains:

- `persona_id`
- `name`
- `age`
- `occupation`
- `income_level`
- `interests`
- `personality_traits`
- `price_sensitivity`
- `technical_literacy`
- `brand_loyalty`
- `purchase_impulsiveness`
- `primary_motivation`

Behavioural scores are normalized between 0 and 1.

### 7.3 Simulation Request

File: `contracts/simulation_request.schema.json`

Example:

```json
{
  "product_id": "PROD001",
  "persona_count": 100,
  "audience_config": {
    "age_groups": ["18-24", "25-34"],
    "interests": ["fitness", "technology"]
  },
  "evaluation_categories": [
    "appeal",
    "purchase_intent",
    "price_acceptance"
  ],
  "pricing_scenarios": [2999, 3999, 4999]
}
```

### 7.4 Individual Agent Response

File: `contracts/simulation_result.schema.json`

Example:

```json
{
  "persona_id": "P001",
  "interest_score": 85,
  "purchase_intent": 62,
  "price_acceptance": 45,
  "perceived_usefulness": 90,
  "design_appeal": 80,
  "would_recommend": true,
  "positive_factors": [
    "Useful fitness tracking",
    "Good battery life"
  ],
  "negative_factors": [
    "Price is high for a student"
  ],
  "reasoning": "The features are useful, but I would wait for a discount."
}
```

### 7.5 Final Report

File: `contracts/report.schema.json`

The final report includes:

- `simulation_id`
- `overall_score`
- `metrics`
- `segment_analysis`
- `pricing_analysis`
- `sentiment_distribution`
- `recommendations`
- `limitations`

All modules must use the same field names and data types. Any changes to these schemas must be communicated before implementation.

---

## 8. Internal Function Interfaces

The following function signatures define how the modules communicate internally.

| Module | Function | Expected Output |
|---|---|---|
| Persona Engine | `generate_personas()` | List of persona profiles |
| Persona Engine | `create_agents()` | List of consumer agents |
| Agent Engine | `evaluate_product()` | Individual agent response |
| Simulation Engine | `run_simulation()` | Collected simulation responses |
| Evaluation Engine | `calculate_scores()` | Overall score dictionary |
| Evaluation Engine | `analyze_segments()` | Segment-wise analysis |
| Evaluation Engine | `generate_report()` | Final structured report |
| Backend | `run_product_simulation()` | Simulation result |

### Example Persona Generator Interface

```python
class PersonaGenerator:

    def generate_personas(
        self,
        audience_config: dict,
        count: int
    ) -> list[dict]:
        pass
```

### Example Consumer Agent Interface

```python
class ConsumerAgent:

    def __init__(self, persona, llm):
        self.persona = persona
        self.llm = llm

    async def evaluate_product(self, product):
        pass
```

### Example Simulation Manager Interface

```python
class SimulationManager:

    async def run(
        self,
        product: dict,
        agents: list,
        simulation_id: str
    ) -> dict:
        pass
```

### Example Scoring Engine Interface

```python
class ScoringEngine:

    def calculate_scores(
        self,
        responses: list[dict]
    ) -> dict:
        pass
```

### Backend Integration Interface

```python
async def run_product_simulation(
    product_id: str,
    target_audience: dict,
    num_personas: int
) -> dict:
    pass
```

Person 2 is responsible for integrating these functions into the backend workflow.

---

## 9. Scoring Methodology

The platform evaluates products using multiple independent metrics.

| Metric | Description |
|---|---|
| Product Appeal | Overall attractiveness of the product |
| Purchase Intent | Stated likelihood of purchasing |
| Price Acceptance | Perceived acceptability of pricing |
| Perceived Usefulness | Perceived utility of product features |
| Design Appeal | Aesthetic and design preferences |
| Recommendation Intent | Willingness to recommend the product |

An initial composite score can be calculated using:

\[
S=0.25A+0.25P+0.20C+0.15U+0.15D
\]

Where:

- A = Product Appeal
- P = Purchase Intent
- C = Price Acceptance
- U = Perceived Usefulness
- D = Design Appeal

All individual metrics are normalized between 0 and 100.

The resulting score represents simulated product readiness based on the generated population. It should not be interpreted as a validated probability of commercial success.

### Segment Analysis

The system should calculate scores independently for different consumer groups.

Examples:

- Age groups
- Income categories
- Occupations
- Interests
- Technical literacy
- Lifestyle preferences
- Geographic categories

This allows users to identify which audiences respond most positively to a product.

---

## 10. API Endpoints

Person 2 is responsible for implementing the following REST API endpoints.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/products` | Create a product |
| GET | `/api/v1/products` | Retrieve all products |
| GET | `/api/v1/products/{id}` | Retrieve a product |
| POST | `/api/v1/personas/generate` | Generate personas |
| GET | `/api/v1/personas/{id}` | Retrieve a persona |
| POST | `/api/v1/simulations` | Start a simulation |
| GET | `/api/v1/simulations/{id}` | Retrieve simulation status |
| GET | `/api/v1/simulations/{id}/results` | Retrieve simulation results |
| GET | `/api/v1/reports/{id}` | Retrieve final report |

### Simulation Status Protocol

The frontend must use consistent simulation statuses.

| Status | Description |
|---|---|
| `queued` | Waiting to start |
| `generating_personas` | Generating consumer profiles |
| `running` | Consumer evaluations in progress |
| `aggregating` | Calculating analytics |
| `completed` | Report successfully generated |
| `failed` | Simulation failed |

Example:

```json
{
  "simulation_id": "SIM001",
  "status": "running",
  "progress": {
    "total_personas": 100,
    "completed_personas": 45,
    "failed_personas": 2
  }
}
```

---

## 11. GitHub Collaboration Workflow

The project uses a branch-based development workflow.

### Branch Structure

```text
main
│
└── develop
    │
    ├── feature/frontend
    ├── feature/backend
    ├── feature/persona-engine
    └── feature/analytics
```

### Branch Ownership

| Member | Branch |
|---|---|
| Person 1 | `feature/frontend` |
| Person 2 | `feature/backend` |
| Person 3 | `feature/persona-engine` |
| Person 4 | `feature/analytics` |

### Development Rules

1. `main` must always contain a stable version.
2. No member should push directly to `main`.
3. All development must happen on assigned feature branches.
4. Feature branches must be merged into `develop` through pull requests.
5. Module owners must review changes affecting their code.
6. Integration must be tested before merging into `main`.
7. Breaking changes to shared contracts require team approval.
8. Environment variables and API keys must never be committed.

### Initial Setup

Clone the repository:

```bash
git clone https://github.com/USERNAME/persona-pulse.git

cd persona-pulse

git checkout develop

git pull origin develop
```

Create your assigned branch:

```bash
git checkout -b feature/frontend
```

Replace the branch name according to your assigned module.

### Commit Convention

Use descriptive commit messages:

```text
feat(frontend): implement product submission form

feat(backend): add product creation endpoint

feat(ai): implement synthetic persona generator

feat(analytics): implement segment scoring

fix(backend): handle invalid simulation requests

test(ai): add persona validation tests

docs: update API integration documentation
```

---

## 12. Development Timeline

The initial development plan targets a 12-day implementation cycle.

| Phase | Timeline | Major Tasks |
|---|---|---|
| Phase 1 | Day 1 | Repository setup, architecture, contracts |
| Phase 2 | Days 2–4 | Independent module development |
| Phase 3 | Days 5–6 | Frontend, backend, and AI integration |
| Phase 4 | Days 7–8 | End-to-end simulation |
| Phase 5 | Days 9–10 | Advanced analytics and improvements |
| Phase 6 | Days 11–12 | Testing, debugging, deployment |

### Phase 1 — Repository Setup

- Create GitHub repository.
- Establish folder structure.
- Define JSON schemas.
- Configure branches.
- Prepare sample data.

### Phase 2 — Independent Development

- Person 1: Develop frontend.
- Person 2: Develop backend and database.
- Person 3: Develop persona and agent engine.
- Person 4: Develop simulation and analytics using mock responses.

### Phase 3 — Integration

- Connect frontend to backend.
- Connect backend to AI engine.
- Connect agent responses to scoring engine.
- Validate shared data structures.

### Phase 4 — End-to-End Simulation

- Submit a product.
- Generate synthetic personas.
- Execute independent agent evaluations.
- Collect responses.
- Calculate scores.
- Generate a final report.
- Display results.

### Phase 5 — Advanced Features

- Audience segmentation.
- Pricing comparisons.
- Sentiment analytics.
- Product recommendations.
- A/B testing.

### Phase 6 — Testing and Deployment

- Run unit tests.
- Run integration tests.
- Fix errors.
- Optimize LLM calls.
- Deploy the application.
- Prepare a working demonstration.

---

## 13. Local Development Setup

### Prerequisites

Install the following:

- Python 3.11+
- Node.js and npm
- PostgreSQL
- Git
- A supported LLM API key

### Step 1 — Clone the Repository

```bash
git clone https://github.com/USERNAME/persona-pulse.git

cd persona-pulse
```

### Step 2 — Backend Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -e ".[dev]"
```

Configure environment variables using `.env.example`.

Start the backend:

```bash
uvicorn backend.app.main:app --reload --port 8000
```

The API will be available at:

`http://localhost:8000`

API documentation:

`http://localhost:8000/docs`

### Step 3 — Frontend Setup

Open a separate terminal:

```bash
cd frontend

npm install

npm run dev
```

The frontend will be available at:

`http://localhost:3000`

### Step 4 — Database Configuration

Configure PostgreSQL and update the `DATABASE_URL` environment variable.

Example:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/personapulse
```

Database migrations should be managed using Alembic.

---

## 14. Environment Variables

Create a local `.env` file using `.env.example` as a template.

```env
# LLM Configuration
GEMINI_API_KEY=

# Database Configuration
DATABASE_URL=

# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Simulation Configuration
DEFAULT_PERSONA_COUNT=20
MAX_PERSONA_COUNT=500
MAX_CONCURRENT_AGENTS=10
```

**Security:** Never commit actual API keys, database passwords, or `.env` files to GitHub.

---

## 15. Testing Strategy

Each module must be tested independently before integration.

| Member | Testing Requirements |
|---|---|
| Person 1 | Component rendering, form validation, API integration |
| Person 2 | API endpoints, database operations, simulation lifecycle |
| Person 3 | Persona generation, profile validation, agent responses |
| Person 4 | Parallel execution, scoring, segmentation, report generation |

### End-to-End Acceptance Test

**Test Product:** Fitness Smartwatch

**Product Price:** ₹4,999

**Target Audience:**
- Age groups: 18–24, 25–34, 35–44
- Interests: Fitness and technology

**Simulation Size:** 50 synthetic personas

Expected workflow:

1. Submit the product.
2. Generate 50 personas.
3. Validate generated profiles.
4. Run independent product evaluations.
5. Collect agent responses.
6. Calculate product scores.
7. Generate age-wise and interest-wise analysis.
8. Generate pricing insights.
9. Produce actionable recommendations.
10. Display the final report on the dashboard.

### Acceptance Criteria

- Every valid response must be associated with a persona ID.
- Invalid responses must be rejected or retried.
- Failed evaluations must be tracked separately.
- Analytics must be calculated using valid responses only.
- Segment-wise analysis must be available.
- Simulation progress must be accessible through the API.
- The final report must follow the agreed JSON schema.
- No mock results should be presented as real simulation results.

---

## 16. Future Enhancements

The following features are planned for future development.

### A/B Product Battle
Compare two product versions using the same synthetic consumer population to identify differences in appeal, purchase intent, and pricing acceptance.

### Dynamic Audience Discovery
Automatically identify potential consumer segments based on product characteristics and simulated responses.

### Persona Debate
Allow selected personas to discuss and challenge different product opinions after their independent evaluations have been completed.

### Competitor Analysis
Compare a submitted product against competing products using standardized evaluation criteria.

### Advertisement Testing
Simulate how different consumer groups might respond to alternative advertising messages and marketing campaigns.

### UX Testing
Evaluate product websites and interfaces from different synthetic user perspectives.

### Real-World Calibration
Compare synthetic responses against real survey or user-testing data to measure agreement, identify biases, and improve simulation reliability.

---

## 17. Project Development Principles

The team will follow these principles throughout development:

1. **Modularity:** Each module must be independently developed and testable.
2. **Standardization:** All modules must follow shared schemas and function interfaces.
3. **Separation of Concerns:** Persona generation, agent reasoning, orchestration, scoring, and presentation must remain separate.
4. **Scalability:** Agent execution must support controlled concurrency and API rate limits.
5. **Reliability:** Invalid responses and failed agent calls must not corrupt the final report.
6. **Reproducibility:** Simulation configurations, persona profiles, model settings, and results should be recorded.
7. **Transparency:** Reports must distinguish synthetic insights from real-world consumer evidence.

---

## 18. Expected MVP Deliverable

The first working version of the platform should support the following:

- [ ] Product submission.
- [ ] Target audience configuration.
- [ ] Generation of 50–100 synthetic consumer personas.
- [ ] Independent LLM-based consumer evaluations.
- [ ] Parallel agent execution.
- [ ] Structured response collection.
- [ ] Overall product scoring.
- [ ] Age-wise and interest-wise segmentation.
- [ ] Pricing acceptance analysis.
- [ ] Interactive market validation dashboard.
- [ ] Final product evaluation report.

---

## 19. Contributors

| Member | Responsibility |
|---|---|
| Mahalakshmi B | Frontend & UI/UX |
| Ashrith Puppala | Backend, Database & Integration |
| Janhvi | AI Persona Generation & Multi-Agent Engine |
| Chinmay J Rao | Simulation Orchestration & Analytics |

---

## 20. License

This project is currently under development.

License and usage terms will be finalized before public release.

---

<p align="center">
  <strong>Synthetic User Persona Swarm</strong><br>
  <em>Understand potential consumers. Evaluate product ideas. Make better-informed decisions.</em>
</p>
