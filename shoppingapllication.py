from pymongo import MongoClient

class Shop:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['shop_db']
        self.customers = self.db['customers']
        self.uamount = 0
        self.bill = 0
        self.name = ''
        self.item = {
            0: 'Rice 1 sack - 1250 rs',
            1: 'Dal 1 kg - 250 rs',
            2: 'Soap - 45 rs',
            3: 'Shampoo - 120 rs',
            4: 'Oil - 750 rs',
            5: 'Clips - 10 rs',
            6: 'Carrot - 120 rs',
            7: 'Potato - 70 rs'
        }
        self.product = ['Rice', 'Dal', 'Soap', 'Shampoo', 'Oil', 'Clips', 'Carrot', 'Potato']
        self.price = [1250, 250, 45, 120, 750, 10, 120, 70]
        self.stock = [50, 100, 250, 50, 50, 50, 50, 50]  # Item stocks
        self.usercart = {}

    def customer(self, a, p):
        self.name = a
        self.uamount = p

    def save_customer(self):
        customer_data = {
            'name': self.name,
            'wallet': self.uamount,
            'cart': self.usercart,
            'bill': self.bill
        }
        self.customers.insert_one(customer_data)

    def listitem(self):
        print("\nList of items available:")
        for key, value in self.item.items():
            print(f"{key}. {value}")

    def buyitem(self, a, q):
        try:
            if a >= len(self.price) or a < 0:
                raise ValueError("Invalid item number.")
            if q > self.stock[a]:
                print(f"Sorry, we only have {self.stock[a]} units of {self.product[a]} in stock.")
                return
            if self.price[a] * q <= self.uamount:
                self.uamount -= self.price[a] * q
                self.stock[a] -= q
                self.usercart[self.product[a]] = self.usercart.get(self.product[a], 0) + q
                self.bill += self.price[a] * q
                print(f"{self.product[a]} added to cart.")
            else:
                print('Insufficient money to buy.')
        except Exception as e:
            print("Enter a valid item number (0 to 7).", e)

    def bills(self):
        print("---------------------------")
        print(f"CUSTOMER NAME: {self.name}")
        print("---------Bill--------------")
        print("(Item, Quantity) Price")
        for item, qty in self.usercart.items():
            item_index = self.product.index(item)
            print(f"{item} ({qty}) - {self.price[item_index] * qty} rs")
        print("----------------------------")
        print(f"Total bill amount = {self.bill} rs")
        print(f"Balance amount in wallet = {self.uamount} rs")
        print("----------------------------")
        self.save_customer()

    def stocks(self):
        print('--------Stock available in stores----------')
        for idx, (product, stock) in enumerate(zip(self.product, self.stock)):
            print(f"{idx}. {product}: {stock} units")
        print("--------------------------------------------")

    def customer_history(self, customer_name):
        print(f"--- Transaction History for {customer_name} ---")
        transactions = self.customers.find({'name': customer_name})
        for transaction in transactions:
            print(f"Name: {transaction['name']}")
            print(f"Wallet: {transaction['wallet']} rs")
            print("Cart:", transaction['cart'])
            print(f"Total Bill: {transaction['bill']} rs")
            print("----------------------------")


print("---------------WELCOME TO MURUGAN STORES-------------------")
shop = Shop()
action = input("Do you want to (1) Shop or (2) View Customer History? Enter 1 or 2: ")

if action == '1':
    a1 = input("Enter your name: ")
    p1 = int(input("Enter your wallet amount: "))
    shop.customer(a1, p1)

    while True:
        shop.listitem()
        s = int(input("Enter the item number to buy: "))
        q = int(input("Enter the quantity of the item: "))
        shop.buyitem(s, q)
        pl = int(input("Press 1 to continue buying or 0 to calculate bill: "))
        if pl == 0:
            break

    shop.bills()
    shop.stocks()

elif action == '2':
    customer_name = input("Enter the customer's name to view history: ",)
    
    shop.customer_history(customer_name)

else:
    print("Invalid option. Please restart the program.")
