#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

# from .crews.poem_crew.poem_crew import PoemCrew
from .crews.gmail_crew.gmail_crew import EmailCrew


class PoemState(BaseModel):
    priority: str = ""
    description: str = ""
    issue_reported: str = ""
    jiraId: str = "Jira-12345"
    email: str = ""

class PoemFlow(Flow[PoemState]):

    @start()
    def generate_issue_reported_user(self):
        print("Generating issue reported by user")
        self.state.issue_reported = "As a user I am not able to perform the transaction from the last 15 minutes and due to this over 500K transactions have declined that result in the revenue loss of more than 150K US dollar. Please look into this issue on urgent basis."
        # self.state.issue_reported = "As a user I am not able to perform the transaction from the last 5 minutes and due to this around 100 transactions have declined that result in the revenue loss of around 1000 US dollar. Please look into this issue and provide resolution."

    @listen(generate_issue_reported_user)
    def create_email_template(self):
        print("Creating email template")
        self.state.description = self.state.issue_reported
        result = (
            EmailCrew()
            .crew()
            .kickoff(inputs={"jiraId": self.state.jiraId, "priority": "High", "description": self.state.description, "project": "GNOC"})
        )

        print("Email template created", result.raw)
        self.state.email = result.raw

    @listen(create_email_template)
    def save_email_template(self):
        print("Saving email template")
        with open("email_template.txt", "w") as f:
            f.write(self.state.email)

    # @listen(save_email_template)
    # def send_email(self):
    #     print("Send email")
    #     self.state.description = self.state.issue_reported
    #     result = (
    #         EmailCrew()
    #         .crew()
    #         .kickoff(inputs={"email_content": self.state.email})
    #     )
    #
    #     print("Email template created", result.raw)
    #     self.state.email = result.raw

def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
