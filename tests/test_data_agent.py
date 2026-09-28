from app.data_agents.data_agent import DataAgent


def test_total_revenue():
    agent = DataAgent()

    result = agent.total_revenue()

    assert result == 109000.0


def test_monthly_revenue():
    agent = DataAgent()

    result = agent.monthly_revenue()

    assert result[0]["month"] == "2026-01"
    assert result[0]["revenue"] == 105000
    assert result[1]["month"] == "2026-02"
    assert result[1]["revenue"] == 4000


def test_monthly_profit():
    agent = DataAgent()

    result = agent.monthly_profit()

    assert result[0]["month"] == "2026-01"
    assert result[0]["profit"] == 23000
    assert result[1]["month"] == "2026-02"
    assert result[1]["profit"] == 1500