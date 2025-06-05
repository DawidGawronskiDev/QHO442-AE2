from color import Color

class TUI:
    def __init__(self):
        pass

    @staticmethod
    def validate_input(msg):
        prefix = ""
        i = ""

        while len(i) == 0:
            i = str(input(f"{prefix + " " if len(prefix) > 0 else ""}{msg}")).strip()
            if len(i) == 0:
                prefix = f"{Color.error("Missing value.")}"
            else:
                prefix = ""
        return i

    @staticmethod
    def print_success(s):
        print(Color.success(s))

    @staticmethod
    def print_error(s):
        print(Color.error(s))
