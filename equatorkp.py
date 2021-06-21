# Keypirinha: a fast launcher for Windows (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu

from Equator import main as eq

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

        if 

    def on_execute(self, item, action):
        if item.category() != kp.ItemCategory.URL:
            return

        url_scheme, corrected_url, default_scheme_applied = self._extract_url_scheme(item.target())
        if not url_scheme:
            self.warn("Could not guess URL scheme from URL:", item.target())
            return

        scheme_registered = self._is_registered_url_scheme(url_scheme)
        if not scheme_registered:
            self.warn('URL cannot be launched because its scheme "{}" is not registered'.format(url_scheme))
            return

        if url_scheme in self.WEB_SCHEMES:
            kpu.execute_default_action(self, item, action)
        else:
            kpu.shell_execute(item.target())

    def on_events(self, flags):
        if flags & kp.Events.PACKCONFIG:
            self._read_config()

    def _read_config(self):
        settings = self.load_settings()
        self.keep_history = settings.get_bool(
            "keep_history", "main", self.DEFAULT_KEEP_HISTORY)

    def _read_tld_databases(self):
        tlds = set()
        incomplete = False

        for resource in self.find_resources("tld-*.txt"):
            try:
                lines = self.load_text_resource(resource).lower().splitlines()
            except Exception as exc:
                self.warn("Failed to load DB resource \"{}\". Error: {}".format(resource, exc))
                incomplete = True
                continue

            for line in lines:
                line = line.strip()
                if line and line[0] not in ("#", ";"):
                    tlds.add("." + line)

        if not tlds:
            self.warn("Empty TLD database. Falling back to default...")
            self.known_tlds = self.KNOWN_TLDS
        elif incomplete:
            self.warn("Incomplete TLD database. Merging with default...")
            self.known_tlds = tlds.union(self.KNOWN_TLDS)
        else:
            self.known_tlds = tlds

    def _extract_url_scheme(self, user_input):
        user_input = user_input.strip()
        user_input_lc = user_input.lower()

        # does input string starts with a valid scheme name?
        rem = self.REGEX_URL_PREFIX.match(user_input_lc)
        if rem:
            return rem.group(1), user_input, False

        # since no scheme is specified we want to check the network location only
        if "/" in user_input:
            if user_input[0] == "/":
                user_input = user_input.lstrip("/")
                user_input_lc = user_input.lower()
            idx = user_input_lc.find("/")
            netloc_lc = user_input_lc[0:idx] if idx > -1 else user_input_lc
        else:
            netloc_lc = user_input_lc

        # does the input string contain a known ".tld" (but not as a prefix)?
        if len(netloc_lc) >= 3:
            for tld in self.known_tlds:
                if netloc_lc.find(tld, 1) > -1:
                    return self.DEFAULT_SCHEME, self.DEFAULT_SCHEME_PREFIX + user_input, True

        # does the input string contain a valid IPv4 or IPv6 address?
        groups = re.split(r"/|\[|\]:\d+", netloc_lc)
        for ip_addr in groups:
            if not ip_addr:
                continue
            else:
                for af in (socket.AF_INET6, socket.AF_INET):
                    try:
                        socket.inet_pton(af, ip_addr)
                        if af == socket.AF_INET and "." not in ip_addr:
                            # Here, an IPv4 address has been validated but does
                            # not contain any dot. Avoid to pollute the
                            # suggestions list with that.
                            break
                        return self.DEFAULT_SCHEME, self.DEFAULT_SCHEME_PREFIX + user_input, True
                    except OSError:
                        pass
                break

        return None, None, False

    def _is_registered_url_scheme(self, url_scheme):
        if url_scheme in self.known_schemes:
            return True

        if url_scheme in self.WEB_SCHEMES:
            self.known_schemes.add(url_scheme)
            return True

        cmdline, defico = kpu.shell_url_scheme_to_command(url_scheme)
        if cmdline:
            self.known_schemes.add(url_scheme)
            return True

        return False
