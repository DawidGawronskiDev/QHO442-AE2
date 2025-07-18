from utils.TUI import TUI

class Validator:
    """A class for validating user input in the terminal user interface."""
    @staticmethod
    def validate_numeric_input(prompt, error_message="Invalid input. Please enter a numeric value.", min_value=None, max_value=None):
        """Validates that the input is a numeric value."""
        while True:
            try:
                value = int(input(prompt).strip())
                if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                    TUI.print_error(f"Value must be between {min_value} and {max_value}.\n")
                    continue
                return value
            except ValueError:
                TUI.print_error(f"{error_message}\n")

    @staticmethod
    def validate_confirmation(prompt, error_message="Invalid input. Please enter Y or N."):
        """Validates that the input is a confirmation (Y/N)."""
        while True:
            confirmation = input(prompt).strip().upper()
            if confirmation in ("Y", "N"):
                return confirmation == "Y"
            TUI.print_error(f"{error_message}\n")