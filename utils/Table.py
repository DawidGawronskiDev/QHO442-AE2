class Table:
    def __init__(self, lengths, headers, rows):
        """
        Initializes a table for formatted display.
        """
        self.headers = headers
        self.rows = rows
        self.lengths = lengths

    def __str__(self):
        """
        Returns a string representation of the table with borders and formatted rows.
        """
        header = self.create_row(self.headers)
        border = '#' * len(header)
        rows_str = '\n'.join(self.create_row(row) for row in self.rows)

        return f"{border}\n{header}\n{border}\n{rows_str}\n{border}"

    def create_row(self, items):
        """
        Creates a formatted row with the specified column widths.
        """
        formatted_columns = [str(column).ljust(length) for column, length in zip(items, self.lengths)]
        return f"# {' # '.join(formatted_columns)} #"

    def print_header(self):
        """
        Prints the header of the table to the console.
        """
        header = self.create_row(self.headers)
        border = '#' * len(header)
        print(f"{border}\n{header}\n{border}")

    def print_row(self, items):
        """
        Prints a row of data to the console.
        """
        print(self.create_row(items))

    def print_table(self):
        """
        Prints the entire table to the console, including headers and rows.
        """
        print(self.__str__())