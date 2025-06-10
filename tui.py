from typing import Tuple

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
        print(Color.error(s), end="")

    @staticmethod
    def print_list(l):
        for i in l:
            print(f'- {i}')

    @staticmethod
    def print_table(lens: Tuple[int], header: Tuple[str], rows: Tuple[str, int]):
        lens = (12, 16, 48, 24, 8, 8, 12)
        header = ("Order ID", "Order Date", "Product Description", "Seller", "Price", "Qty", "Status")
        for i, val in enumerate(header):
            print(str(val).strip()[:lens[i]].ljust(lens[i], " "), end="")
        print("\n")
        for row in rows:
            for i, val in enumerate(row):
                print(str(val).strip()[:lens[i]].ljust(lens[i], " "), end="")
            print("\n")