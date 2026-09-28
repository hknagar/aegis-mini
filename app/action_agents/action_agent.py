from app.data_agents.data_agent import DataAgent


class ActionAgent:

    def __init__(self):
        self.data_agent = DataAgent()

        self.allowed_actions = {
            "prepare_revenue_report": self.prepare_revenue_report
        }

    def prepare_revenue_report(self):
        total_revenue = self.data_agent.total_revenue()
        monthly_revenue = self.data_agent.monthly_revenue()

        return {
            "status": "prepared",
            "report": {
                "title": "Acme Retail Revenue Report",
                "total_revenue": total_revenue,
                "monthly_revenue": monthly_revenue
            }
        }

    def execute(
        self,
        action_name: str,
        approved: bool = False
    ):

        if action_name not in self.allowed_actions:
            return {
                "status": "rejected",
                "message": "This action is not permitted."
            }

        if not approved:
            return {
                "status": "approval_required",
                "action": action_name,
                "message": "Approval is required before execution."
            }

        result = self.allowed_actions[action_name]()

        return {
            "status": "success",
            "result": result
        }