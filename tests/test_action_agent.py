from app.action_agents.action_agent import ActionAgent


def test_action_requires_approval():
    agent = ActionAgent()

    result = agent.execute(
        "prepare_revenue_report"
    )

    assert result["status"] == "approval_required"


def test_approved_action_succeeds():
    agent = ActionAgent()

    result = agent.execute(
        "prepare_revenue_report",
        approved=True
    )

    assert result["status"] == "success"
    assert result["result"]["report"]["total_revenue"] == 109000.0


def test_unknown_action_is_rejected():
    agent = ActionAgent()

    result = agent.execute(
        "delete_database",
        approved=True
    )

    assert result["status"] == "rejected"