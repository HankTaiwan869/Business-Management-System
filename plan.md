I'm designing a small scale business management local web app using SQLite3 and NiceGUI.
Here's my draft system plan.
Database:
TABLE ({} indicates primary key)
	- customers: {id}, name, discount
    - order_cycles: {id}, start_date, end_date
    - products: {id}, name
    - suppliers: {id}, name
    - customer_orders: {cycle_id, customer_id, product_id}, quantity, actual_price, created_at_timestamp
    - product_prices: {cycle_id, product_id}, price, created_at_timestamp
    - supply_orders: {cycle_id, supplier_id, product_id}, quantity, created_at_timestamp
INDEX: order_cycles.id, all primary keys of customer_orders, product_prices, supply_orders

Webpage:
/Home
    - Button: Start a Cycle [hidden if the last cycle is unfinished (marked by NULL end_date)]
    - Button: Continue the Cycle
    - Button: Business Report
    - Button: Customer Profile

/Cycle
    - Title: Cycle {idx} {start_date}
    - Three steps: 
        - Link to Product
        - Link to Customer
        - Link to Supply
    - Button: Finish this cycle [only show when three steps are finished] [links to cycle_summary]

/Cycle/Product
    - Table: shows product name and last-cycle price
    - Update price here [Opens a dialogue (label: old price, number input: new price) to update values]

/Cycle/Customer
    - Label: cycle {idx} {start_date}
    - For each customer,
        - Label: customer name
        - Button 1: Add Order
        - Button 2: Update Order
        [first only show add order button, then only show update order button once an order is added]
        - Button 3: Edit customer profile [links to /Customer/{Customer_id}, always shows]
        - Table: shows their order, actual_price (quantity * (price - discount); eg. 3 units * ($100 - $10) = $270)
    - To the right hand side, show the product price table (unchangeable here)
    - Button: Add new customer [opens a simple dialog with input fields: name, discount]

/Cycle/Customer/{customer_id}/New_order
    - bindable dataclass for data
    - Editable table: all product name, order quantity (shows last-cycle order quantity for this customer as default value)
    - Table: product price table for reference
    - Button: submit (INSERT INTO)

/Cycle/Customer/{customer_id}/Update_order
    - bindable dataclass for data
    - Editable table: all product name, order quantity (shows the current order quantity for this customer as default value)
    - Table: product price table for reference
    - Button: submit (UPDATE)

/Cycle/Supply
    - bindable dataclass for data
    - Label: cycle {idx} {start_date}
    - Table: 
        - supplier name as row names
        - product name as column names
        - last row is total
    - Button: "Add Supplier" [opens a simple dialogue with input field name]
    - Button: "Auto" automatically fill in the remaining values
    - Button: "Save" (if user tries to leave the page without saving, prompt for saving)
    - Label: Indicates finished if Total for every product is 0
    - Logic: 
        - Total = all customer order for the product - all supplier order for the product
        - Total should be 0 at the end
        - Auto button fills in the last missing row to make sure the Total is 0

/Cycle/Summary
    - Label: cycle {idx} {start_date}
    - Histogram: profit made from each product
    - Histogram: profit made from each customer
    - Line plot: revenue, profit over the last 20 cycles

/Customer
    - For each customer,
        - Link to their profile

/Customer/{Customer_id}
    - bindable dataclass for customer data
    - Inputs fields for: name, discount
    - Plots: to be decided

/Business_report
    - to be decided
