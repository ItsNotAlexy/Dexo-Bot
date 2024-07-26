import nextcord
import psutil
import json
import os
import time
from datetime import datetime, timedelta
from rich import print
from rich.console import Console
from rich.table import Table
from nextcord.ext import commands

with open("config/botconf.json") as f:
    config = json.load(f)


class Dexo(commands.Bot):
    def __init__(self):
        super().__init__(intents=nextcord.Intents.all())
        self.start_time = datetime.now()
        self.console = Console()
        self.load_commands_and_events()

    def load_commands_and_events(self):
        commands_path = "./commands"
        events_path = "./events"

        with self.console.status(
            "[bold green]Loading Commands and Events..."
        ) as status:
            tasks = 0
            total_tasks = len(os.listdir(commands_path)) + len(os.listdir(events_path))

            for file in os.listdir(commands_path):
                if file.endswith(".py"):
                    self.load_extension(f"commands.{file[:-3]}")
                    tasks += 1
                    time.sleep(1)
                    status.update(
                        f"[bold green]Loaded {tasks}/{total_tasks} Commands and Events..."
                    )

            for file in os.listdir(events_path):
                if file.endswith(".py"):
                    self.load_extension(f"events.{file[:-3]}")
                    tasks += 1
                    time.sleep(1)
                    status.update(
                        f"[bold green]Loaded {tasks}/{total_tasks} Commands and Events..."
                    )

            status.update("[bold green]Commands and Events Loaded Successfully!")

    async def on_ready(self):
        await self.change_presence(
            activity=nextcord.Activity(
                type=nextcord.ActivityType.watching,
                name=f"Over You | /info",
            ),
            status=nextcord.Status.idle,
        )
        uptime = datetime.now() - self.start_time
        formatted_uptime = str(timedelta(seconds=int(uptime.total_seconds())))

        print(f"[bold green]Logged in as {self.user}[/bold green]")
        print(f"[bold green]ID: {self.user.id}[/bold green]")
        print("\n")
        table = Table(title="Bot Statistics", style="bold green")
        table.add_column("Uptime", style="bold green")
        table.add_column("Memory Usage", style="bold green")
        table.add_column("CPU Usage", style="bold green")
        table.add_column("Guilds", style="bold green")
        table.add_column("Users", style="bold green")
        table.add_row(
            formatted_uptime,
            f"{psutil.virtual_memory().percent}%",
            f"{psutil.cpu_percent()}%",
            f"{len(self.guilds)}",
            f"{len(self.users)}",
            style="bold green",
        )
        print(table)


DexoClient = Dexo()
DexoClient.run(config["TOKEN"])
