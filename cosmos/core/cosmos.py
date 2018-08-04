import discord

from discord.ext import commands
from cosmos.core.utilities.time import Time
from cosmos.core.functions.configs.handler import ConfigHandler
from cosmos.core.functions.logger.handler import LoggerHandler
from cosmos.core.functions.plugins.handler import PluginHandler
from cosmos.core.functions.database.database import Database


class Cosmos(commands.Bot):

    def __init__(self, token=None, client_id=None, prefixes=None):
        self.time = None
        self.configs = None
        self.logger = None
        self.db = None
        self.plugins = None
        self._init_time()
        self._init_configs()
        self._init_logger()
        self._init_database()
        self._init_plugins()
        self.configs.discord.token = token or self.configs.discord.token
        self.configs.discord.client_id = client_id or self.configs.discord.client_id
        self.configs.discord.prefixes = prefixes or self.configs.cosmos.prefixes
        super().__init__(command_prefix=commands.when_mentioned_or(*self.configs.cosmos.prefixes))

    def _init_time(self):
        print("Initialising Cosmos time.")
        self.time = Time()
        print("Done.", end="\n\n")

    def _init_configs(self):
        print("Initialising configs.")
        start_time = self.time.time()
        self.configs = ConfigHandler()
        print(f"Done. [{round(self.time.time() - start_time, 3)}s].", end="\n\n")

    def _init_logger(self):
        print("Initialising logger.")
        start_time = self.time.time()
        self.logger = LoggerHandler(self)
        print(f"Done. [{round(self.time.time() - start_time, 3)}s].", end="\n\n")

    def _init_database(self):
        print("Initialising database.")
        start_time = self.time.time()
        self.db = Database(self)
        print(f"Done. [{round(self.time.time() - start_time, 3)}s].", end="\n\n")

    def _init_plugins(self):
        print("Initialising plugins.")
        start_time = self.time.time()
        self.plugins = PluginHandler(self)
        print(f"Done. [{round(self.time.time() - start_time, 3)}s].", end="\n\n")

    def run(self):
        try:
            super().run(self.configs.discord.token)
        except discord.LoginFailure:
            print("Invalid token provided.")

    async def on_ready(self):
        print(f"{self.user.name}#{self.user.discriminator} Ready! [{self.time.round_time()} seconds.]")
        print(f"User Id: {self.user.id}")
        print("-------")