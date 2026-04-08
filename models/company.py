class Company:
    """Company/Organization model"""
    
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type  # 'supplier', 'customer', 'bank'
    
    def __repr__(self):
        return f"Company({self.name}, {self.type})"