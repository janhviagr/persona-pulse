# PersonaPulse

### Synthetic consumer perspectives for early product exploration

PersonaPulse is a Python application that lets a team describe a product, create a synthetic consumer panel, collect AI-generated evaluations from each persona, and explore the results in an interactive dashboard.

It is intended to help teams form hypotheses and decide what to validate with real customers. Its outputs are simulated opinions, not actual customer research or statistically validated forecasts.

## What it does

- Capture a product name, description, category, price, features, target age groups, interests, and panel size.
- Generate synthetic consumer profiles using demographic rules and reusable behavioral archetypes.
- Create one independent AI consumer agent per persona.
- Ask each agent to score the product and explain its reaction in structured JSON.
- Aggregate valid responses into product metrics, segment summaries, recurring factors, and recommendations.
- Browse the panel, evaluations, and charts in a multi-page Streamlit app.
- Provide a separate FastAPI service for product, persona, simulation, and report endpoints, with database-backed simulation records.

## Application flow

~~~mermaid
flowchart LR
    A[Product brief] --> B[Rule-based persona generator]
    B --> C[Persona profiles]
    C --> D[One consumer agent per persona]
    A --> D
    D --> E[Gemini evaluations]
    E --> F[Validate structured responses]
    F --> G[Metrics and segment analytics]
    G --> H[Streamlit dashboard]
~~~

### Persona generation

The profiles are generated in Python, not by an LLM. The generator samples ages, occupations, income levels, interests, personality traits, and behavioral scores based on the selected audience. Archetypes such as budget student, tech enthusiast, working professional, and health-conscious consumer add coherent motivations and constraints. The Streamlit generation page supplies a fixed seed for repeatable demo panels.

### Consumer agents

Each profile is assigned its own ConsumerAgent. Agents do not message one another: they independently receive the product brief and their persona context, then return scores and reasoning. The asyncio runner executes these independent requests concurrently with a configurable limit and reports progress and failures.

The current design is custom Python using asyncio; it does not use LangChain, LangGraph, CrewAI, or MCP.

### Evaluation and analytics

The evaluation layer validates agent responses, excludes invalid or unmatched responses, and computes summary metrics. The composite score weights interest, purchase intent, price acceptance, perceived usefulness, and design appeal at 25%, 25%, 20%, 15%, and 15%, respectively. Segment analysis groups results by persona attributes, while recurring positive and negative factors help surface common themes.

The current run evaluates the submitted price. It does not run a multi-price experiment. Recommendation answers are not the same as an independent sentiment model.

## Technology used

| Area | Implementation |
| --- | --- |
| User interface | Streamlit, Python |
| Charts | Plotly and Pandas |
| API service | FastAPI, Uvicorn |
| Data validation | Pydantic |
| AI evaluations | Google Gemini API through the Google GenAI Python SDK |
| Agent concurrency | Python asyncio and an asyncio semaphore |
| Database layer | SQLAlchemy async ORM; SQLite by default, PostgreSQL supported by configuration |
| Tests | Pytest |

The Streamlit simulation page currently calls the AI engine directly. The FastAPI service is a separate API path; the frontend service helper is currently empty, so do not describe the Streamlit workflow as routed through the API.

## Repository map

~~~
frontend/
  app.py                       Streamlit entry point and navigation
  pages/                       Overview, product submission, personas, simulation, analytics
  theme.py                     Shared visual theme and components
  components/                  Persona cards and reusable chart helpers
  data/mock_data.py            Sample/demo analytics data
  services/api.py              Reserved frontend API helper (currently empty)

ai_engine/
  personas/                    Persona schema, archetypes, and generator
  agents/                      Consumer agent, factory, prompts, response models, asyncio runner
  llm/                         Provider interface, Gemini provider, and test mock provider
  prompts/                     Persona role and product-evaluation instructions
  simulation/                  Simulation coordination and result validation
  evaluation/                  Scoring, segment analysis, and report generation
  tests/                       AI engine tests

backend/
  app/main.py                  FastAPI app and route registration
  app/api/                     Product, persona, simulation, and report endpoints
  app/schemas/                 API request and response models
  app/models/orm.py            SQLAlchemy database models
  app/database/                Async database engine and sessions
  app/services/                Background simulation and report services
  tests/                       API tests

contracts/                     JSON schemas for shared product and simulation data
docs/                          Architecture and persona design documentation
sample_data/                   Example product, personas, and agent responses
~~~

## Run the Streamlit application

Run commands from the repository root. On Windows, the existing virtual environment can be used as follows:

    .\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
    .\.venv\Scripts\python.exe -m streamlit run frontend\app.py

Open the local URL printed by Streamlit, usually http://localhost:8501.

To run live Gemini evaluations, add your API key to the root .env file:

    GEMINI_API_KEY=your_key_here

Keep .env private; it is ignored by Git. The simulation page loads the root .env and will show a setup message if the key is missing. Persona generation itself does not need the key. Start with a small panel because evaluations use model requests and may be subject to provider rate limits.

Optional settings read by the Gemini provider and runner:

| Variable | Default | Purpose |
| --- | --- | --- |
| GEMINI_REQUESTS_PER_MINUTE | 12 | Spaces Gemini requests to respect provider limits |
| MAX_CONCURRENT_AGENTS | 10 | Caps concurrent persona evaluations |

## Run the FastAPI backend

The backend is a separate service from the Streamlit simulation flow. It exposes versioned routes under /api/v1 and persists products, simulations, personas, and responses.

    .\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --port 8000

- Health check: http://localhost:8000/health
- Interactive API docs: http://localhost:8000/docs

The default database URL is sqlite+aiosqlite:///./personapulse.db. Set DATABASE_URL in the root .env to use another configured SQLAlchemy async database URL. Database tables are created at startup for development; production migrations are not yet wired in.

## API outline

The backend registers these route groups:

- /api/v1/products — create and retrieve product records.
- /api/v1/personas — generate or retrieve persona records.
- /api/v1/simulations — start a background simulation, poll its status, and retrieve results.
- /api/v1/reports — retrieve a simulation report.

Simulation status can progress through queued, generating personas, running, aggregating, completed, or failed. See backend/app/api/ and the Pydantic schemas under backend/app/schemas/ for the exact request and response shapes.

## Testing

Run the backend and AI engine test suites from the repository root:

    .\.venv\Scripts\python.exe -m pytest backend\tests ai_engine\tests -q

The AI engine includes a mock LLM provider so tests can exercise prompt handling, response validation, runner behavior, and analytics without making live Gemini requests.

## Important limitations

- Personas and their reactions are synthetic. They should be treated as exploratory hypotheses, not representative samples of a real market.
- Model outputs can vary and may reflect model, prompt, or sampling bias.
- No calibration against real customer behavior is implemented.
- The submitted product price is evaluated as-is; alternate prices are not tested by the current Streamlit workflow.
- Results depend on the personas requested and the responses successfully returned by the model.
- The current FastAPI backend and Streamlit UI are separate execution paths.

## Future directions

Possible extensions include integrating the Streamlit UI with the API-backed workflow, testing multiple prices, comparing product variants, calibrating against real research, and expanding audience controls. These are future directions, not capabilities to assume are already delivered.

## License

See LICENSE.
