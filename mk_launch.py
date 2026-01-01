import argparse
import mk_core
import constants
import utils


class Launch:
    def __init__(self):
        self.grocery_app = mk_core.GroceryList()

    print("")
    print("Welcome to the Grocery List app! Let's make shopping easier.")
    print(utils.get_line_delimiter())

    def launch(self, mode="interactive") -> None:
        while True:
            command = input(
                "Enter a command(add, remove, edit, list, export, search, quit):"
            )
            
            if command == "add":

                self.handle_add_command()

            if command == "remove":

                self.handle_remove_command()

            if command == "edit":

                self.handle_edit_command()

            if command == "list":
                self.grocery_app.list_items(self.grocery_app.grocery_list)

            if command == "export":
                self.grocery_app.export_items()

            if command == "search":
                self.handle_search_command()

            if command == "quit":
                break

    def handle_add_command(self):  # This will allow the user to add items.
        name, store, cost, amount, priority, buy = self.get_inputs()
        self.grocery_app.add_item(
            name=name, store=store, cost=cost, amount=amount, priority=priority, buy=buy
        )

        print(f"{name} added to list")
        print(utils.get_line_delimiter())

    def handle_remove_command(self):  # this is the command to remove an item.
        name = input("Which item would you like to remove? ")
        matches = self.grocery_app.search_item_name(name)

        if not matches:
            print(f"I'm sorry, I could not find a match for {name}")

        elif len(matches) > 1:
            for match_num, match in enumerate(matches, start=1):
                match_string = (
                    f"{match_num}. "
                    f"| Name: {match["name"]} "
                    f"| Store: {match["store"]} "
                    f"| Cost: {match["cost"]} "
                    f"| Amount: {match["amount"]} "
                    f"| Priority: {match["priority"]} "
                    f"| Buy: {match["buy"]} |"
                )
                print(match_string)

            item_num = input("\nPlease select the number you would like to remove: ")
            match_item = matches[int(item_num) - 1]
            self.grocery_app.remove_item(match_item.id)
            print(f"\nItem {match_item.name} has been removed.")

        else:
            match_item = matches[0]
            self.grocery_app.remove_item(match_item.id)
            print(f"That item has been removed")

    def handle_edit_command(self):  # This is the command to be used to edit
        item = input("Which item would you like to edit? ")
        matches = self.grocery_app.search_item_name(item)

        if not matches:
            print(f"There are no items twith the name{item}")

        elif len(matches) > 1:
            match_num = 1
            for match in matches:
                match_string = (
                    f"item {match_num} "
                    f"| name: {match["name"]} "
                    f"| store: {match["store"]} "
                    f"| cost: {match["cost"]} "
                    f"| amount: {match["amount"]} "
                    f"| priority: {match["priority"]} "
                    f"| buy: {match["buy"]}"
                )
                print(match_string)
                match_num += 1

            item_num = input("Which item do you want to edit?")
            match_item = matches[int(item_num) - 1]
            name, store, cost, amount, priority, buy = self.get_inputs()
            self.grocery_app.edit_item(
                name, store, cost, amount, priority, buy, match_item.id
            )
        else:
            match_item = matches[0]
            name, store, cost, amount, priority, buy = self.get_inputs()
            self.grocery_app.edit_item(
                name, store, cost, amount, priority, buy, match_item.id
            )

    def handle_search_command(self):
        search_keyword = input(
            "What is the name of the item you would like to search? "
            )
        print(utils.get_line_delimiter())

        print("Searching for matching items...")

        matches = self.grocery_app.search_item_name(search_keyword)
        
        if matches:
            
            print("Theese items match your search. ")
            self.grocery_app.list_items(matches)
                
        else:
            print("No items match the provided search item")


    def get_inputs(self):
        """The following functions are for the inputs
            to collect information for the list.
        export

                Returns:
                    string:  item to be added as a string
        """
        
        name = self.get_name_input()
        print(utils.get_line_delimiter())

        store = self.get_store_input()
        print(utils.get_line_delimiter())

        cost = self.get_cost_input()
        print(utils.get_line_delimiter())

        amount = self.get_amount_input()
        print(utils.get_line_delimiter())

        priority = self.get_priority_input()
        print(utils.get_line_delimiter())

        buy = self.get_buy_input()
        print(utils.get_line_delimiter())

        return name, store, cost, amount, priority, buy
    
    @staticmethod
    def get_name_input():
        """
        Get the user input for the name attribute.

        Returns:
            name(str) The name of the item

        """
        print("Enter a name for the item. (ex. ice cream")
        # Get the name input
        name = input("Item name: ").strip()

        if not name:
            name = constants.NAME_DEFAULT

        return name
    
    @staticmethod
    def get_store_input():
        print("Enter the name of the store for the item. (ex. Walmart)")

        # Get the store input
        store = input("Store name (or 'skip' to leave blank): ").strip()

        # No store provided, set to default
        if not store:
            store = constants.STORE_DEFAULT

        return store

    @staticmethod
    def get_cost_input():
        print("Enter the cost of the item. (ex. 5.25)")

        while True:
            # Get the cost input
            cost = input("Item price: ").strip()

            # No cost input provided, set to default
            if not cost:
                cost = constants.COST_DEFAULT
                break

            try:
                # Convert the cost to a float
                cost = float(cost)
                break

            # Unable to convert the cost to a float
            except ValueError:
                print("Invalid input. Please enter a valid price.")

        return cost
    
    @staticmethod
    def get_amount_input():
        print("Enter the amount you need to get. (ex. 5)")
        while True:
            # Get the amount input
            amount = input("Item quantity: ").strip()
            # Amount not provided, set to default
            if not amount:
                amount = constants.AMOUNT_DEFAULT
                break

            try:
                # Convert the amount to an int
                amount = int(amount)
                # Amount must be at least 1
                if amount > 0:
                    break

                print("Quantity must be a positive number.")

            # Unable to convert amount to an int
            except ValueError:
                print("Invalid input. Please enter a valid quantity.")

        return amount

    @staticmethod
    def get_priority_input():
        p_min = constants.PRIORITY_MIN
        p_max = constants.PRIORITY_MAX

        print(f"Enter the priority for the item between " f"{p_min}-{p_max}. (ex. 2)")

        while True:
            # Get the priority input
            priority = input("Priority: ").strip()

            # No input provided, set to default
            if not priority:
                constants.PRIORITY_DEFAULT
                break

            try:
                # Convert the priority to an int
                priority = int(priority)

                # Check priority is within min to max
                if p_min <= priority <= p_max:
                    break

            # Failed to convert priority to an int
            except ValueError:
                print(
                    f"Invalid input. Please enter a number between "
                    f"{p_min} and {p_max}."
                )

        return priority
    
    @staticmethod
    def get_buy_input():
        print("Enter if this item should be purchased now. (ex. yes)")

        while True:
            # Get the buy input
            buy = input("Buy: ").strip().lower()

            # No buy input provided
            if not buy:
                buy = constants.BUY_DEFAULT
                break

            # Buy input is true
            if buy in constants.BUY_TRUE:
                buy = True
                break

            # Buy input is false
            elif buy in constants.BUY_FALSE:
                buy = False
                break

            # Buy input was not valid
            else:
                print("Invalid input. Please enter true|yes OR false|no")

        return buy

    # Call the function
if __name__ == "__main__":
    app = Launch()
    app.launch()
