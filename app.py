import csv
import re

from collections import OrderedDict
from datetime import date

from peewee import *


db = SqliteDatabase("inventory.db")

class Product(Model):
    product_id = AutoField()
    product_name = CharField(max_length=255, unique=True)
    product_price = IntegerField(default=0)
    product_quantity = IntegerField(default=0)
    date_updated = DateField()

    def __str__(self):
        r = "id: {}\n".format(self.id)
        r += "Name: {}\n".format(self.name)

    class Meta:
        database = db


def clean_product(name=" ", price="", quantity="", updated="01/01/01"):
    """ Cleans the data to be entered """
    cln_prod = {"name": name.strip(), "quantity": int(quantity)}
    temp_price = price.replace("$", "").split(".")
    cln_prod["price"] = int(temp_price[0]) * 100 + int(temp_price[1])
    temp_update = updated.split("/")
    cln_prod["updated"] = date(int(temp_update[2]), int(temp_update[0]), int(temp_update[1]))
    return cln_prod
     

def fill_invetory():
    """ Fills the inventory database """
    with open("store-inventory/inventory.csv", newline="") as file:
        stuff = csv.DictReader(file)
        for i in stuff:
            cln_prod = clean_product(
                i["product_name"],
                i["product_price"],
                i["product_quantity"],
                i["date_updated"])
                
            add_to_inventory(
                cln_prod["name"],
                cln_prod["price"],
                cln_prod["quantity"],
                cln_prod["updated"])      


def add_to_inventory(name="", price=0, quantity=0, updated="01-01-01"):
    """ Add new product after being cleaned """
    try:
        Product.create(
            product_name=name,
            product_price=price,
            product_quantity=quantity,
            date_updated=updated)
    except IntegrityError:
        prod_in_date = Product.select().where(Product.product_name == name).get().date_updated
        if prod_in_date <= updated:
            print("Product repeated las update saved.")
            print("Name: {}".format(Product.select().where(Product.product_name == name).get().product_name))
            up = Product.update(
                product_price=price,
                product_quantity=quantity,
                date_updated=updated).where(Product.product_name == name)
            up.execute()   

def view_product_by_id():
    """ View product by id."""
    while True:
        min_id = Product.select().order_by(Product.product_id.asc()).get().product_id 
        max_id = Product.select().order_by(Product.product_id.desc()).get().product_id 
        opt = input("Please enter and id ({} - {}, r to return): ".format(min_id, max_id))
        if opt.lower().strip() == "r":
            break
        else:
            try:    
                prod = Product.select().where(Product.product_id == int(opt)).get()
                print("\nid: {}\nName: {}".format(prod.product_id, prod.product_name))
                print("=====" + "=" * len(prod.product_name))
                print("Price: {}\nQuantity: {}\nDate Updated: {}\n".format(prod.product_price, prod.product_quantity, prod.date_updated))
            except ValueError:
                print("Value must be an int or r")
            except:
                print("The id must be between {} and {}".format(min_id, max_id))


def add_new_product():
    """ Add new product to the database by terminal."""
    name = input("Please enter name: ")
    price = None
    while not price:
        price = re.match(r'^[$]{1}\d+[.]+\d{2}$', input("Please enter a price (in format $4.30): "))
        if price is None:
            print("Please input the price in the correct format.")
        else:
            price = price.group()

    quantity = None
    while not isinstance(quantity, int):
        try: 
            quantity = int(input("Please input the quantity: "))
            if quantity < 0:
                quantity = None
                print("Quantity must be greater or equal than 0.")
        except ValueError:
            print("The quantity must be an int.")
        
    updated = date.today()
    cln_prod = clean_product(name, price, quantity)
    add_to_inventory(cln_prod["name"], cln_prod["price"], cln_prod["quantity"], updated)


def backup():
    """ Backup the database as csv. """
    with open("store-inventory/backup.csv", "w") as bak:
        field_names = ["product_name", "product_price", "product_quantity", "date_updated"]
        wrtr = csv.DictWriter(bak, fieldnames=field_names)
        wrtr.writeheader()
        for i in Product:
            wrtr.writerow({
                "product_name" : i.product_name,
                "product_price": i.product_price,
                "product_quantity": i.product_quantity,
                "date_updated": str(i.date_updated.month)+"/"+str(i.date_updated.day)+"/"+str(i.date_updated.year)
            })
        print("A backup was created in store-inventory/backup.csv.\n")
    

def menu_loop():
    choice = None
    while choice != "q":
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("Choose an option: ").lower().strip()
        print("\n")
        if choice in menu:
            menu[choice]()
        elif choice != "q":
            print("You must choose a valid option.")


menu = OrderedDict([
    ("a", add_new_product),
    ("b", backup),
    ("v", view_product_by_id)
])


if __name__ == "__main__":
    db.connect()
    db.create_tables([Product], safe=True)
    fill_invetory()
    menu_loop()