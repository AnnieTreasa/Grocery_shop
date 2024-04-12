from flask import render_template, Blueprint
from datetime import datetime, timedelta
import pandas as pd
from grocery_app.models import PurchaseHistory, Product, Category
import plotly.express as px
# Create a Blueprint for the summary route
summary_bp = Blueprint('summary', __name__)

# Define the summary route using the Blueprint
@summary_bp.route('/summary')
def summary():
    # Calculate the date range for the last 7 days (weekly)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # Retrieve purchase history within the date range
    purchase_history = PurchaseHistory.query.filter(
        PurchaseHistory.purchase_date >= start_date,
        PurchaseHistory.purchase_date <= end_date
    ).all()

    # Calculate total sales within the date range
    total_sales = sum(item.product.rate_per_unit * item.quantity for item in purchase_history)

    # Create a dictionary to store total sales per category
    category_sales_data = {}
    
    # Get all categories
    categories = Category.query.all()

    # Populate the category_sales_data dictionary
    for category in categories:
        category_sales_data[category.name] = 0  # Initialize sales for the category

    # Calculate total sales per category
    for item in purchase_history:
        category = item.product.section
        category_sales_data[category.name] += item.product.rate_per_unit * item.quantity

    print(category_sales_data)

    # Create a DataFrame for products and their quantities
    products_data = pd.DataFrame(
        [(product.name, product.quantity, product.section.name,product.expiration_date) for product in Product.query.all()],
        columns=['Product', 'Quantity', 'Category','Expiration_date']
    )

    # Filter products that are out of stock
    out_of_stock_products = products_data[products_data['Quantity'] <= 0].to_dict(orient='records')
    stock_products = products_data[products_data['Quantity'] > 0].to_dict(orient='records')
    stock_products1=stock_products
    
    # Fetch expired products
    expired_products = Product.query.filter(Product.expiration_date < datetime.now().date()).all()

    # Fetch products expiring within 2 days
    expiring_products = Product.query.filter(Product.expiration_date <= (datetime.now() + timedelta(days=2)).date()).all()

    #-------------------graphs----------------------
    
    
    
    # Calculate data for product summary graph
    product_summary_data = {
        'Product': [product['Product'] for product in stock_products],
        'Quantity': [product['Quantity'] for product in stock_products]
    }

    # Calculate data for category-wise distribution graph
    category_distribution_data = {
        'Category': list(category_sales_data.keys()),
        'Total Sales': list(category_sales_data.values())
    }

    # Calculate sales trend over the last 7 days
    sales_trend_data = []
    date_range = [(start_date + timedelta(days=i)).date() for i in range(7)]
    for date in date_range:
        daily_sales = sum(
            getattr(item.product, 'rate_per_unit', 0) * getattr(item, 'quantity', 0)
            for item in purchase_history
            if getattr(item, 'purchase_date', datetime.min).date() == date
        )
        sales_trend_data.append(daily_sales)

    # Print sales trend data for debugging
    print(sales_trend_data)

    # Create a DataFrame for products and their quantities
    products_data = pd.DataFrame(
        [(product.name, product.quantity, product.section.name) for product in Product.query.all()],
        columns=['Product', 'Quantity', 'Category']
    )

    # Filter products that are out of stock
    stock_products = products_data[products_data['Quantity'] > 0]

    # Create bar chart using plotly
    product_bar_chart = px.bar(stock_products, x='Product', y='Quantity', title='Product Distribution')

    # Create pie chart using plotly
    category_pie_chart = px.pie(category_distribution_data, names='Category', values='Total Sales', title='Category Sales Distribution')

    # Convert the charts to HTML and pass them to the template
    product_bar_chart_html = product_bar_chart.to_html(full_html=False)
    category_pie_chart_html = category_pie_chart.to_html(full_html=False)

    #stock_products=list(stock_products)
    # Print the contents of the stock_products list for debugging
    print("Stock products:", stock_products)
    # Render the summary template with the calculated data
    


 
    return render_template(
        "summary.html",
        current_datetime=datetime.now(),
        total_sales=total_sales,
        category_sales_data=category_sales_data,
        out_of_stock_products=out_of_stock_products,
        stock_products=stock_products1,
        product_summary_data=product_summary_data,
        category_distribution_data=category_distribution_data,
        product_bar_chart_html=product_bar_chart_html,
        category_pie_chart_html=category_pie_chart_html,
        expired_products=expired_products,
        expiring_products=expiring_products
    )


    





