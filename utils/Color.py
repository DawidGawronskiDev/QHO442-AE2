class Color:
    @staticmethod
    def red():
        """ Returns the ANSI escape code for red text. """
        return "\033[91m"

    @staticmethod
    def green():
        """ Returns the ANSI escape code for green text. """
        return "\033[92m"

    @staticmethod
    def reset():
        """ Returns the ANSI escape code to reset text formatting. """
        return "\033[0m"

    @staticmethod
    def success(s):
        """ Formats a string in green for success messages. """
        return f'{Color.green()}{s}{Color.reset()}'

    @staticmethod
    def error(s):
        """ Formats a string in red for error messages. """
        return f'{Color.red()}{s}{Color.reset()}'