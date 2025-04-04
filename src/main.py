from repository import UserRepository, ProductRepository, Database
from models import User, Product

def main():
    db = Database("app.db")
    db.initialize_db()
    
    user_repo = UserRepository(db)
    product_repo = ProductRepository(db)
    
    new_user = User(username="john_doe", password="secure_password")
    user_id = user_repo.create_user(new_user)
    print(f"Created user with ID: {user_id}")
    
    users = user_repo.get_all()
    print("All users:")
    for user in users:
        print(f"Username: {user.username}, Password: {user.password}")
    
    new_product = Product(name="Laptop", price=999.99)
    product_id = product_repo.create_product(new_product)
    print(f"Created product with ID: {product_id}")
    
    products = product_repo.get_all()
    print("All products:")
    for product in products:
        print(f"Product: {product.name}, Price: ${product.price:.2f}")

if __name__ == "__main__":
    main()


