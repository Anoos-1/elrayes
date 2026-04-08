from sqlalchemy import Column, Integer, String, Float, Date
from db import Base
from datetime import date


# =========================
# Accounts Table
# =========================
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)          # customer / supplier / bank
    region = Column(String, default="")
    balance = Column(Float, default=0)


# =========================
# Operations Table (ledger rows)
# =========================
class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer)
    account_type = Column(String)

    date = Column(Date, default=date.today)
    record_number = Column(String, default="")
    description = Column(String, default="")

    item_type = Column(String, default="")
    price_per_ton = Column(Float, default=0)

    gross_weight = Column(Float, default=0)
    deduction = Column(Float, default=0)
    net_weight = Column(Float, default=0)

    supplier_amount = Column(Float, default=0)
    payment = Column(Float, default=0)
    total = Column(Float, default=0)


# =========================
# Companies Table
# =========================
class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String)


# =========================
# Item Types Table
# =========================
class ItemType(Base):
    __tablename__ = "item_types"

    id = Column(Integer, primary_key=True)
    name = Column(String)


# =========================
# Bank Accounts Table
# =========================
class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True)
    bank_name = Column(String)          # Bank name (e.g., البنك الأهلي)
    account_name = Column(String)       # Account name (e.g., حساب جاري)
    account_number = Column(String)     # Account number
    initial_balance = Column(Float, default=0)
    current_balance = Column(Float, default=0)


# =========================
# Treasury Transactions Table
# =========================
class TreasuryTransaction(Base):
    __tablename__ = "treasury_transactions"

    id = Column(Integer, primary_key=True)
    date = Column(Date, default=date.today)
    trans_type = Column(String)  # 'withdrawal', 'deposit', 'payment'
    bank_id = Column(Integer)
    bank_name = Column(String)
    amount = Column(Float)
    discount_percent = Column(Float, default=0)
    final_amount = Column(Float)
    notes = Column(String, default="")
    balance = Column(Float, default=0)