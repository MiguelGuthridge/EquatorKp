# Keypirinha: a fast launcher for Windows (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu

from .Equator.lib import main as eq

class Equator(kp.Plugin):
    """Evaluate expressions or solve equations"""
    DEFAULT_KEEP_HISTORY = True

    keep_history = DEFAULT_KEEP_HISTORY
    
    ITEMCAT_VAR = kp.ItemCategory.USER_BASE + 1

    def __init__(self):
        super().__init__()

    def on_start(self):
        pass

    def on_catalog(self):
        self.on_start()

    def on_suggest(self, user_input, items_chain):
        if items_chain:
            return
        suggestions = []
        try:
            command, expression = eq.splitInput(user_input)
            if command not in ["ev", "eq"]: return
        except:
            return
        try:
            results = eq.runInput(command, expression)
            
            for r in results:
                r = str(r)
                suggestions.append(self.create_item(
                    category=self.ITEMCAT_VAR,
                    label=r,
                    short_desc="Equator",
                    target=r,
                    args_hint=kp.ItemArgsHint.FORBIDDEN,
                    hit_hint=kp.ItemHitHint.IGNORE,
                ))
        
        except Exception as e:
            suggestions.append(self.create_error_item(
                label=expression,
                short_desc="Error: " + str(e)))
            print(e)
        
        self.set_suggestions(suggestions, kp.Match.ANY, kp.Sort.LABEL_ASC)

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
