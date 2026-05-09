from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class MyCrew():
    """Debate and Judge Crew"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def debater(self) -> Agent:
        return Agent(config=self.agents_config['debater'], verbose=True)
    
    @agent
    def judge(self) -> Agent:
        return Agent(config=self.agents_config['judge'], verbose=True)
    
    @task
    def propose(self) -> Task:
        return Task(config=self.tasks_config['propose'],)
    
    @task
    def oppose(self) -> Task:
        return Task(config=self.tasks_config['oppose'])
    
    @task
    def decide(self) -> Task:
        return Task(config=self.tasks_config['decide'])
    
    @crew
    def crew(self) -> Crew:
        """Create a debate and judge crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )