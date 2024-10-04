from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Customer Model
class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    
    # Define serialization rules
    __serialize_only__ = ('id', 'name', 'reviews')
    __exclude__ = ('reviews.customer',)  # Exclude the customer in reviews

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Relationship to Review
    reviews = db.relationship('Review', back_populates='customer')

    # Association proxy to access items through reviews
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

# Item Model
class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'
    
    # Define serialization rules
    __serialize_only__ = ('id', 'name', 'price', 'reviews')
    __exclude__ = ('reviews.item',)  # Exclude the item in reviews

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Relationship to Review
    reviews = db.relationship('Review', back_populates='item')

    # Association proxy to access customers through reviews
    customers = association_proxy('reviews', 'customer')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

# Review Model
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    # Define serialization rules
    __serialize_only__ = ('id', 'comment', 'customer', 'item')
    __exclude__ = ('customer.reviews', 'item.reviews')  # Exclude reviews in customer and item

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    # Foreign keys to Customer and Item
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    # Relationships
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}, Customer: {self.customer_id}, Item: {self.item_id}>'
