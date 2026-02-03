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
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Sequence


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


# returns True if success, False if fail
def finish_cycle() -> bool:
    with SessionLocal() as session:
        try:
            settings = session.scalar(select(Settings))
            if settings is None:
                return False
            settings.is_in_cycle = False
            id = settings.cycle_id
            current_cycle = session.scalar(select(Cycle).where(Cycle.id == id))
            if current_cycle is None:
                return False
            current_cycle.end_date = datetime.now().isoformat()
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
            return False


def get_settings() -> Settings:
    with SessionLocal() as session:
        settings = session.query(Settings).one()
        return settings


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


def get_total_customer_order_quantity_by_product(
    cycle_id: int, product_id: int
) -> float:
    with SessionLocal() as session:
        orders = session.scalars(
            select(CustomerOrder.quantity).where(
                CustomerOrder.cycle_id == cycle_id,
                CustomerOrder.product_id == product_id,
            )
        ).all()
    return sum(orders)


def get_total_supply_order_quantity_by_product(cycle_id: int, product_id: int) -> float:
    with SessionLocal() as session:
        orders = session.scalars(
            select(SupplyOrder.quantity).where(
                SupplyOrder.cycle_id == cycle_id,
                SupplyOrder.product_id == product_id,
            )
        ).all()
    return sum(orders)


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


if __name__ == "__main__":
    get_product_prices(1)
