class Basket:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def get_items(self):
        return self.items

    def clear(self):
        self.items.clear()

    def __str__(self):
        return f"Basket(items={self.items})"