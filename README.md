# techdegree-project-4 _Store Inventory_

```
class Product(Model)
```
The database table model that includes:
- id = AutoField()
- name = CharField(max_length=255, unique=True)
- price = IntegerField(default=0)
- quantity = IntegerField(default=0)
- updated = DateField()


```
def clean_product(name=" ", price="", quantity="", updated="01/01/01")
```
Cleans the data to be entered into the database.


```
def fill_invetory():
```
Fills the inventory database with the information in the csv file.

```
def add_to_inventory(name="", price=0, quantity=0, updated="01-01-01")
```
Add new product after being cleaned.

```
def view_product_by_id()
```
Displays a product after being searched by its id

```
def add_new_product()
```
Adds a new product form a terminal prompt

```
def backup()
```
Backup the database as a csv file.