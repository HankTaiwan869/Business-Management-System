import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter, MaxNLocator
from database.db_operations import (
    get_products,
    get_customers,
    get_customer_orders_by_product,
    get_product_price_by_product_id,
    get_supply_orders_by_product,
    get_customer_by_id,
    get_profits_by_cycle,
    get_customer_orders_by_cycle_and_product,
)
import matplotlib.pyplot as plt


# ======== Prepare data for plotting ==========
def _profit_by_product_data(cycle_id) -> pd.DataFrame:
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


def _revenue_by_customer_data(cycle_id: int) -> dict[str, float]:
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


def _orders_by_product_and_cycle_data(begin: int, end: int) -> pd.DataFrame:
    rows = get_customer_orders_by_cycle_and_product(begin, end)

    # Convert to list of dicts for DataFrame creation
    data = [
        {
            "cycle_id": row.cycle_id,
            "product_name": row.product_name,
            "total_quantity": row.total_quantity,
        }
        for row in rows
    ]
    df = pd.DataFrame(data)

    # If no data, return empty DataFrame with proper structure
    if df.empty:
        print("There is no data fetched.")
        return df

    # Pivot to get products as columns, cycles as rows
    df_pivot = df.pivot(
        index="cycle_id", columns="product_name", values="total_quantity"
    ).fillna(0)

    return df_pivot


# ========== Plotting function ===========
def profit_by_product_plot(fig, cycle_id: int) -> None:
    """
    Create a horizontal bar chart showing net profit by product for a given cycle.
    """
    df = _profit_by_product_data(cycle_id)
    sns.set_style("whitegrid")
    sns.set_context("notebook", font_scale=1.1)
    sns.set_theme(font="Microsoft JhengHei")

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
    ax.set_xlabel("利潤", fontsize=12, fontweight="bold")
    ax.set_ylabel("", fontsize=12, fontweight="bold")
    ax.set_title("各產品利潤比較", fontsize=14, fontweight="bold", pad=20)

    # Format x-axis to show currency
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: f"${x:,.0f}"))

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
    revenue_data = _revenue_by_customer_data(cycle_id)

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
    sns.set_theme(font="Microsoft JhengHei")

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

    ax.set_xlabel("營收", fontsize=12, fontweight="bold")
    ax.set_ylabel("", fontsize=12, fontweight="bold")
    ax.set_title("每位顧客營收比較", fontsize=14, fontweight="bold", pad=20)

    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: f"${x:,.0f}"))
    for container in ax.containers:
        ax.bar_label(container, fmt="$%.0f", padding=3)

    # Remove top and right spines for cleaner look
    sns.despine(left=False, bottom=False)

    plt.tight_layout()


def profits_by_cycle_plot(fig, begin: int, end: int) -> None:
    """
    Create a line plot with points showing profits by cycle for a given range.
    """
    sns.set_style("whitegrid")
    sns.set_context("notebook", font_scale=1.1)
    sns.set_theme(font="Microsoft JhengHei")

    ax = fig.gca()

    # Prepare the data
    rows = get_profits_by_cycle(begin, end)
    x = [row.id for row in rows]
    y = [row.profit for row in rows]

    # Create line plot with points
    ax.plot(
        x,
        y,
        marker="o",
        markersize=8,
        color="#6B9BD1",
        alpha=0.7,
        markeredgecolor="white",
        markeredgewidth=1.5,
        linewidth=2,
    )

    ax.set_xlabel("期數", fontsize=12, fontweight="bold")
    ax.set_ylabel("利潤", fontsize=12, fontweight="bold")
    ax.set_title("每期利潤", fontsize=14, fontweight="bold", pad=20)

    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f"${x:,.0f}"))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Remove top and right spines for cleaner look
    sns.despine(left=False, bottom=False)
    plt.tight_layout()


def orders_by_product_and_cycle_plot(fig, begin: int, end: int) -> None:
    sns.set_style("whitegrid")
    sns.set_context("notebook", font_scale=1.1)
    sns.set_theme(font="Microsoft JhengHei")

    ax = fig.gca()
    df = _orders_by_product_and_cycle_data(begin, end)

    if df.empty:
        return

    # Create stacked bar chart with improved styling
    df.plot(
        kind="bar",
        stacked=True,
        ax=ax,
        alpha=0.7,
        edgecolor="white",
        linewidth=1.5,
        width=0.7,
    )

    ax.set_xlabel("期數", fontsize=12, fontweight="bold")
    ax.set_ylabel("數量", fontsize=12, fontweight="bold")
    ax.set_title("顧客訂單及產品分析", fontsize=14, fontweight="bold", pad=20)

    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f"{x:,.0f}"))

    # Rotate x-axis labels for better readability
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

    ax.legend(
        title="產品清單",
        title_fontsize=10,
        fontsize=9,
        loc="upper left",
        frameon=True,
        framealpha=0.9,
        edgecolor="lightgray",
    )

    # Remove top and right spines for cleaner look
    sns.despine(left=False, bottom=False)
    plt.tight_layout()
