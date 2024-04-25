import asyncio

async def function_A():
    print("Executing function A")
    await asyncio.sleep(1)
    print("Finished function A")

async def function_B():
    print("Executing function B")
    await asyncio.sleep(1)
    print("Finished function B")

class TaskGroup:
    def __init__(self):
        self.tasks = []
        self.current_task_index = 0

    async def add_task(self, task):
        self.tasks.append(task)

    async def process_next_task(self):
        if self.current_task_index < len(self.tasks):
            task = self.tasks[self.current_task_index]
            await task
            self.current_task_index += 1

    async def run_tasks(self):
        while True:
            await self.process_next_task()
            if self.current_task_index >= len(self.tasks):
                self.current_task_index = 0

async def main():
    task_group = TaskGroup()

    # 创建任务并添加到任务组
    task_A = asyncio.create_task(function_A())
    task_B = asyncio.create_task(function_B())
    await task_group.add_task(task_A)
    await task_group.add_task(task_B)

    # 循环执行任务组中的任务
    while True:
        await task_group.run_tasks()

asyncio.run(main())
