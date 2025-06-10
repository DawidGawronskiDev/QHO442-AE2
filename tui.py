from typing import Tuple

from color import Color

class TUI:
    def __init__(self):
        pass

    @staticmethod
    def display_options(all_options, title, type):
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
            prompt = "Enter the number against the " + type + " you want to choose: "
            selected_option = int(input(prompt))
        return option_list[selected_option - 1]

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
        print(Color.error(s), end="")

    @staticmethod
    def print_list(l):
        for i in l:
            print(f'- {i}')

    @staticmethod
    def print_header(s):
        print(f'\n{s}\n{"-" * len(s)}\n')

    @staticmethod
    def print_table(lens, header, rows):
        for i, val in enumerate(header):
            print(str(val).strip()[:lens[i]].ljust(lens[i], " "), end="")
        print("\n")
        for row in rows:
            for i, val in enumerate(row):
                print(str(val).strip()[:lens[i]].ljust(lens[i], " "), end="")
            print("\n")