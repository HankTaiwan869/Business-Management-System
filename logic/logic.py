from database.models import Customer
from database.db_operations import (
    get_customers,
    get_products,
    get_product_price_by_product_id,
    get_orders_by_customer_and_product,
    get_customer_orders_by_product,
    get_supply_orders_by_product,
)


def calculate_total_price_by_customer(
    cycle_id: int,
    customer: Customer,
    order_quantities: dict[tuple[int, int], float],
) -> float | None:
    total = 0
    products = get_products()
    for product in products:
        if (customer.id, product.id) in order_quantities:
            price = get_product_price_by_product_id(cycle_id, product.id)
            if price is None:
                raise ValueError(
                    f"No price found for product {product.id} in cycle {cycle_id}"
                )
            # Business logic: calculate price for each customer product pair
            total += (price - customer.discount) * order_quantities[
                (customer.id, product.id)
            ]
    return total


def calculate_total_customer_order_quantity_by_product(
    cycle_id: int, product_id: int
) -> float:
    customer_orders = get_customer_orders_by_product(cycle_id, product_id)
    quantities = [order.quantity for order in customer_orders]
    return sum(quantities)


def calculate_total_supply_order_quantity_by_product(
    cycle_id: int, product_id: int
) -> float:
    supply_orders = get_supply_orders_by_product(cycle_id, product_id)
    quantities = [order.quantity for order in supply_orders]
    return sum(quantities)


def calculate_total_revenue(cycle_id: int) -> float:
    customers = get_customers()
    order_quantities = get_orders_by_customer_and_product(cycle_id)
    total_revenue = 0.0
    for customer in customers:
        revenue = calculate_total_price_by_customer(
            cycle_id, customer, order_quantities
        )
        if revenue is not None:
            total_revenue += revenue
    return total_revenue


def calculate_total_cost(cycle_id: int) -> float:
    products = get_products()
    total_cost = 0.0
    for product in products:
        supply_orders = get_supply_orders_by_product(cycle_id, product.id)
        cost = sum([order.buy_price * order.quantity for order in supply_orders])
        if cost is not None:
            total_cost += cost
    return total_cost


def calculate_cycle_financial_metrics(cycle_id: int) -> dict[str, float]:
    # Current cycle metrics
    new_revenue = calculate_total_revenue(cycle_id)
    new_cost = calculate_total_cost(cycle_id)
    new_profit = new_revenue - new_cost
    new_profit_margin = (new_profit / new_revenue * 100) if new_revenue != 0 else 0

    # Previous cycle metrics
    old_revenue = calculate_total_revenue(cycle_id - 1)
    old_cost = calculate_total_cost(cycle_id - 1)
    old_profit = old_revenue - old_cost

    # Calculate growth (None if first cycle)
    growth = ((new_profit - old_profit) / old_profit * 100) if old_profit != 0 else 0

    return {
        "cycle_id": cycle_id,
        "revenue": new_revenue,
        "cost": new_cost,
        "profit": new_profit,
        "profit_margin": new_profit_margin,
        "previous_revenue": old_revenue,
        "previous_cost": old_cost,
        "previous_profit": old_profit,
        "growth": growth,
    }
