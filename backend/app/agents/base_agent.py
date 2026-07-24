from abc import ABC, abstractmethod
import time
import traceback


class BaseAgent(ABC):
    """
    Base class for all AI Investigation Agents.
    Every agent in the system should inherit from this class.
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.version = "1.0.0"

    async def before_run(self):
        """
        Called before the agent starts executing.
        """
        self.start_time = time.time()

        print("=" * 60)
        print(f"Starting Agent : {self.name}")
        print(f"Description    : {self.description}")
        print("=" * 60)

    @abstractmethod
    async def execute(self):
        """
        Main logic of the agent.

        Every child agent MUST implement this method.
        """
        pass

    async def after_run(self):
        """
        Called after successful execution.
        """
        end_time = time.time()

        elapsed = round(end_time - self.start_time, 3)
        
        self.execution_time = elapsed

        print("-" * 60)
        print(f"{self.name} completed.")
        print(f"Execution Time : {elapsed} seconds")
        print("-" * 60)

    async def run(self):
        """
        Standard execution flow used by every agent.
        """

        await self.before_run()

        try:

            result = await self.execute()

            await self.after_run()

            return result

        except Exception as ex:

            print("=" * 60)
            print(f"[ERROR] {self.name}")
            print("=" * 60)

            print(ex)

            traceback.print_exc()

            raise