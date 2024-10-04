from app import app, db
from server.models import Customer, Item, Review

class TestSerialization:
    '''Models in models.py'''

    def test_customer_is_serializable(self):
        '''Customer is serializable'''
        with app.app_context():
            c = Customer(name='Phil')
            db.session.add(c)
            db.session.commit()
            
            # Create a review only after committing the customer
            item = Item(name='Test Item', price=10.0)
            db.session.add(item)
            db.session.commit()
            
            r = Review(comment='great!', customer=c, item=item)
            db.session.add(r)
            db.session.commit()
            
            customer_dict = c.to_dict()  # Change to serialize()
            assert customer_dict['id']
            assert customer_dict['name'] == 'Phil'
            assert customer_dict['reviews']
            assert 'customer' not in customer_dict['reviews'][0]  # Adjusted to access the first review

    def test_item_is_serializable(self):
        '''Item is serializable'''
        with app.app_context():
            i = Item(name='Insulated Mug', price=9.99)
            db.session.add(i)
            db.session.commit()
            
            c = Customer(name='Phil')
            db.session.add(c)
            db.session.commit()

            # Create a review only after committing the item
            r = Review(comment='great!', item=i, customer=c)
            db.session.add(r)
            db.session.commit()

            item_dict = i.to_dict()  # Change to serialize()
            assert item_dict['id']
            assert item_dict['name'] == 'Insulated Mug'
            assert item_dict['price'] == 9.99
            assert item_dict['reviews']
            assert 'item' not in item_dict['reviews'][0]  # Adjusted to access the first review

    def test_review_is_serializable(self):
        '''Review is serializable'''
        with app.app_context():
            c = Customer(name='Phil')
            i = Item(name='Insulated Mug', price=9.99)
            db.session.add_all([c, i])
            db.session.commit()

            # Now create the review with both customer and item present
            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            review_dict = r.to_dict()  # Change to serialize()
            assert review_dict['id']
            assert review_dict['customer']
            assert review_dict['item']
            assert review_dict['comment'] == 'great!'
            assert 'reviews' not in review_dict['customer']
            assert 'reviews' not in review_dict['item']
