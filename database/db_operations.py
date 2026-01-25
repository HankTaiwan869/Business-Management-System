from .models import (
    Base,
    Customer,
    Cycle,
    Product,
    Supplier,
    CustomerOrder,
    ProductPrice,
    SupplyOrder,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

engine = create_engine("sqlite:///data/Business.db", echo=False)
SessionLocal = sessionmaker(bind=engine)


def db_reset():
    try:
        Base.metadata.drop_all(bind=engine)
        print("All tables dropped successfully.")

        # Usually, you'd want to re-initialize right after dropping
        Base.metadata.create_all(bind=engine)
        print("Database re-initialized.")
    except Exception as e:
        print(f"Error resetting database: {e}")


def add_customer(name, discount=0.0):
    with SessionLocal() as session:
        customer = Customer(name=name, discount=discount)
        session.add(customer)
        session.commit()


def add_product(name):
    with SessionLocal() as session:
        product = Product(name=name)
        session.add(product)
        session.commit()


def add_supplier(name):
    with SessionLocal() as session:
        supplier = Supplier(name=name)
        session.add(supplier)
        session.commit()


def get_customers() -> pd.DataFrame:
    with SessionLocal() as session:
        df = pd.read_sql_query("SELECT * FROM customers", session.connection())
    return df
