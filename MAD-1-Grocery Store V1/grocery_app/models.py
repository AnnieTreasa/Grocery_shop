from grocery_app import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    firstname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False,default="User")
    is_manager = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'<User {self.firstname}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category_type = db.Column(db.String(100), nullable=False,default="Null")
    image = db.Column(db.String(100), nullable=True,default="Null")
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin = db.relationship('User', backref=db.backref('categories', lazy=True))
    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    rate_per_unit = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    section = db.relationship('Category', backref=db.backref('products', lazy=True))
    cart_items_relation = db.relationship('CartItem', backref='product', lazy=True)  # Use a different name
    expiration_date = db.Column(db.Date)


    def __repr__(self):
        return f'<Product {self.name} - Unit: {self.unit} - Rate per unit: {self.rate_per_unit} - Quantity: {self.quantity}>'

    # Add a method to check if the product is expired
    def is_expired(self):
        if self.expiration_date is None:
            return False  # If no expiration date is set, the product is not expired
        current_date = datetime.now().date()
        return current_date > self.expiration_date
    
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    cart_item_product = db.relationship('Product', backref='cart_items', lazy=True)

    def __repr__(self):
        return f'<CartItem - User: {self.user_id}, Product: {self.product_id}, Quantity: {self.quantity}>'

class PurchaseHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    purchase_date = db.Column(db.DateTime, default=func.now())
    product = db.relationship('Product', backref='purchase_history', lazy=True)
    
    def __repr__(self):
        return f'<PurchaseHistory - User: {self.user_id}, Product: {self.product_id}, Date: {self.purchase_date}>'