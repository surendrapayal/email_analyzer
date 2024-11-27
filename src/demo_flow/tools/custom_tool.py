from typing import Type

from crewai.tools import BaseTool
from crewai_tools import tool
from pydantic import BaseModel, Field

class MyCustomEmailInput(BaseModel):
    """Input schema for MyCustomJiraTool"""
    email_content: str = Field(..., description="email content.")

@tool
def my_custom_email_tool_new(custom_input: MyCustomEmailInput):
    """This tool is used to send the email and accept out from Email Analyzer as a custom input"""
    print(f"email content inside email tool:- {custom_input.email_content}")
    return "email sent successfully"

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")


class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, you agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
