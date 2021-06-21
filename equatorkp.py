# Keypirinha: a fast launcher for Windows (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu

from .Equator.lib import main as eq

class Equator(kp.Plugin):
    """Evaluate expressions or solve equations"""
    DEFAULT_KEEP_HISTORY = True

    keep_history = DEFAULT_KEEP_HISTORY

    def __init__(self):
        super().__init__()

    def on_start(self):
        pass

    def on_catalog(self):
        self.on_start()

    def on_suggest(self, user_input, items_chain):
        if items_chain:
            return

        try:
            command, expression = eq.splitInput(user_input)
        except:
            return
        try:
            results = eq.runInput(command, expression)
            suggestions = []
            for r in results:
                suggestions.append(self.create_item(
                    name="EquatorResult",
                    label=r,
                    short_desc="Wow!"
                ))
            
        except:
            return
        

    def on_execute(self, item, action):
        if item.category() != kp.ItemCategory.URL:
            return

        

    def on_events(self, flags):
        if flags & kp.Events.PACKCONFIG:
            self._read_config()

    def _read_config(self):
        settings = self.load_settings()
        self.keep_history = settings.get_bool(
            "keep_history", "main", self.DEFAULT_KEEP_HISTORY)
