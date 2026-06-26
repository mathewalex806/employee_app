from agno.agent import Agent
from agno.models.groq import Groq
from database.connection import AsyncSessionLocal
from rag.retrieval import ask_policy_question
from employee.employee_service import GetUserByIdService


async def employee_lookup(employee_id: int):
    """DB tool for Employee details lookup using employee id"""
    async with AsyncSessionLocal() as db:
        emp_object = await GetUserByIdService(id=employee_id, db=db)
        # return emp_object.model_dump()
        return [
            emp_object.name,
            emp_object.addresses,
            emp_object.created_at,
            emp_object.email,
            emp_object.id,
            emp_object.age,
            emp_object.experience,
            emp_object.status,
            emp_object.role,
        ]


def policy_lookup(question: str):
    """RAG tool for HR policy lookup"""
    return ask_policy_question(query=question)


def create_hr_agent() -> Agent:
    return Agent(
        model=Groq(id="openai/gpt-oss-120b"),
        tools=[
            employee_lookup,
            policy_lookup,
        ],
        instructions="""
You are an HR assistant. You MUST use tools to answer questions. Never guess or make up answers.

- When asked about an employee, you MUST call employee_lookup with their id. Do not describe what you would do, just call the tool.
- When asked about HR policies, you MUST call policy_lookup with the question.
- If you don't have enough information to call a tool, ask the user for it.
- Never respond with what the tool "would return". Always call the tool and return the actual result in a formatted manner.
- If any field is missing in the data, ignore those fields and return the available data

#Output Formatting
- Always return in plain text. Do not return json, markdown, emoji's or any other special characters. Do not return raw data like <address_object>.
- The response has to always be in natural language and easily readable.
""",
    )
