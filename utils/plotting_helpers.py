import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from database.db_operations import (
    get_products,
    get_customers,
    get_customer_orders_by_product,
    get_product_price_by_product_id,
    get_supply_orders_by_product,
    get_customer_by_id,
)

# ======== Prepare data for plotting ==========


def profit_by_product_data(cycle_id) -> pd.DataFrame:
    products = get_products()
    customers = get_customers()

    data = []

    for product in products:
        # Calculate revenue
        customer_orders = get_customer_orders_by_product(cycle_id, product.id)
        price = get_product_price_by_product_id(cycle_id, product.id)

        product_revenue = 0.0
        if price is not None and customer_orders:
            for order in customer_orders:
                customer = next(
                    (c for c in customers if c.id == order.customer_id), None
                )
                if customer:
                    product_revenue += (price - customer.discount) * order.quantity

        # Calculate cost
        supply_orders = get_supply_orders_by_product(cycle_id, product.id)
        product_cost = sum(order.buy_price * order.quantity for order in supply_orders)

        # Calculate profit
        profit = product_revenue - product_cost

        data.append(
            {
                "product_name": product.name,
                "revenue": product_revenue,
                "cost": product_cost,
                "profit": profit,
            }
        )

    df = pd.DataFrame(data)

    return df.sort_values("profit", ascending=False)


def revenue_by_customer_data(cycle_id: int) -> dict[str, float]:
    """
    Prepare revenue data grouped by customer for a given cycle.

    Args:
        cycle_id: The cycle ID to analyze

    Returns:
        Dictionary mapping customer names to their total revenue
    """
    revenue_by_customer = {}

    # Get all products
    products = get_products()

    # For each product, get all customer orders
    for product in products:
        product_price = get_product_price_by_product_id(cycle_id, product.id)
        if product_price is None:
            continue

        customer_orders = get_customer_orders_by_product(cycle_id, product.id)

        for order in customer_orders:
            customer = get_customer_by_id(order.customer_id)
            if customer is None:
                continue

            # Calculate revenue (price * quantity * (1 - discount))
            revenue = (product_price - customer.discount) * order.quantity

            # Add to customer's total revenue
            if customer.name in revenue_by_customer:
                revenue_by_customer[customer.name] += revenue
            else:
                revenue_by_customer[customer.name] = revenue

    return revenue_by_customer


# ========== Plotting function ===========
def profit_by_product_plot(fig, cycle_id: int) -> None:
    """
    Create a horizontal bar chart showing net profit by product for a given cycle.
    """
    df = profit_by_product_data(cycle_id)
    sns.set_style("whitegrid")
    sns.set_context("notebook", font_scale=1.1)

    ax = fig.gca()

    # Create barplot with improved styling
    sns.barplot(
        data=df,
        x="profit",
        y="product_name",
        hue="product_name",
        palette="viridis",
        legend=False,  # Remove redundant legend since y-axis shows product names
        ax=ax,
    )

    # Enhance labels and title
    ax.set_xlabel("Net Profit ($)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Product", fontsize=12, fontweight="bold")
    ax.set_title("Net Profit by Product", fontsize=14, fontweight="bold", pad=20)

    # Format x-axis to show currency
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))

    # Add value labels on bars
    for container in ax.containers:
        ax.bar_label(container, fmt="$%.0f", padding=3)

    # Remove top and right spines for cleaner look
    sns.despine(left=False, bottom=False)

    # Adjust layout
    plt.tight_layout()


def revenue_by_customer_plot(fig, cycle_id: int) -> None:
    """
    Create a horizontal bar chart showing revenue by customer for a given cycle.
    """
    # Get the data
    revenue_data = revenue_by_customer_data(cycle_id)

    if not revenue_data:
        print(f"No revenue data found for cycle {cycle_id}")
        return

    # Convert to DataFrame for seaborn
    df = pd.DataFrame(
        [
            {"customer_name": name, "revenue": revenue}
            for name, revenue in revenue_data.items()
        ]
    )

    # Sort by revenue (descending)
    df = df.sort_values("revenue", ascending=False)

    sns.set_style("whitegrid")
    sns.set_context("notebook", font_scale=1.1)

    ax = fig.gca()

    # Create barplot with improved styling
    sns.barplot(
        data=df,
        x="revenue",
        y="customer_name",
        hue="customer_name",
        palette="viridis",
        legend=False,  # Remove redundant legend since y-axis shows customer names
        ax=ax,
    )

    # Enhance labels and title
    ax.set_xlabel("Revenue ($)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Customer", fontsize=12, fontweight="bold")
    ax.set_title("Revenue by Customer", fontsize=14, fontweight="bold", pad=20)

    # Format x-axis to show currency
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))

    # Add value labels on bars
    for container in ax.containers:
        ax.bar_label(container, fmt="$%.0f", padding=3)

    # Remove top and right spines for cleaner look
    sns.despine(left=False, bottom=False)

    # Adjust layout
    plt.tight_layout()
