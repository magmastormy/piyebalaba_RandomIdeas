"""
Modern Record Keeper Application
A refactored version of the quantity tracker with improved structure and functionality.
"""

import sys
import json
import os
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import datetime


@dataclass
class Transaction:
    """Data class representing a transaction record."""
    name: str
    item: str
    amount: int
    transaction_type: str  # "Incoming" or "Outgoing"
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.datetime.now().isoformat()


class RecordKeeper:
    """Main application class for the Record Keeper system."""
    
    def __init__(self, data_file: str = "transaction_data.json"):
        self.data_file = Path(data_file)
        self.transactions: List[Transaction] = []
        self.load_data()
    
    def load_data(self) -> None:
        """Load transaction data from file."""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.transactions = [Transaction(**item) for item in data]
            else:
                self.transactions = []
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading data: {e}")
            self.transactions = []
    
    def save_data(self) -> None:
        """Save transaction data to file."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump([asdict(transaction) for transaction in self.transactions], f, indent=2)
        except IOError as e:
            print(f"Error saving data: {e}")
    
    def add_transaction(self, name: str, item: str, amount: int, transaction_type: str) -> None:
        """Add a new transaction."""
        # Remove plural 's' if present
        if item.lower().endswith('s') and len(item) > 1:
            item = item[:-1]
        
        transaction = Transaction(
            name=name.strip().capitalize(),
            item=item.strip().capitalize(),
            amount=amount,
            transaction_type=transaction_type.strip().capitalize()
        )
        self.transactions.append(transaction)
        self.save_data()
    
    def get_all_items(self) -> Dict[str, int]:
        """Get dictionary of all items with their total quantities."""
        items = {}
        for transaction in self.transactions:
            items[transaction.item] = items.get(transaction.item, 0) + transaction.amount
        return items
    
    def get_all_persons(self) -> Dict[str, int]:
        """Get dictionary of all persons with their transaction counts."""
        persons = {}
        for transaction in self.transactions:
            persons[transaction.name] = persons.get(transaction.name, 0) + 1
        return persons
    
    def get_transactions_by_person(self, name: str) -> List[Transaction]:
        """Get all transactions for a specific person."""
        return [t for t in self.transactions if t.name.lower() == name.lower()]
    
    def get_transactions_by_item(self, item: str) -> List[Transaction]:
        """Get all transactions for a specific item."""
        return [t for t in self.transactions if t.item.lower() == item.lower()]
    
    def get_transactions_by_type(self, transaction_type: str) -> List[Transaction]:
        """Get all transactions of a specific type."""
        return [t for t in self.transactions if t.transaction_type.lower() == transaction_type.lower()]
    
    def get_recent_transactions(self, count: int) -> List[Transaction]:
        """Get the most recent transactions."""
        return self.transactions[-count:] if count <= len(self.transactions) else self.transactions
    
    def delete_transaction(self, index: int) -> bool:
        """Delete a transaction by index."""
        if 0 <= index < len(self.transactions):
            del self.transactions[index]
            self.save_data()
            return True
        return False
    
    def update_transaction(self, index: int, field: str, new_value: str) -> bool:
        """Update a specific field of a transaction."""
        if 0 <= index < len(self.transactions):
            transaction = self.transactions[index]
            if field == "name":
                transaction.name = new_value.strip().capitalize()
            elif field == "item":
                transaction.item = new_value.strip().capitalize()
            elif field == "amount":
                transaction.amount = int(new_value)
            elif field == "transaction_type":
                transaction.transaction_type = new_value.strip().capitalize()
            self.save_data()
            return True
        return False


class UserInterface:
    """Handles all user interface operations."""
    
    def __init__(self, record_keeper: RecordKeeper):
        self.record_keeper = record_keeper
    
    @staticmethod
    def display_header():
        """Display the application header."""
        print("\n" + "=" * 50)
        print("         MODERN QUANTITY TRACKER")
        print("            Record Keeper v2.0")
        print("=" * 50)
    
    @staticmethod
    def display_section_header(title: str):
        """Display a section header."""
        print(f"\n{'-' * 20} {title} {'-' * 20}")
    
    def display_main_menu(self):
        """Display the main menu and get user choice."""
        stats = self.get_statistics()
        print(f"\nRecords: {stats['total_records']} | Items: {stats['total_items']} | Clients: {stats['total_clients']}")
        print("\nMAIN MENU:")
        print("1. [Add] - Add New Record")
        print("2. [View] - View Records")
        print("3. [Edit] - Modify Records")
        print("4. [Help] - Show Help")
        print("5. [Quit] - Exit Program")
        
        return input("\nYour choice: ").lower().strip()
    
    def get_statistics(self) -> Dict[str, int]:
        """Get application statistics."""
        return {
            'total_records': len(self.record_keeper.transactions),
            'total_items': len(self.record_keeper.get_all_items()),
            'total_clients': len(self.record_keeper.get_all_persons())
        }
    
    def add_records_interface(self):
        """Interface for adding new records."""
        self.display_section_header("ADD RECORDS")
        
        try:
            count = int(input("Number of records to add: "))
            print("\nEnter: Client_name Item_name Amount Type(Incoming/Outgoing)")
            print("Separate each field with a space.\n")
            
            for i in range(1, count + 1):
                while True:
                    try:
                        user_input = input(f"Record {i}: ").strip().split()
                        if len(user_input) != 4:
                            print("Please enter exactly 4 fields separated by spaces.")
                            continue
                        
                        name, item, amount, trans_type = user_input
                        amount = int(amount)
                        
                        if trans_type.lower() not in ['incoming', 'outgoing']:
                            print("Transaction type must be 'Incoming' or 'Outgoing'")
                            continue
                        
                        self.record_keeper.add_transaction(name, item, amount, trans_type)
                        break
                    except ValueError:
                        print("Amount must be a valid number.")
                    except Exception as e:
                        print(f"Error: {e}")
            
            print(f"\n{count} record(s) added successfully!")
        except ValueError:
            print("Please enter a valid number.")
    
    def view_menu(self):
        """Display the view menu and handle choices."""
        self.display_section_header("VIEW RECORDS")
        
        print("1. All Items")
        print("2. All Clients")
        print("3. By Transaction Type")
        print("4. Recent Records")
        print("5. All Transaction History")
        print("6. Specific Item")
        print("7. Specific Person")
        print("8. Advanced Search")
        print("9. Return to Main Menu")
        
        choice = input("\nYour choice: ").lower().strip()
        
        if choice in ['1', 'allitems']:
            self.view_all_items()
        elif choice in ['2', 'allclients']:
            self.view_all_clients()
        elif choice in ['3', 'transactiontype']:
            self.view_by_transaction_type()
        elif choice in ['4', 'recent']:
            self.view_recent_records()
        elif choice in ['5', 'history']:
            self.view_all_history()
        elif choice in ['6', 'item']:
            self.view_specific_item()
        elif choice in ['7', 'person']:
            self.view_specific_person()
        elif choice in ['8', 'search']:
            self.advanced_search()
        elif choice in ['9', 'main']:
            return
        else:
            print("Invalid choice!")
            self.view_menu()
    
    def view_all_items(self):
        """Display all items with their quantities."""
        items = self.record_keeper.get_all_items()
        if not items:
            print("No items found!")
            return
        
        print(f"\n{'No.':<4}{'Item Name':<20}{'Total Quantity':<15}")
        print("-" * 40)
        for i, (item, quantity) in enumerate(items.items(), 1):
            print(f"{i:<4}{item:<20}{quantity:<15}")
    
    def view_all_clients(self):
        """Display all clients."""
        persons = self.record_keeper.get_all_persons()
        if not persons:
            print("No clients found!")
            return
        
        print(f"\n{'No.':<4}{'Client Name':<20}{'Transactions':<15}")
        print("-" * 40)
        for i, (person, count) in enumerate(persons.items(), 1):
            print(f"{i:<4}{person:<20}{count:<15}")
    
    def view_by_transaction_type(self):
        """Display transactions by type."""
        trans_type = input("Enter type (Incoming/Outgoing): ").strip()
        transactions = self.record_keeper.get_transactions_by_type(trans_type)
        
        if not transactions:
            print(f"No {trans_type} transactions found!")
            return
        
        self.display_transactions(transactions)
        print(f"\nTotal {trans_type} transactions: {len(transactions)}")
    
    def view_recent_records(self):
        """Display recent records."""
        try:
            count = int(input("Number of recent records to view: "))
            transactions = self.record_keeper.get_recent_transactions(count)
            
            if not transactions:
                print("No transactions found!")
                return
            
            print(f"\nShowing last {len(transactions)} record(s):")
            self.display_transactions(transactions)
        except ValueError:
            print("Please enter a valid number.")
    
    def view_all_history(self):
        """Display all transaction history."""
        if not self.record_keeper.transactions:
            print("No transactions found!")
            return
        
        print("\nAll Transaction History:")
        self.display_transactions(self.record_keeper.transactions)
    
    def view_specific_item(self):
        """Display transactions for a specific item."""
        item = input("Enter item name: ").strip()
        transactions = self.record_keeper.get_transactions_by_item(item)
        
        if not transactions:
            print(f"No transactions found for '{item}'!")
            return
        
        print(f"\nTransactions for '{item.capitalize()}':")
        self.display_transactions(transactions)
        
        total_quantity = sum(t.amount for t in transactions)
        print(f"\nTotal quantity: {total_quantity}")
    
    def view_specific_person(self):
        """Display transactions for a specific person."""
        person = input("Enter person name: ").strip()
        transactions = self.record_keeper.get_transactions_by_person(person)
        
        if not transactions:
            print(f"No transactions found for '{person}'!")
            return
        
        print(f"\nTransactions for '{person.capitalize()}':")
        self.display_transactions(transactions)
    
    def advanced_search(self):
        """Advanced search functionality."""
        print("\nAdvanced Search")
        print("Enter: <transaction_type> <search_type> <search_term>")
        print("Example: 'incoming person john' or 'outgoing item pencil'")
        
        try:
            search_input = input("Search: ").strip().split()
            if len(search_input) != 3:
                print("Please enter exactly 3 terms.")
                return
            
            trans_type, search_type, search_term = search_input
            
            # Get transactions by type first
            transactions = self.record_keeper.get_transactions_by_type(trans_type)
            
            # Filter by search type and term
            if search_type.lower() in ['person', 'client']:
                results = [t for t in transactions if t.name.lower() == search_term.lower()]
            elif search_type.lower() == 'item':
                results = [t for t in transactions if t.item.lower() == search_term.lower()]
            else:
                print("Search type must be 'person' or 'item'")
                return
            
            if not results:
                print(f"No {trans_type} transactions found for {search_type} '{search_term}'")
                return
            
            print(f"\n{trans_type.capitalize()} transactions for {search_type} '{search_term.capitalize()}':")
            self.display_transactions(results)
            
        except Exception as e:
            print(f"Search error: {e}")
    
    def display_transactions(self, transactions: List[Transaction]):
        """Display a list of transactions in a formatted table."""
        print(f"\n{'No.':<4}{'Name':<15}{'Item':<15}{'Amount':<10}{'Type':<12}{'Date':<20}")
        print("-" * 80)
        
        for i, transaction in enumerate(transactions, 1):
            date_str = transaction.timestamp.split('T')[0] if transaction.timestamp else "N/A"
            print(f"{i:<4}{transaction.name:<15}{transaction.item:<15}{transaction.amount:<10}{transaction.transaction_type:<12}{date_str:<20}")
    
    def edit_menu(self):
        """Display edit menu and handle modifications."""
        if not self.record_keeper.transactions:
            print("No records to edit!")
            return
        
        self.display_section_header("EDIT RECORDS")
        
        # Display all transactions with indices
        print("Current Records:")
        self.display_transactions(self.record_keeper.transactions)
        
        print("\nEdit Options:")
        print("1. Edit Name")
        print("2. Edit Item")
        print("3. Edit Amount")
        print("4. Edit Transaction Type")
        print("5. Delete Record")
        print("6. Return to Main Menu")
        
        try:
            choice = input("\nYour choice: ").strip()
            
            if choice in ['6', 'main']:
                return
            
            record_num = int(input("Record number to edit: ")) - 1
            
            if record_num < 0 or record_num >= len(self.record_keeper.transactions):
                print("Invalid record number!")
                return
            
            transaction = self.record_keeper.transactions[record_num]
            print(f"\nEditing: {transaction.name} | {transaction.item} | {transaction.amount} | {transaction.transaction_type}")
            
            if choice in ['1', 'name']:
                new_value = input(f"Current name: {transaction.name}. New name: ")
                self.record_keeper.update_transaction(record_num, "name", new_value)
                print("Name updated successfully!")
            
            elif choice in ['2', 'item']:
                new_value = input(f"Current item: {transaction.item}. New item: ")
                self.record_keeper.update_transaction(record_num, "item", new_value)
                print("Item updated successfully!")
            
            elif choice in ['3', 'amount']:
                new_value = input(f"Current amount: {transaction.amount}. New amount: ")
                self.record_keeper.update_transaction(record_num, "amount", new_value)
                print("Amount updated successfully!")
            
            elif choice in ['4', 'type']:
                new_value = input(f"Current type: {transaction.transaction_type}. New type (Incoming/Outgoing): ")
                if new_value.lower() in ['incoming', 'outgoing']:
                    self.record_keeper.update_transaction(record_num, "transaction_type", new_value)
                    print("Transaction type updated successfully!")
                else:
                    print("Invalid transaction type!")
            
            elif choice in ['5', 'delete']:
                confirm = input("Are you sure you want to delete this record? (yes/no): ")
                if confirm.lower() in ['yes', 'y']:
                    self.record_keeper.delete_transaction(record_num)
                    print("Record deleted successfully!")
                else:
                    print("Deletion cancelled.")
            
            else:
                print("Invalid choice!")
        
        except (ValueError, IndexError):
            print("Please enter valid numbers.")
        except Exception as e:
            print(f"Error: {e}")
    
    @staticmethod
    def show_help():
        """Display help information."""
        print("\n" + "=" * 60)
        print("                    HELP SECTION")
        print("=" * 60)
        
        print("\n1. ABOUT THE PROGRAM:")
        print("   This program helps track quantities of items and transactions.")
        print("   It supports adding, viewing, editing, and deleting records.")
        
        print("\n2. INPUT GUIDELINES:")
        print("   • Inputs are case-insensitive")
        print("   • You can use numbers or keywords (e.g., '1' or 'add')")
        print("   • Item names ending in 's' are automatically converted to singular")
        
        print("\n3. TRANSACTION TYPES:")
        print("   • Incoming: Items received/added to inventory")
        print("   • Outgoing: Items sent/removed from inventory")
        
        print("\n4. DATA STORAGE:")
        print("   • All data is automatically saved to a JSON file")
        print("   • Data persists between program sessions")
        
        print("\n5. EDITING RECORDS:")
        print("   • You can modify any field of existing records")
        print("   • Deleted records cannot be recovered")
        
        print("\n" + "=" * 60)


class Application:
    """Main application controller."""
    
    def __init__(self):
        self.record_keeper = RecordKeeper()
        self.ui = UserInterface(self.record_keeper)
    
    def run(self):
        """Run the main application loop."""
        self.ui.display_header()
        
        while True:
            try:
                choice = self.ui.display_main_menu()
                
                if choice in ['1', 'add']:
                    self.ui.add_records_interface()
                
                elif choice in ['2', 'view', 'vw']:
                    self.ui.view_menu()
                
                elif choice in ['3', 'edit', 'mod']:
                    self.ui.edit_menu()
                
                elif choice in ['4', 'help', 'hp']:
                    self.ui.show_help()
                
                elif choice in ['5', 'quit', 'exit', 'qt']:
                    print("\nThank you for using the Record Keeper!")
                    sys.exit(0)
                
                else:
                    print("Invalid choice! Please try again.")
                
            except KeyboardInterrupt:
                print("\n\nProgram interrupted by user.")
                sys.exit(0)
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    app = Application()
    app.run()