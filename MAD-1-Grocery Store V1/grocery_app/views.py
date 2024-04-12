from flask import Blueprint, render_template,request,redirect,url_for,flash,session
from .models import Category, Product,User,CartItem,PurchaseHistory
from flask_login import login_required, current_user
from . import db
from datetime import datetime


views = Blueprint('views',__name__)

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    # Get all categories and associated products
    categories = Category.query.all()
    products = Product.query.all()
    return render_template("home.html", categories=categories, products=products)

@views.route('/adminhome', methods=['GET', 'POST'])
@login_required
def adminhome():
    # Get all categories created by the admin
    categories = Category.query.filter_by(admin_id=current_user.id).all()
    return render_template("admin_home.html", categories=categories)

# Create a new category
@views.route('/admin/categories/create', methods=['GET', 'POST'])
@login_required
def create_category():
    if request.method == 'POST':
        name = request.form['name']

        # Get the ID of the currently logged-in admin
        admin_id = current_user.id

        # Check if the category already exists
        existing_category = Category.query.filter_by(name=name, admin_id=admin_id).first()
        if existing_category:
            flash('Category already exists.', 'error')
            return redirect(url_for('views.list_categories'))
        
        category = Category(name=name,admin_id=admin_id)
        db.session.add(category)
        db.session.commit()

        flash('Category created successfully.', 'success')
        return redirect(url_for('views.adminhome'))

    return render_template('create_category.html')

# Read (list) all categories
@views.route('/admin/categories')
@login_required
def list_categories():
    categories = Category.query.all()
    return render_template('list_categories.html', categories=categories)

# Update an existing category
@views.route('/admin/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = Category.query.get(category_id)

    if request.method == 'POST':
        category.name = request.form['name']
        db.session.commit()

        flash('Category updated successfully.', 'success')
        return redirect(url_for('views.list_categories'))

    return render_template('edit_category.html', category=category)

# Delete an existing category
@views.route('/admin/categories/<int:category_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get(category_id)

    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()

        flash('Category deleted successfully.', 'success')
        return redirect(url_for('views.list_categories'))

    return render_template('delete_category.html', category=category)


# Create a new product
@views.route('/admin/products/create', methods=['GET', 'POST'])
@login_required
def create_product():
    if request.method == 'POST':
        name = request.form['name']
        rate_per_unit = float(request.form['rate_per_unit'])
        quantity = float(request.form['quantity'])
        section_id = int(request.form['section'])
        unit=request.form['unit'] 
        expiration_date_str = request.form['expiration_date']

        # Convert the string to a Python date object
        try:
            expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()
        except ValueError:
            expiration_date = None  # Handle the case when the date format is invalid

        product = Product(name=name, rate_per_unit=rate_per_unit, quantity=quantity, section_id=section_id,unit=unit,expiration_date=expiration_date)
        db.session.add(product)
        db.session.commit()

        flash('Product created successfully.', 'success')
        return redirect(url_for('views.list_products'))

    sections = Category.query.all()
    return render_template('create_product.html', sections=sections)

# Read (list) all products
@views.route('/admin/products')
@login_required
def list_products():
    products = Product.query.all()
    return render_template('list_products.html', products=products)

# Update an existing product
@views.route('/admin/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    sections = Category.query.all()

    if request.method == 'POST':
        product.name = request.form['name']
        product.rate_per_unit = float(request.form['rate_per_unit'])
        product.quantity = float(request.form['quantity'])
        product.section_id = int(request.form['section'])
        
        # Assuming you have the expiration date as a string from the form or request
        expiration_date_str = request.form['expiration_date']

        # Convert the string to a Python date object
        try:
            expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()
        except ValueError:
            expiration_date = None  # Handle the case when the date format is invalid

        # Now you can use the expiration_date in your update
        product = Product.query.get(product_id)
        if product:
            # Update the product's rate_per_unit and expiration_date
            product.rate_per_unit = float(request.form['rate_per_unit'])
            product.expiration_date = expiration_date

        db.session.commit()

        flash('Product updated successfully.', 'success')
        return redirect(url_for('views.list_products'))

    return render_template('edit_product.html', product=product, sections=sections)

# Delete an existing product
@views.route('/admin/products/<int:product_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)

    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()

        flash('Product deleted successfully.', 'success')
        return redirect(url_for('views.list_products'))

    return render_template('delete_product.html', product=product)

# Search for sections/categories or products based on search_type
@views.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    search_type = request.args.get('search_type', 'sections')  # Default to searching sections

    if search_type == 'sections':
        sections = Category.query.filter(Category.name.contains(query)).all()
        # Fetch the available sections for the dropdown
        sections = Category.query.filter(Category.name.contains(query)).all() # Fetch all sections
        return render_template('search_result.html', query=query, sections=sections, available_sections=sections)

    elif search_type == 'products':
        section_search = request.args.get('section_search')  # Get the selected section
        if section_search:
            products = Product.query.filter(
                Product.name.contains(query),
                Product.section.has(name=section_search)
            ).all()
        else:
            products = Product.query.filter(Product.name.contains(query) | Product.rate_per_unit.contains(query)).all()
        return render_template('search_result.html', query=query, products=products, section_search=section_search)




@views.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    user_id = current_user.id
    quantity = int(request.form['quantity'])

    # Retrieve the product from the database
    product = Product.query.get(product_id)

    # Check if the product exists and if it has an expiration date
    if product and product.expiration_date:
        # Get the current date
        current_date = datetime.now().date()

        # Check if the product has expired
        if product.expiration_date < current_date:
            flash('Product has expired and cannot be added to the cart.', 'danger')
            return redirect(url_for('views.home'))

    # Check if the product is in stock
    if product and product.quantity >= quantity:
        # Check if the product is already in the cart
        cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)

        db.session.commit()
        flash('Product added to cart.', 'success')
    else:
        flash('Insufficient quantity or the product does not exist.', 'danger')

    return redirect(url_for('views.home'))


@views.route('/remove_from_cart/<int:product_id>', methods=['GET'])
@login_required
def remove_from_cart(product_id):
    user_id = current_user.id
    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Product removed from cart.', 'success')

    return redirect(url_for('views.view_cart'))


@views.route('/cart', methods=['GET'])
@login_required
def view_cart():
    user_id = current_user.id
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    total_amount = sum(cart_item.product.rate_per_unit * cart_item.quantity for cart_item in cart_items)

    return render_template('view_cart.html', cart_items=cart_items, total_amount=total_amount)



@views.route('/buy_all', methods=['GET', 'POST'])
@login_required
def buy_all():
    user_id = current_user.id
    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    if request.method == 'POST':
        # Perform the purchase logic here, e.g., update product quantities, create orders, etc.
        for cart_item in cart_items:
            product = Product.query.get(cart_item.product_id)
            if product and product.quantity >= cart_item.quantity:
                # Update product quantity
                product.quantity -= cart_item.quantity

                # Create a purchase history record
                purchase = PurchaseHistory(
                    user_id=user_id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity 
                )
                db.session.add(purchase)
                db.session.delete(cart_item)
                db.session.commit()
            else:
                flash(f"Insufficient quantity for {product.name}. Purchase canceled.", "danger")
                return redirect(url_for('views.view_cart'))

        flash("All items purchased successfully.", "success")
        return redirect(url_for('views.home'))

    return render_template('buy_all.html', cart_items=cart_items)


