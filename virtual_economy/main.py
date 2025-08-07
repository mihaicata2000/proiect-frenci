# Main file for the virtual economy simulation
import uuid
from datetime import datetime

class Transaction:
    """Represents a single transaction."""
    def __init__(self, transaction_type, from_user, to_user, amount, item_name=None, quantity=None):
        """
        Initializes a Transaction instance.

        Args:
            transaction_type (str): The type of transaction (e.g., 'buy', 'sell', 'transfer').
            from_user (User): The user initiating the transaction.
            to_user (User): The user receiving the transaction.
            amount (float): The amount of the transaction.
            item_name (str, optional): The name of the item being transacted. Defaults to None.
            quantity (int, optional): The quantity of the item being transacted. Defaults to None.
        """
        self.transaction_id = str(uuid.uuid4())
        self.timestamp = datetime.now()
        self.transaction_type = transaction_type
        self.from_user = from_user
        self.to_user = to_user
        self.amount = amount
        self.item_name = item_name
        self.quantity = quantity

    def __str__(self):
        """Returns a string representation of the transaction."""
        return (f"Transaction ID: {self.transaction_id}\n"
                f"Timestamp: {self.timestamp}\n"
                f"Type: {self.transaction_type}\n"
                f"From: {self.from_user.name if self.from_user else 'Marketplace'}\n"
                f"To: {self.to_user.name if self.to_user else 'Marketplace'}\n"
                f"Amount: {self.amount}\n"
                f"Item: {self.item_name if self.item_name else 'N/A'}\n"
                f"Quantity: {self.quantity if self.quantity else 'N/A'}")

class TransactionHistory:
    """Manages the history of all transactions."""
    def __init__(self):
        """Initializes a TransactionHistory instance."""
        self.transactions = []

    def add_transaction(self, transaction):
        """
        Adds a transaction to the history.

        Args:
            transaction (Transaction): The transaction to add.
        """
        self.transactions.append(transaction)

    def get_user_history(self, user):
        """
        Retrieves the transaction history for a specific user.

        Args:
            user (User): The user whose transaction history is to be retrieved.

        Returns:
            list: A list of transactions involving the user.
        """
        user_history = []
        for transaction in self.transactions:
            if transaction.from_user == user or transaction.to_user == user:
                user_history.append(transaction)
        return user_history

class Wallet:
    """Represents a user's wallet."""
    def __init__(self, owner, balance=100.0):
        """
        Initializes a Wallet instance.

        Args:
            owner (str): The name of the owner of the wallet.
            balance (float): The initial balance of the wallet.
        """
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        """
        Deposits a specified amount into the wallet.

        Args:
            amount (float): The amount to deposit.

        Returns:
            bool: True if the deposit was successful, False otherwise.
        """
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        """
        Withdraws a specified amount from the wallet.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            bool: True if the withdrawal was successful, False otherwise.
        """
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

class User:
    """Represents a user in the virtual economy."""
    def __init__(self, name):
        """
        Initializes a User instance.

        Args:
            name (str): The name of the user.
        """
        self.user_id = str(uuid.uuid4())
        self.name = name
        self.wallet = Wallet(owner=self.name)
        self.transaction_history = []

    def transfer_funds(self, recipient, amount, transaction_history):
        """
        Transfers funds from the user's wallet to another user's wallet.

        Args:
            recipient (User): The user who will receive the funds.
            amount (float): The amount to transfer.
            transaction_history (TransactionHistory): The transaction history to record the transaction.

        Returns:
            bool: True if the transfer was successful, False otherwise.
        """
        if self.wallet.withdraw(amount):
            recipient.wallet.deposit(amount)
            transaction = Transaction(
                transaction_type='transfer',
                from_user=self,
                to_user=recipient,
                amount=amount
            )
            transaction_history.add_transaction(transaction)
            print(f"{self.name} transferred {amount} to {recipient.name}.")
            return True
        else:
            print(f"Error: {self.name} has insufficient funds to transfer.")
            return False

