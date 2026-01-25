from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, Text, Integer, REAL, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    discount: Mapped[float] = mapped_column(REAL, default=0)

    # Relationship
    orders: Mapped[List["CustomerOrder"]] = relationship(back_populates="customer")


class Cycle(Base):
    __tablename__ = "cycles"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_date: Mapped[str] = mapped_column(Text, nullable=False)
    end_date: Mapped[Optional[str]] = mapped_column(Text)

    # Relationships
    customer_orders: Mapped[List["CustomerOrder"]] = relationship(
        back_populates="cycle"
    )
    product_prices: Mapped[List["ProductPrice"]] = relationship(back_populates="cycle")
    supply_orders: Mapped[List["SupplyOrder"]] = relationship(back_populates="cycle")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    # Relationships
    customer_orders: Mapped[List["CustomerOrder"]] = relationship(
        back_populates="product"
    )
    prices: Mapped[List["ProductPrice"]] = relationship(back_populates="product")
    supply_orders: Mapped[List["SupplyOrder"]] = relationship(back_populates="product")


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    # Relationship
    supply_orders: Mapped[List["SupplyOrder"]] = relationship(back_populates="supplier")


class CustomerOrder(Base):
    __tablename__ = "customer_orders"

    cycle_id: Mapped[int] = mapped_column(ForeignKey("cycles.id"), primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_price: Mapped[float] = mapped_column(REAL, nullable=False)
    created_at_timestamp: Mapped[str] = mapped_column(
        Text, default=lambda: datetime.now().isoformat()
    )

    # Relationships
    cycle: Mapped["Cycle"] = relationship(back_populates="customer_orders")
    customer: Mapped["Customer"] = relationship(back_populates="orders")
    product: Mapped["Product"] = relationship(back_populates="customer_orders")


class ProductPrice(Base):
    __tablename__ = "product_prices"

    cycle_id: Mapped[int] = mapped_column(ForeignKey("cycles.id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    price: Mapped[float] = mapped_column(REAL, nullable=False)
    created_at_timestamp: Mapped[str] = mapped_column(
        Text, default=lambda: datetime.now().isoformat()
    )

    # Relationships
    cycle: Mapped["Cycle"] = relationship(back_populates="product_prices")
    product: Mapped["Product"] = relationship(back_populates="prices")


class SupplyOrder(Base):
    __tablename__ = "supply_orders"

    cycle_id: Mapped[int] = mapped_column(ForeignKey("cycles.id"), primary_key=True)
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id"), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at_timestamp: Mapped[str] = mapped_column(
        Text, default=lambda: datetime.now().isoformat()
    )

    # Relationships
    cycle: Mapped["Cycle"] = relationship(back_populates="supply_orders")
    supplier: Mapped["Supplier"] = relationship(back_populates="supply_orders")
    product: Mapped["Product"] = relationship(back_populates="supply_orders")


if __name__ == "__main__":
    # Create an engine (example with SQLite)
    engine = create_engine("sqlite:///data/Business.db")

    # Create all tables
    Base.metadata.create_all(engine)
