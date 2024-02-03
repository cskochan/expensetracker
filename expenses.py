class Expenses:
    def __init__(self, date = None, name = "unknown", type = "misc", amount = 0.0) -> None:
        self.date = date
        self.name = name
        self.type = type
        self.amount = amount