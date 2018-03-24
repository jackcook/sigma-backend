class User:

    def __init__(self, balance, transactions, user_id):
        self.balance = balance
        self.transactions = transactions
        self.user_id = user_id

    def serialize(self):
        return {
            "id": self.user_id,
            "balance": self.balance,
            "transactions": self.transactions
        }
