from abc import ABCMeta, abstractmethod


class Cog(object):

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        self._plugin = None
        self._bot = None

    @property
    @abstractmethod
    def plugin(self):
        return self._plugin

    @plugin.setter
    def plugin(self, plugin):
        self._plugin = plugin

    @property
    @abstractmethod
    def bot(self):
        return self._bot

    @bot.setter
    def bot(self, bot):
        self._bot = bot

    def __load(self):
        plugin = self.plugin
        plugin.bot.log.info(f"Loading COG {self.__class__.__name__}.")
        cog = self.__class__(plugin)
        if cog.name in plugin.cogs:
            plugin.bot.log.error(f"Cog {self.__class__.__name__} is already loaded.")
            return
        else:
            plugin.bot.add_cog(cog)
        plugin.bot.log.info("Done.")

    def unload(self):
        self.bot.log.info(f"Unloading COG {self.name}.")
        if self.name not in self.plugin.cogs:
            self.bot.log.error(f"Cog {self.name} is not loaded.")
            return
        else:
            self.bot.remove_cog(self.name)
        self.bot.log.info(f"COG {self.name} unloaded.")

    def reload(self):
        self.bot.log.info(f"Reloading COG {self.name}.")
        self.unload()
        self.__load()
        self.bot.log.info(f"COG {self.name} reloaded.")