class User:

    def __init__(self, user_id, name, balance, transactions):
        self.user_id = user_id
        self.name = name
        self.balance = balance
        self.transactions = transactions

    def serialize(self):
        return {
            "id": self.user_id,
            "name": self.name,
            "balance": self.balance,
            "transactions": self.transactions
        }
