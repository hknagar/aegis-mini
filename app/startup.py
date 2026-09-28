from app.knowledge_agents.knowledge_agent import KnowledgeAgent


def initialize_knowledge():
    agent = KnowledgeAgent()

    agent.ingest("knowledge")