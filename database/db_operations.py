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
    Supply_quantity_and_price,
)
from sqlalchemy import create_engine, select, func, Row
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from typing import Sequence, Any


engine = create_engine("sqlite:///data/Business.db", echo=False)
SessionLocal = sessionmaker(bind=engine)


# development only
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


def add_customer(name, discount=0.0) -> None:
    with SessionLocal() as session:
        customer = Customer(name=name, discount=discount)
        session.add(customer)
        session.commit()


def add_product(name) -> None:
    with SessionLocal() as session:
        product = Product(name=name)
        session.add(product)
        session.commit()


def add_supplier(name) -> None:
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


def get_product_prices(cycle_id: int) -> Sequence[ProductPrice]:
    with SessionLocal() as session:
        rows = session.scalars(
            select(ProductPrice).where(ProductPrice.cycle_id == cycle_id)
        ).all()
    return rows


def get_product_price_by_product_id(cycle_id: int, product_id: int) -> float | None:
    with SessionLocal() as session:
        row = session.scalar(
            select(ProductPrice.sell_price).where(
                ProductPrice.cycle_id == cycle_id, ProductPrice.product_id == product_id
            )
        )
    return row


def get_orders_by_suppliers(cycle_id: int, supplier_id: int) -> Sequence[SupplyOrder]:
    with SessionLocal() as session:
        rows = session.scalars(
            select(SupplyOrder).where(
                SupplyOrder.cycle_id == cycle_id, SupplyOrder.supplier_id == supplier_id
            )
        ).all()
    return rows


def get_orders_by_customer_and_product(cycle_id: int) -> dict[tuple[int, int], float]:
    with SessionLocal() as session:
        orders = session.execute(
            select(
                CustomerOrder.customer_id,
                CustomerOrder.product_id,
                CustomerOrder.quantity,
            ).where(CustomerOrder.cycle_id == cycle_id)
        )
    return {(order.customer_id, order.product_id): order.quantity for order in orders}


def get_customer_orders_by_product(
    cycle_id: int, product_id: int
) -> Sequence[CustomerOrder]:
    with SessionLocal() as session:
        orders = session.scalars(
            select(CustomerOrder).where(
                CustomerOrder.cycle_id == cycle_id,
                CustomerOrder.product_id == product_id,
            )
        ).all()
    return orders


def get_supply_orders_by_product(
    cycle_id: int, product_id: int
) -> Sequence[SupplyOrder]:
    with SessionLocal() as session:
        orders = session.scalars(
            select(SupplyOrder).where(
                SupplyOrder.cycle_id == cycle_id,
                SupplyOrder.product_id == product_id,
            )
        ).all()
    return orders


def get_orders_by_supplier_and_product(
    cycle_id: int,
) -> dict[tuple[int, int], Supply_quantity_and_price]:
    with SessionLocal() as session:
        orders = session.execute(
            select(
                SupplyOrder.supplier_id,
                SupplyOrder.product_id,
                SupplyOrder.quantity,
                SupplyOrder.buy_price,
            ).where(SupplyOrder.cycle_id == cycle_id)
        )
    return {
        (order.supplier_id, order.product_id): Supply_quantity_and_price(
            quantity=order.quantity, price=order.buy_price
        )
        for order in orders
    }


def update_customer_discount(name: str, discount: float) -> None:
    with SessionLocal() as session:
        customer = session.scalars(select(Customer).where(Customer.name == name)).one()
        customer.discount = discount
        session.commit()


def update_product_price(cycle_id: int, product_name: str, new_price: float):
    with SessionLocal() as session:
        product_id = session.scalars(
            select(Product.id).where(Product.name == product_name)
        ).one()
        product_price = session.scalars(
            select(ProductPrice).where(
                ProductPrice.cycle_id == cycle_id,
                ProductPrice.product_id == product_id,
            )
        ).one_or_none()
        if product_price:
            product_price.sell_price = new_price
        else:
            product_price = ProductPrice(
                cycle_id=cycle_id, product_id=product_id, sell_price=new_price
            )
            session.add(product_price)
        session.commit()


def update_customer_order(
    cycle_id: int, customer_id: int, product_id: int, quantity: float
) -> None:
    with SessionLocal() as session:
        customer = get_customer_by_id(customer_id)
        if customer is None:
            raise ValueError(f"Customer {customer_id} not found")
        product_price = session.scalar(
            select(ProductPrice).where(
                ProductPrice.cycle_id == cycle_id, ProductPrice.product_id == product_id
            )
        )
        if product_price is None:
            raise ValueError(
                f"Product price not found for product {product_id} in cycle {cycle_id}"
            )

        # Try querying existing orders
        order = session.scalars(
            select(CustomerOrder).where(
                CustomerOrder.cycle_id == cycle_id,
                CustomerOrder.customer_id == customer_id,
                CustomerOrder.product_id == product_id,
            )
        ).one_or_none()
        if order is None:
            new_order = CustomerOrder(
                cycle_id=cycle_id,
                customer_id=customer_id,
                product_id=product_id,
                quantity=quantity,
            )
            session.add(new_order)
        else:
            order.quantity = quantity
            order.created_at_timestamp = datetime.now().isoformat()
        session.commit()


def update_supplier_order(
    cycle_id: int, supplier_id: int, product_id: int, quantity: float, price: float
) -> None:
    with SessionLocal() as session:
        order = session.scalar(
            select(SupplyOrder).where(
                SupplyOrder.cycle_id == cycle_id,
                SupplyOrder.supplier_id == supplier_id,
                SupplyOrder.product_id == product_id,
            )
        )
        if order is None:
            order = SupplyOrder(
                cycle_id=cycle_id,
                supplier_id=supplier_id,
                product_id=product_id,
                quantity=quantity,
                buy_price=price,
            )
            session.add(order)
        else:
            order.quantity = quantity
            order.buy_price = price
            order.created_at_timestamp = datetime.now().isoformat()
        session.commit()
