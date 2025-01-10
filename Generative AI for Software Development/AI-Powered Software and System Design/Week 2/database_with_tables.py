from sqlalchemy import select, join, create_engine, Table, Column, Integer, String, Float, ForeignKey, MetaData
from sqlalchemy.orm import sessionmaker

# Initialize database engine and metadata
engine = create_engine('sqlite:///ecommerce.db', echo=True)
metadata = MetaData()

# Define Users table
users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('email', String, nullable=False, unique=True)
)

# Define Products table
products = Table('products', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('price', Float, nullable=False)
)

# Define Orders table
orders = Table('orders', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
)

# Define Order_Items table
order_items = Table('order_items', metadata,
    Column('id', Integer, primary_key=True),
    Column('order_id', Integer, ForeignKey('orders.id'), nullable=False),
    Column('product_id', Integer, ForeignKey('products.id'), nullable=False),
    Column('quantity', Integer, nullable=False)
)

# Create all tables
metadata.create_all(engine)

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

def add_sample_data():
    # Add more users
    session.execute(users.insert(), [
        {'name': 'Alice Smith', 'email': 'alice.smith@example.com'},
        {'name': 'Bob Johnson', 'email': 'bob.johnson@example.com'},
        {'name': 'Charlie Brown', 'email': 'charlie.brown@example.com'}
    ])

    # Add more products
    session.execute(products.insert(), [
        {'name': 'Smartphone', 'price': 699.99},
        {'name': 'Tablet', 'price': 299.99},
        {'name': 'Headphones', 'price': 199.99}
    ])

    # Add more orders
    session.execute(orders.insert(), [
        {'user_id': 1},
        {'user_id': 2},
        {'user_id': 3}
    ])

    # Add more order items
    session.execute(order_items.insert(), [
        {'order_id': 1, 'product_id': 1, 'quantity': 1},
        {'order_id': 1, 'product_id': 3, 'quantity': 2},
        {'order_id': 2, 'product_id': 2, 'quantity': 1},
        {'order_id': 3, 'product_id': 1, 'quantity': 3},
        {'order_id': 3, 'product_id': 3, 'quantity': 1}
    ])

    # Commit the changes
    session.commit()

    # Verify the data
    print("Users:", session.execute(users.select()).fetchall())
    print("Products:", session.execute(products.select()).fetchall())
    print("Orders:", session.execute(orders.select()).fetchall())
    print("Order Items:", session.execute(order_items.select()).fetchall())

# Run the function to add sample data
#add_sample_data()

def create_user(name, email):
    """Create a new user."""
    session.execute(users.insert().values(name=name, email=email))
    session.commit()
    print(f"User '{name}' added.")

def update_user_email(user_id, new_email):
    """Update the email of a user."""
    session.execute(users.update().where(users.c.id == user_id).values(email=new_email))
    session.commit()
    print(f"User with ID {user_id} email updated to '{new_email}'.")

def delete_user(user_id):
    """Delete a user."""
    session.execute(users.delete().where(users.c.id == user_id))
    session.commit()
    print(f"User with ID {user_id} deleted.")

def Test_crud_operations():
    # Create a new user
    create_user('John Doe', 'john.doe@example.com')

    # Retrieve and verify the user
    user_result = session.execute(users.select().where(users.c.name == 'John Doe')).fetchone()
    print("Retrieved User:", user_result)

    # Update the user's email
    if user_result:
        update_user_email(user_result.id, 'john.new@example.com')

    # Verify the update
    updated_user_result = session.execute(users.select().where(users.c.id == user_result.id)).fetchone()
    print("Updated User:", updated_user_result)

    # Delete the user
    if updated_user_result:
        delete_user(updated_user_result.id)

    # Verify the deletion
    deleted_user_result = session.execute(users.select().where(users.c.id == updated_user_result.id)).fetchone()
    print("Deleted User:", deleted_user_result)

    # Assertions to check the operations
    assert user_result is not None, "User creation failed"
    assert updated_user_result.email == 'john.new@example.com', "User email update failed"
    assert deleted_user_result is None, "User deletion failed"

    print("CRUD operations test passed!")

# Run the test
#Test_crud_operations()

# Close the session
session.close()


def find_orders_by_user(email):
    # Join users and orders tables
    user_orders = join(users, orders, users.c.id == orders.c.user_id)

    # Construct the query
    query = select(orders).select_from(user_orders).where(users.c.email == email)

    # Execute the query
    result = session.execute(query).fetchall()

    # Print the orders
    print(f"Orders placed by {email}:")
    for order in result:
        print(order)


if __name__ == '__main__':
    # Example usage
    find_orders_by_user('john.doe@example.com')