from datetime import datetime


class Account:
    """Account model for suppliers and customers"""
    
    def __init__(self, id, name, account_type, balance=0, date_created=None):
        self.id = id
        self.name = name
        self.account_type = account_type  # 'supplier', 'customer', 'bank'
        self.balance = balance
        self.date_created = date_created or datetime.now()
    
    def __repr__(self):
        return f"Account({self.name}, {self.account_type}, {self.balance})"