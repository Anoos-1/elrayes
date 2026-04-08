class ItemType:
    """Item/Product type model"""
    
    def __init__(self, id, name, code=None):
        self.id = id
        self.name = name
        self.code = code
    
    def __repr__(self):
        return f"ItemType({self.name})"