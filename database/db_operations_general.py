from .models import (
    Base,
    Customer,
    Cycle,
    Product,
    Supplier,
    CustomerOrder,
    Settings,
)
from sqlalchemy import create_engine, select, func, Row
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from typing import Sequence, Any


engine = create_engine("sqlite:///data/Business.db", echo=False)
SessionLocal = sessionmaker(bind=engine)


# ===== development only =====
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


# ===== development only =====


# Initialize the database when program starts for the firs time
def initialize_database():
    """Initialize database tables and settings on first run"""
    try:
        # Try to get settings
        get_current_settings()
    except Exception as e:
        # If tables don't exist, create them
        print(f"Database not initialized. Creating tables... ({e})")

        # Create all tables
        Base.metadata.create_all(bind=engine)

        with SessionLocal() as session:
            initial_setting = Settings(is_in_cycle=False, cycle_id=None)
            session.add(initial_setting)
            session.commit()

        print("Database initialized successfully")


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


# returns True if success, False if fail
def finish_cycle(revenue: float, cost: float) -> bool:
    with SessionLocal() as session:
        try:
            settings = session.scalar(select(Settings))
            if settings is None:
                return False
            cycle_id = settings.cycle_id
            if cycle_id is None:
                return False
            current_cycle = session.scalar(select(Cycle).where(Cycle.id == cycle_id))
            if current_cycle is None:
                return False

            # Update current cycle
            settings.is_in_cycle = False
            current_cycle.end_date = datetime.now().isoformat()
            current_cycle.revenue = revenue
            current_cycle.cost = cost
            current_cycle.profit = revenue - cost

            session.commit()
            return True

        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
            return False


def get_monthly_figures(year: int, month: int) -> tuple[Any, Any]:
    with SessionLocal() as session:
        result = session.execute(
            select(func.sum(Cycle.revenue), func.sum(Cycle.cost)).where(
                Cycle.end_date.like(f"{year}-{str(month).zfill(2)}%"),
                Cycle.revenue.is_not(None),
                Cycle.cost.is_not(None),
            )
        ).one()
    revenue, cost = result
    return (revenue or 0, cost or 0)


def get_profits_by_cycle(
    begin: int, end: int
) -> Sequence[Row[tuple[int, float | None]]]:
    with SessionLocal() as session:
        profits = session.execute(
            select(Cycle.id, Cycle.profit).where(Cycle.id >= begin, Cycle.id <= end)
        ).all()
    return profits


def get_customer_orders_by_cycle_and_product(
    begin: int, end: int
) -> Sequence[Row[tuple[int, str, float]]]:
    with SessionLocal() as session:
        # Query to get aggregated quantities by cycle and product
        query = (
            select(
                CustomerOrder.cycle_id,
                Product.name.label("product_name"),
                func.sum(CustomerOrder.quantity).label("total_quantity"),
            )
            .join(Product, CustomerOrder.product_id == Product.id)
            .where(CustomerOrder.cycle_id >= begin, CustomerOrder.cycle_id <= end)
            .group_by(CustomerOrder.cycle_id, Product.name)
            .order_by(CustomerOrder.cycle_id, Product.name)
        )

        results = session.execute(query).all()

    return results


def get_current_settings() -> Settings:
    with SessionLocal() as session:
        settings = session.query(Settings).one()
        return settings


def get_cycle_start_date(cycle_id: int) -> date | None:
    with SessionLocal() as session:
        row = session.scalars(
            select(Cycle.start_date).where(Cycle.id == cycle_id)
        ).one_or_none()
    if row is None:
        return None
    return datetime.fromisoformat(row).date()


def add_customer(name: str, discount: float = 0.0) -> None:
    with SessionLocal() as session:
        customer = Customer(name=name, discount=discount)
        session.add(customer)
        session.commit()


def add_product(name: str) -> None:
    with SessionLocal() as session:
        product = Product(name=name)
        session.add(product)
        session.commit()


def add_supplier(name: str) -> None:
    with SessionLocal() as session:
        supplier = Supplier(name=name)
        session.add(supplier)
        session.commit()


def get_customers() -> Sequence[Customer]:
    with SessionLocal() as session:
        rows = session.scalars(select(Customer)).all()
    return rows


def get_customer_by_id(id: int) -> Customer | None:
    with SessionLocal() as session:
        row = session.scalars(select(Customer).where(Customer.id == id)).one_or_none()
    return row


def get_products() -> Sequence[Product]:
    with SessionLocal() as session:
        rows = session.scalars(select(Product)).all()
    return rows


def get_suppliers() -> Sequence[Supplier]:
    with SessionLocal() as session:
        rows = session.scalars(select(Supplier)).all()
    return rows


def update_customer_discount(name: str, discount: float) -> None:
    with SessionLocal() as session:
        customer = session.scalars(select(Customer).where(Customer.name == name)).one()
        customer.discount = discount
        session.commit()
