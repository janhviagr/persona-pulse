"""Regenerates contracts/*.schema.json from the backend Pydantic models.
Run from repo root:  py -m scripts.export_contracts
"""
import json
from pathlib import Path

from backend.app.schemas.persona import PersonaProfile
from backend.app.schemas.product import Product
from backend.app.schemas.simulation import AgentResponse, Report, SimulationRequest

OUT = Path("contracts")
OUT.mkdir(exist_ok=True)
for name, model in {
    "product": Product,
    "persona": PersonaProfile,
    "simulation_request": SimulationRequest,
    "simulation_result": AgentResponse,
    "report": Report,
}.items():
    (OUT / f"{name}.schema.json").write_text(json.dumps(model.model_json_schema(), indent=2), encoding="utf-8")
    print("wrote", OUT / f"{name}.schema.json")
