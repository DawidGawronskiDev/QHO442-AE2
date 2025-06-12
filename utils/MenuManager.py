from utils.Validator import Validator

class MenuManager:
    def __init__(self, controller):
        self.controller = controller
        self.options = {
            1: ("Display your order history", self.controller.sub_1),
            2: ("Add an item to your basket", self.controller.sub_2),
            3: ("View your basket", self.controller.sub_3),
            4: ("Change the quantity of an item in your basket", self.controller.sub_4),
            5: ("Remove an item from your basket", self.controller.sub_5),
            6: ("Checkout", self.controller.sub_6),
            7: ("Exit", exit)
        }

    def display_menu(self):
        while True:
            for key, (desc, _) in self.options.items():
                print(f"{key}. {desc}")
            choice = Validator.validate_numeric_input("Choose an option: ", "Invalid choice.", min_value=1, max_value=7)
            self.options[choice][1]()