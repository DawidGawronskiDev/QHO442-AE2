class Color:
    @staticmethod
    def red():
        return "\033[91m"

    @staticmethod
    def green():
        return "\033[92m"

    @staticmethod
    def reset():
        return "\033[0m"

    @staticmethod
    def success(s):
        return f'{Color.green()}{s}{Color.reset()}'

    @staticmethod
    def error(s):
        return f'{Color.red()}{s}{Color.reset()}'