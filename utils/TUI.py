from utils.Color import Color

class TUI:
    """A class for handling terminal user interface operations, including displaying options, validating input,
     and printing messages in various formats."""
    @staticmethod
    def display_options(all_options, title, t):
        """Displays a list of options to the user and allows them to select one."""
        option_num = 1
        option_list = []
        print("\n", title, "\n")
        for option in all_options:
            code = option[0]
            desc = option[1]
            print("{0}.\t{1}".format(option_num, desc))
            option_num += 1
            option_list.append(code)
        selected_option = 0
        while selected_option > len(option_list) or selected_option == 0:
            prompt = "Enter the number against the " + t + " you want to choose: "
            selected_option = int(input(prompt))
        return option_list[selected_option - 1]

    @staticmethod
    def print_success(s):
        """Prints a success message in green."""
        print(Color.success(s))

    @staticmethod
    def print_error(s):
        """Prints an error message in red."""
        print(Color.error(s), end="")

    @staticmethod
    def print_header(s):
        """Prints a header with the given string, underlined by dashes."""
        print(f'\n{s}\n{"-" * len(s)}\n')