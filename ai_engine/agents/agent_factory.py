from ai_engine.personas.persona_model import Persona

from .consumer_agent import ConsumerAgent


class AgentFactory:
    """Turns a list of persona dicts into a list of ConsumerAgents."""

    @staticmethod
    def create_agents(personas: list[dict], llm) -> list[ConsumerAgent]:
        agents = []
        for persona in personas:
            Persona(**persona)  # raises ValidationError if the persona is invalid
            agents.append(ConsumerAgent(persona, llm))
        return agents
