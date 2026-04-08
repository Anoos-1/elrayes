from db import Session
from models import Account, Operation, Company, ItemType, TreasuryTransaction
from datetime import date


# ============================
# Account CRUD
# ============================
def create_account(name, acc_type, region=""):
    """Create a new account (supplier, customer, or bank)"""
    s = Session()
    try:
        acc = Account(name=name, type=acc_type, region=region, balance=0)
        s.add(acc)
        s.commit()
        return acc
    except Exception as e:
        s.rollback()
        print(f"Error creating account: {e}")
    finally:
        s.close()


def get_accounts(acc_type):
    """Get all accounts of a specific type"""
    s = Session()
    try:
        data = s.query(Account).filter_by(type=acc_type).all()
        return data
    except Exception as e:
        print(f"Error getting accounts: {e}")
        return []
    finally:
        s.close()


def get_account_by_id(account_id):
    """Get a single account by ID"""
    s = Session()
    try:
        acc = s.query(Account).filter_by(id=account_id).first()
        return acc
    except Exception as e:
        print(f"Error getting account: {e}")
        return None
    finally:
        s.close()


def get_account_balance(account_id):
    """Get current balance of an account"""
    s = Session()
    try:
        acc = s.query(Account).filter_by(id=account_id).first()
        balance = acc.balance if acc else 0
        return balance
    except Exception as e:
        print(f"Error getting balance: {e}")
        return 0
    finally:
        s.close()


# ============================
# Operations
# ============================
def add_operation(account_id, account_type, description="",
                  item_type="", price_per_ton=0,
                  gross_weight=0, deduction=0, net_weight=0,
                  supplier_amount=0, payment=0,
                  op_date=None, record_number=""):
    """Add a new operation (transaction)"""

    total = supplier_amount - payment

    s = Session()
    try:
        op = Operation(
            account_id=account_id,
            account_type=account_type,
            date=op_date if op_date else date.today(),
            record_number=record_number,
            description=description,
            item_type=item_type,
            price_per_ton=price_per_ton,
            gross_weight=gross_weight,
            deduction=deduction,
            net_weight=net_weight,
            supplier_amount=supplier_amount,
            payment=payment,
            total=total
        )
        s.add(op)

        # Update account balance
        acc = s.query(Account).filter_by(id=account_id).first()
        if acc:
            acc.balance += total

        s.commit()
    except Exception as e:
        s.rollback()
        print(f"Error adding operation: {e}")
    finally:
        s.close()


def get_operations(account_id):
    """Get all operations for an account"""
    s = Session()
    try:
        data = s.query(Operation).filter_by(account_id=account_id).order_by(Operation.id).all()
        return data
    except Exception as e:
        print(f"Error getting operations: {e}")
        return []
    finally:
        s.close()


# ============================
# Payments (Customer / Supplier)
# ============================
def customer_payment(customer_id, bank_id, amount, record_number="", op_date=None):
    """Record a customer payment"""
    s = Session()
    try:
        customer = s.query(Account).filter_by(id=customer_id).first()
        bank = s.query(Account).filter_by(id=bank_id).first()

        if customer:
            customer.balance -= amount
        if bank:
            bank.balance += amount

        op_customer = Operation(
            account_id=customer_id,
            account_type="customer",
            description="سداد عميل",
            date=op_date if op_date else date.today(),
            record_number=record_number,
            payment=amount,
            total=-amount
        )

        op_bank = Operation(
            account_id=bank_id,
            account_type="bank",
            description="تحصيل من عميل",
            date=op_date if op_date else date.today(),
            record_number=record_number,
            supplier_amount=amount,
            total=amount
        )

        s.add(op_customer)
        s.add(op_bank)
        s.commit()
    except Exception as e:
        s.rollback()
        print(f"Error recording customer payment: {e}")
    finally:
        s.close()


def pay_supplier(supplier_id, bank_id, amount, record_number="", op_date=None):
    """Record a supplier payment"""
    s = Session()
    try:
        supplier = s.query(Account).filter_by(id=supplier_id).first()
        bank = s.query(Account).filter_by(id=bank_id).first()

        if supplier:
            supplier.balance -= amount
        if bank:
            bank.balance -= amount

        op_supplier = Operation(
            account_id=supplier_id,
            account_type="supplier",
            description="دفعة",
            date=op_date if op_date else date.today(),
            record_number=record_number,
            payment=amount,
            total=-amount
        )

        op_bank = Operation(
            account_id=bank_id,
            account_type="bank",
            description="دفع لمورد",
            date=op_date if op_date else date.today(),
            record_number=record_number,
            payment=amount,
            total=-amount
        )

        s.add(op_supplier)
        s.add(op_bank)
        s.commit()
    except Exception as e:
        s.rollback()
        print(f"Error recording supplier payment: {e}")
    finally:
        s.close()


# ============================
# Treasury Transactions
# ============================
def add_treasury_transaction(trans_type, bank_id, bank_name, amount, 
                           discount_percent=0, notes="", current_balance=0):
    """Add a treasury transaction (withdrawal, deposit, payment)"""
    s = Session()
    try:
        # Calculate final amount after discount
        final_amount = amount - (amount * discount_percent / 100)
        
        trans = TreasuryTransaction(
            date=date.today(),
            trans_type=trans_type,
            bank_id=bank_id,
            bank_name=bank_name,
            amount=amount,
            discount_percent=discount_percent,
            final_amount=final_amount,
            notes=notes,
            balance=current_balance + final_amount
        )
        s.add(trans)
        s.commit()
    except Exception as e:
        s.rollback()
        print(f"Error adding treasury transaction: {e}")
    finally:
        s.close()


def get_treasury_transactions():
    """Get all treasury transactions"""
    s = Session()
    try:
        data = s.query(TreasuryTransaction).order_by(TreasuryTransaction.id).all()
        return data
    except Exception as e:
        print(f"Error getting treasury transactions: {e}")
        return []
    finally:
        s.close()


def get_treasury_balance():
    """Get current treasury balance"""
    s = Session()
    try:
        last_trans = s.query(TreasuryTransaction).order_by(TreasuryTransaction.id.desc()).first()
        balance = last_trans.balance if last_trans else 0
        return balance
    except Exception as e:
        print(f"Error getting treasury balance: {e}")
        return 0
    finally:
        s.close()


# ============================
# Master Data
# ============================
def get_companies():
    """Get all companies"""
    s = Session()
    try:
        data = s.query(Company).all()
        return data
    except Exception as e:
        print(f"Error getting companies: {e}")
        return []
    finally:
        s.close()


def add_company(name):
    """Add a new company"""
    s = Session()
    try:
        s.add(Company(name=name))
        s.commit()
    except Exception as e:
        s.rollback()
        print(f"Error adding company: {e}")
    finally:
        s.close()


def get_item_types():
    """Get all item types"""
    s = Session()
    try:
        data = s.query(ItemType).all()
        return data
    except Exception as e:
        print(f"Error getting item types: {e}")
        return []
    finally:
        s.close()


def add_item_type(name):
    """Add a new item type"""
    s = Session()
    try:
        s.add(ItemType(name=name))
        s.commit()
    except Exception as e:
        s.rollback()
        print(f"Error adding item type: {e}")
    finally:
        s.close()