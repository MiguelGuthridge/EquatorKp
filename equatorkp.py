# Keypirinha: a fast launcher for Windows (keypirinha.com)

import site
import os

import keypirinha as kp
import keypirinha_util as kpu

# insert lib directory to path to import modules normally
site.addsitedir(os.path.join(os.path.dirname(__file__), "include"))

import equator as eq

class Equator(kp.Plugin):
    """Evaluate expressions or solve equations"""
    DEFAULT_KEEP_HISTORY = True

    keep_history = DEFAULT_KEEP_HISTORY
    
    ITEMCAT_VAR = kp.ItemCategory.USER_BASE + 1

    PRIORITY_1 = "EqPriority 1"
    PRIORITY_2 = "EqPriority 2"
    PRIORITY_3 = "EqPriority 3"

    def __init__(self):
        super().__init__()

    def on_start(self):
        pass

    def on_catalog(self):
        self.on_start()

    def on_suggest(self, user_input: str, items_chain):
        if items_chain:
            return
        suggestions = []
        try:
            # Check that input starts with "eq"
            command, expression = user_input.split(' ', 1)
            if command != "eq": return
            
        except Exception as e:
            return
        try:
            
            results_exp = eq.Expression(expression)
            results = results_exp.getOutputList()
            
            # No results
            if len(results) == 0:
                suggestions.append(self.create_item(
                    category=self.ITEMCAT_VAR,
                    label="No Results",
                    short_desc="Equator",
                    target=self.PRIORITY_1,
                    args_hint=kp.ItemArgsHint.FORBIDDEN,
                    hit_hint=kp.ItemHitHint.IGNORE,
                    data_bag = ""
                ))
            
            # One result
            elif len(results) == 1:
                eqtns, exprs = results[0]
                # For solutions and expressions
                if len(exprs) >= 1 and len(eqtns) >= 1:
                    exs = '; '.join(exprs)
                    eqs = '; '.join(eqtns)
                    if len(exs) and len(eqs):
                        r = exs + "; " + eqs
                    else:
                        r = exs + eqs
                    suggestions.append(self.create_item(
                        category=self.ITEMCAT_VAR,
                        label="Copy Full Solution",
                        short_desc="Equator",
                        target=self.PRIORITY_1,
                        args_hint=kp.ItemArgsHint.FORBIDDEN,
                        hit_hint=kp.ItemHitHint.IGNORE,
                        data_bag=r
                    ))
                
                # For multiple expressions
                if len(exprs) > 1:
                    r = "; ".join(exprs)
                    suggestions.append(self.create_item(
                        category=self.ITEMCAT_VAR,
                        label="Copy all Expressions",
                        short_desc="Equator",
                        target=self.PRIORITY_2 + r,
                        args_hint=kp.ItemArgsHint.FORBIDDEN,
                        hit_hint=kp.ItemHitHint.IGNORE,
                        data_bag=r
                    ))
                # For each expression
                for x in exprs:
                    suggestions.append(self.create_item(
                        category=self.ITEMCAT_VAR,
                        label=x,
                        short_desc="Equator - Enter to Copy",
                        target=self.PRIORITY_3 + x,
                        args_hint=kp.ItemArgsHint.FORBIDDEN,
                        hit_hint=kp.ItemHitHint.IGNORE,
                        data_bag=x
                    ))
                # For multiple equations
                if len(eqtns) > 1:
                    r = "; ".join(eqtns)
                    suggestions.append(self.create_item(
                        category=self.ITEMCAT_VAR,
                        label="Copy all Equations",
                        short_desc="Equator",
                        target=self.PRIORITY_2 + r,
                        args_hint=kp.ItemArgsHint.FORBIDDEN,
                        hit_hint=kp.ItemHitHint.IGNORE,
                        data_bag=r
                    ))
                # For each equation
                for q in eqtns:
                    suggestions.append(self.create_item(
                        category=self.ITEMCAT_VAR,
                        label=q,
                        short_desc="Equator - Enter to Copy",
                        target=self.PRIORITY_3 + q,
                        args_hint=kp.ItemArgsHint.FORBIDDEN,
                        hit_hint=kp.ItemHitHint.IGNORE,
                        data_bag=q
                    ))

            # Many results
            else:
                out = results_exp.getOutputStr()
                suggestions.append(self.create_item(
                    category=self.ITEMCAT_VAR,
                    label="Copy all Solutions",
                    short_desc="Equator",
                    target=self.PRIORITY_1 + out,
                    args_hint=kp.ItemArgsHint.FORBIDDEN,
                    hit_hint=kp.ItemHitHint.IGNORE,
                    data_bag = out
                ))
                
                for i, s in enumerate(results):
                    exprs = '; '.join(s[1])
                    eqtns = '; '.join(s[0])
                    if len(exprs) and len(eqtns):
                        r = exprs + "; " + eqtns
                    else:
                        r = exprs + eqtns
                    suggestions.append(self.create_item(
                        category=self.ITEMCAT_VAR,
                        label=r,
                        short_desc=f"Equator - Solution {i+1} - Enter to copy",
                        target=self.PRIORITY_3 + r,
                        args_hint=kp.ItemArgsHint.FORBIDDEN,
                        hit_hint=kp.ItemHitHint.IGNORE,
                        data_bag=r
                    ))
        
        except eq.EqException as e:
            suggestions.append(self.create_error_item(
                label="Equator - Error",
                short_desc=str(e)))
            #print(e)
        
        self.set_suggestions(suggestions, kp.Match.ANY, kp.Sort.TARGET_ASC)

    def on_execute(self, item, action):
        if item.category() != self.ITEMCAT_VAR:
            return
        if item and (item.category() == self.ITEMCAT_VAR):
            output = item.data_bag()
            if len(output):
                kpu.set_clipboard(output)

    def on_events(self, flags):
        if flags & kp.Events.PACKCONFIG:
            self._read_config()

    def _read_config(self):
        settings = self.load_settings()
        self.keep_history = settings.get_bool(
            "keep_history", "main", self.DEFAULT_KEEP_HISTORY)
