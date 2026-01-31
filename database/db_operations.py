from .models import (
    Base,
    Customer,
    Cycle,
    Product,
    Supplier,
    CustomerOrder,
    ProductPrice,
    SupplyOrder,
    Settings,
)
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import pandas as pd
from datetime import datetime

engine = create_engine("sqlite:///data/Business.db", echo=False)
SessionLocal = sessionmaker(bind=engine)


def db_reset():
    try:
        Base.metadata.drop_all(bind=engine)

        # Usually, you'd want to re-initialize right after dropping
        Base.metadata.create_all(bind=engine)

        # Initialize Settings
        with SessionLocal() as session:
            initial_setting = Settings(is_in_cycle=False, cycle_id=None)
            session.add(initial_setting)
            session.commit()

    except Exception as e:
        print(f"An error occurred during database reset: {e}")


def start_cycle():
    with SessionLocal() as session:
        try:
            # Check if already in a cycle
            settings = session.query(Settings).one()
            if settings.is_in_cycle:
                print("A cycle is already in progress.")
                return

            # Create a new cycle
            new_cycle = Cycle(start_date=datetime.now().isoformat())
            session.add(new_cycle)
            session.flush()  # To get the new cycle ID
            cycle_id = new_cycle.id

            # Update settings
            settings.is_in_cycle = True
            settings.cycle_id = cycle_id

            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error starting cycle: {e}")
            raise


def get_settings() -> Settings:
    with SessionLocal() as session:
        settings = session.query(Settings).one()
        return settings


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


def get_products() -> pd.DataFrame:
    with SessionLocal() as session:
        df = pd.read_sql_query("SELECT * FROM products", session.connection())
    return df


def get_suppliers() -> pd.DataFrame:
    with SessionLocal() as session:
        df = pd.read_sql_query("SELECT * FROM suppliers", session.connection())
    return df


def get_product_prices(cycle_id: int):
    with SessionLocal() as session:
        data = (
            session.query(ProductPrice).filter(ProductPrice.cycle_id == cycle_id).all()
        )

    return data


def update_product_price(cycle_id: int, product_id: int, new_price: float):
    with SessionLocal() as session:
        product_price = (
            session.query(ProductPrice)
            .filter(
                ProductPrice.cycle_id == cycle_id,
                ProductPrice.product_id == product_id,
            )
            .one_or_none()
        )
        if product_price:
            product_price.sell_price = new_price
        else:
            product_price = ProductPrice(
                cycle_id=cycle_id, product_id=product_id, sell_price=new_price
            )
            session.add(product_price)
        session.commit()


if __name__ == "__main__":
    get_product_prices(1)