class Item:
    """Represents an item in the marketplace."""
    def __init__(self, name, price, quantity):
        """
        Initializes an Item instance.

        Args:
            name (str): The name of the item.
            price (float): The price of the item.
            quantity (int): The available quantity of the item.
        """
        self.name = name
        self.price = price
        self.quantity = quantity

class Marketplace:
    """Represents the marketplace where users can buy and sell items."""
    def __init__(self, transaction_history):
        """
        Initializes a Marketplace instance.

        Args:
            transaction_history (TransactionHistory): The transaction history to record transactions.
        """
        self.items = {}
        self.transaction_history = transaction_history

    def add_item(self, item):
        """
        Adds an item to the marketplace.

        Args:
            item (Item): The item to add to the marketplace.
        """
        self.items[item.name] = item

    def buy_item(self, user, item_name, quantity):
        """
        Allows a user to buy an item from the marketplace.

        Args:
            user (User): The user who is buying the item.
            item_name (str): The name of the item to buy.
            quantity (int): The quantity of the item to buy.

        Returns:
            bool: True if the purchase was successful, False otherwise.
        """
        if item_name not in self.items:
            print(f"Error: Item '{item_name}' not found in the marketplace.")
            return False

        item = self.items[item_name]
        if item.quantity < quantity:
            print(f"Error: Not enough '{item_name}' in stock.")
            return False

        total_cost = item.price * quantity
        if user.wallet.withdraw(total_cost):
            item.quantity -= quantity
            transaction = Transaction(
                transaction_type='buy',
                from_user=None,  # Marketplace
                to_user=user,
                amount=total_cost,
                item_name=item_name,
                quantity=quantity
            )
            self.transaction_history.add_transaction(transaction)
            print(f"{user.name} bought {quantity} of {item_name} for {total_cost}.")
            return True
        else:
            print(f"Error: {user.name} has insufficient funds to buy {item_name}.")
            return False

    def sell_item(self, user, item_name, quantity):
        """
        Allows a user to sell an item to the marketplace.

        Args:
            user (User): The user who is selling the item.
            item_name (str): The name of the item to sell.
            quantity (int): The quantity of the item to sell.

        Returns:
            bool: True if the sale was successful, False otherwise.
        """
        if item_name not in self.items:
            print(f"Error: Item '{item_name}' not found in the marketplace.")
            return False

        item = self.items[item_name]
        total_value = item.price * quantity
        user.wallet.deposit(total_value)
        item.quantity += quantity
        transaction = Transaction(
            transaction_type='sell',
            from_user=user,
            to_user=None,  # Marketplace
            amount=total_value,
            item_name=item_name,
            quantity=quantity
        )
        self.transaction_history.add_transaction(transaction)
        print(f"{user.name} sold {quantity} of {item_name} for {total_value}.")
        return True

def run_tests():
    """Runs a series of tests to verify the functionality of the virtual economy."""
    print("--- Running Tests ---")

    # Setup
    transaction_history = TransactionHistory()
    marketplace = Marketplace(transaction_history)
    user1 = User("Alice")
    user2 = User("Bob")

    # Test Case 1: Add items to marketplace
    marketplace.add_item(Item(name="Wood", price=5.0, quantity=100))
    assert "Wood" in marketplace.items
    print("Test Case 1 Passed: Item added to marketplace.")

    # Test Case 2: User buys an item
    user1.wallet.deposit(100) # Give Alice some money. Initial balance is 100, so now it's 200.
    marketplace.buy_item(user1, "Wood", 10) # Buys 10 wood for 50.
    assert user1.wallet.balance == 150
    assert marketplace.items["Wood"].quantity == 90
    print("Test Case 2 Passed: User successfully bought an item.")

    # Test Case 3: User sells an item
    marketplace.sell_item(user1, "Wood", 5) # Sells 5 wood for 25.
    assert user1.wallet.balance == 175
    assert marketplace.items["Wood"].quantity == 95
    print("Test Case 3 Passed: User successfully sold an item.")

    # Test Case 4: User transfers funds
    user1.transfer_funds(user2, 25, transaction_history) # Transfers 25 to Bob.
    assert user1.wallet.balance == 150
    assert user2.wallet.balance == 125
    print("Test Case 4 Passed: Fund transfer successful.")

    # Test Case 5: Transaction history
    history = transaction_history.get_user_history(user1)
    assert len(history) == 3
    print("Test Case 5 Passed: Transaction history is accurate.")

    print("--- All Tests Passed ---")

