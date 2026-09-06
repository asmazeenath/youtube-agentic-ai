from typing import Dict

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from investment_plan_agent.agent import investment_plan_agent


def get_user_finance_details() -> Dict:
    """Get user's personal finance details like salary, expenses, and savings capacity."""
    return {
        "salary": 50000,
        "expense": {
            "EMI_Expense": 40000,
            "Essentials": 5000
        },
        "savings": 10000
    }


finance_assistance_agent = LlmAgent(
    name="finance_assistance_agent",
    model="gemini-3.6-flash",
    description="A simple finance assistant that helps users with their finance goals.",
    
    instruction="""
You are a friendly finance assistant.

You can help users:
- Answer generic questions about finance.
- Understand their current financial situation.
- Plan their financial goals.
- Create saving plans.

Be friendly, helpful, and positive.

You have two tools:

1. get_user_finance_details
   - This tool provides the user's current salary, expenses, and savings information.

2. investment_plan_agent
   - This tool can use Google Search to find the latest information.
   - It can help users plan their savings and investment goals.

ALWAYS use investment_plan_agent when the user asks about:
- Stock prices, such as "Tesla stock price" or "TSLA latest price".
- Market data.
- Financial news.
- Company information.
- ANY question containing words such as:
  "latest", "current", "today", "now", or "recent".

When using search results, provide factual information and specific numbers when available.
""",

    tools=[
        get_user_finance_details,
        AgentTool(investment_plan_agent)
    ]
)

root_agent = finance_assistance_agent