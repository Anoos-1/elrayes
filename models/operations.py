from datetime import datetime


class Operation:
    """Base operation class for edit/delete functionality"""
    
    @staticmethod
    def calculate_discount(amount, discount_percent):
        """Calculate amount after discount percentage"""
        discount = amount * (discount_percent / 100)
        return round(amount - discount, 2)
    
    @staticmethod
    def calculate_with_damage(amount, damage_percent):
        """Calculate amount after damage/هالك percentage deduction"""
        damage = amount * (damage_percent / 100)
        return round(amount - damage, 2)
    
    @staticmethod
    def format_number(value, decimals=2):
        """Format number with rounding"""
        return round(float(value), decimals)
    
    @staticmethod
    def get_today():
        """Get today's date in YYYYMMDD format"""
        return int(datetime.now().strftime("%Y%m%d"))
    
    @staticmethod
    def get_currency_symbol():
        """Return Egyptian Pound symbol"""
        return "ج.م"  # جنيه مصري