def main():
    """Main function to run the virtual economy simulation."""
    run_tests_choice = input("Run tests before starting the simulation? (y/n): ")
    if run_tests_choice.lower() == 'y':
        run_tests()

    transaction_history = TransactionHistory()
    marketplace = Marketplace(transaction_history)
    users = {}

    # Add some initial items to the marketplace
    marketplace.add_item(Item(name="Lumber", price=10.0, quantity=100))
    marketplace.add_item(Item(name="Iron Ore", price=25.0, quantity=50))
    marketplace.add_item(Item(name="Gold Ore", price=100.0, quantity=10))

    while True:
        print("\n--- Virtual Economy Menu ---")
        print("1. Create User")
        print("2. View User Balance")
        print("3. View Marketplace Items")
        print("4. Buy Item")
        print("5. Sell Item")
        print("6. Transfer Funds")
        print("7. View User Transaction History")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter user name: ")
            if name in users:
                print("Error: User with that name already exists.")
            else:
                user = User(name)
                users[name] = user
                print(f"User '{name}' created successfully.")

        elif choice == '2':
            name = input("Enter user name: ")
            if name in users:
                user = users[name]
                print(f"{user.name}'s balance: {user.wallet.balance}")
            else:
                print("Error: User not found.")

        elif choice == '3':
            print("\n--- Marketplace Items ---")
            for item_name, item in marketplace.items.items():
                print(f"Item: {item.name}, Price: {item.price}, Quantity: {item.quantity}")

        elif choice == '4':
            user_name = input("Enter your user name: ")
            if user_name in users:
                user = users[user_name]
                item_name = input("Enter the item to buy: ")
                try:
                    quantity = int(input("Enter the quantity: "))
                    marketplace.buy_item(user, item_name, quantity)
                except ValueError:
                    print("Error: Invalid quantity.")
            else:
                print("Error: User not found.")

        elif choice == '5':
            user_name = input("Enter your user name: ")
            if user_name in users:
                user = users[user_name]
                item_name = input("Enter the item to sell: ")
                try:
                    quantity = int(input("Enter the quantity: "))
                    marketplace.sell_item(user, item_name, quantity)
                except ValueError:
                    print("Error: Invalid quantity.")
            else:
                print("Error: User not found.")

        elif choice == '6':
            from_user_name = input("Enter your user name: ")
            if from_user_name in users:
                from_user = users[from_user_name]
                to_user_name = input("Enter the recipient's user name: ")
                if to_user_name in users:
                    to_user = users[to_user_name]
                    try:
                        amount = float(input("Enter the amount to transfer: "))
                        from_user.transfer_funds(to_user, amount, transaction_history)
                    except ValueError:
                        print("Error: Invalid amount.")
                else:
                    print("Error: Recipient user not found.")
            else:
                print("Error: User not found.")

        elif choice == '7':
            user_name = input("Enter user name: ")
            if user_name in users:
                user = users[user_name]
                history = transaction_history.get_user_history(user)
                if not history:
                    print(f"No transactions found for {user.name}.")
                else:
                    print(f"\n--- Transaction History for {user.name} ---")
                    for transaction in history:
                        print(transaction)
                        print("-" * 20)
            else:
                print("Error: User not found.")

        elif choice == '8':
            print("Exiting the virtual economy simulation.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
