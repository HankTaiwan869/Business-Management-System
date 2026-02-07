from .models import (
    Product,
    CustomerOrder,
    ProductPrice,
    SupplyOrder,
    Supply_quantity_and_price,
)
from .db_operations_general import SessionLocal, get_customer_by_id
from sqlalchemy import select
from typing import Sequence
from datetime import datetime


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
