from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os
from crewai import LLM

from bedrock_agentcore.runtime import BedrockAgentCoreApp

# use for memory
import uuid
from datetime import datetime, UTC
import boto3


memory_client = boto3.client(service_name = 'bedrock-agentcore', region_name = 'us-west-2')


app = BedrockAgentCoreApp()

# load_dotenv()
# MODEL = os.environ.get("MODEL")
# AWS_REGION = os.environ.get("AWS_DEFAULT_REGION")
# SERPER_API_KEY = os.environ.get("SERPER_API_KEY")

# Initialize the tool for internet searching capabilities
serper_tool = SerperDevTool(api_key = "3597ef4a837f1618e2268ed7b03cb4e2621c5360")
llm = LLM(model = "bedrock/us.amazon.nova-pro-v1:0", aws_region_name = "us-west-2")

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class VacationPlanner():
    """VacationPlanner crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def vacation_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['vacation_researcher'], # type: ignore[index]
            verbose=True,
            tools=[serper_tool],
            llm = llm
        )

    @agent
    def itinerary_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['itinerary_planner'], # type: ignore[index]
            verbose=True,
            llm = llm
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the VacationPlanner crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )


@app.entrypoint
def agent_invocation(payload, context):
    '''Handler for agent invocation'''

    print(f"Payload: {payload}")

    try:
        user_input = payload.get('topic', 'London, UK')
        print(f"Processing Vacation Destination: {user_input}")

        # retrieve the past memory
        session_id = getattr(context, "sessionId", "default_session")

        previous_events = memory_client.list_events(
            memoryId = 'vacation_planner-Go9RLHHjGB',
            actorId = 'user',
            sessionId = session_id,
            maxResults = 3
        )

        research_vacation_planner = VacationPlanner()
        crew = research_vacation_planner.crew()

        # result = crew.kickoff(inputs={'topic': user_input})

        # Send input to Agent with previous memory
        events = previous_events.get('events', [])
        formatted_conversations = []
        for event in events:
            formatted_event = {}
            for key, value in event.items():
                if isinstance(value, datetime):
                    formatted_event[key] = value.isoformat()
                else:
                    formatted_event[key] = value
            formatted_conversations.append(formatted_event)
        
        #4 Starts the sequential agent workflow with memory
        result = crew.kickoff(inputs={'topic': user_input, 'previous_conversations': formatted_conversations})
        
        #5 Memory storage - Save current interaction
        memory_client.create_event(
            memoryId='vacation_planner-Go9RLHHjGB',
            actorId='user',
            sessionId=session_id,
            eventTimestamp=datetime.now(UTC),
            payload=[
                {
                    "conversational": {
                        "content": {"text": user_input},
                        "role": "USER"
                    }
                },
                {
                    "conversational": {
                        "content": {"text": result.raw},
                        "role": "ASSISTANT"
                    }
                }
            ],
            clientToken=str(uuid.uuid4())
        )


        print(f'Result: {result.raw}')
        print(f"Context: {context}")

        # Safely access json_dict if it exists
        if hasattr(result, 'json_dict'):
            print("Result JSON:\n*******\n", result.json_dict)
        
        return {"result": result.raw}

    except Exception as err:
        print(f"Error: {err}")
        return {"error": f"An error occurred: {str(err)}"}


if __name__ == "__main__":

    # Run agentcore server
    app.run(port=8080)