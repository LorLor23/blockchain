import datetime  # Used to record timestamps for block creation
import hashlib   # Used for generating SHA-256 hashes
import json      # Used to format transaction data into JSON

class Block:
    def __init__(self, previous_hash, transactions, nonce=0):

        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Store block creation time
        self.previous_hash = previous_hash  # Store the hash of the previous block for blockchain linking
        self.transactions = transactions  # Store transaction details
        self.nonce = nonce  # Starts as 0 but changes during mining
        self.hash = self.calculate_hash()  # Generate the block hash

    def calculate_hash(self):
        """
        Generate the SHA-256 hash of the block's contents.
        """
        block_content = json.dumps(self.transactions, sort_keys=True) + self.previous_hash + self.timestamp + str(self.nonce)
        return hashlib.sha256(block_content.encode()).hexdigest()  # Convert to SHA-256 hash

    def mine_block(self, difficulty):
        while not self.hash.startswith("0" * difficulty):  # Adjust nonce until hash starts with required zeros
            self.nonce += 1  # Increment nonce value
            self.hash = self.calculate_hash()  # Recalculate hash
        print(f"Block mined: {self.hash}")  # Print the mined block's hash


class Blockchain:
    def __init__(self, difficulty=3):
        self.chain = [self.create_genesis_block()]  # Initialize the blockchain with the genesis block
        self.difficulty = difficulty  # Set mining difficulty
        self.pending_transactions = []  # List of pending transactions to be mined
        self.accounts = {"Bank": 1000000}  # Dictionary to store account balances, initialized with the Bank's balance

    def create_genesis_block(self):
        return Block("0", [{"sender": "Bank", "receiver": "Genesis", "amount": 0}])

    def get_latest_block(self):
        return self.chain[-1]

    def create_transaction(self, sender, receiver, amount):
        """
        Create a new transaction and add it to the list of pending transactions.
        """
        # Check if sender has sufficient funds
        if sender != "Bank" and sender not in self.accounts:
            print(f"Transaction failed: {sender} does not have an account.")
            return False

        if sender != "Bank" and self.accounts[sender] < amount:
            print(f"Transaction failed: {sender} has insufficient funds.")
            return False

        # Add transaction to the pending transactions list
        self.pending_transactions.append({"sender": sender, "receiver": receiver, "amount": amount})
        print(f"Transaction added: {sender} -> {receiver}: ${amount}")
        return True

    def mine_pending_transactions(self):
        """
        Mine a new block with all pending transactions and add it to the blockchain.
        The transactions are then processed, updating account balances.
        """
        if not self.pending_transactions:  # If no pending transactions, exit
            print("No transactions to mine.")
            return

        # Create a new block containing the pending transactions
        new_block = Block(self.get_latest_block().hash, self.pending_transactions)
        new_block.mine_block(self.difficulty)  # Mine the block

        # Process transactions after mining
        for tx in self.pending_transactions:
            sender, receiver, amount = tx["sender"], tx["receiver"], tx["amount"]

            # Deduct funds from sender and credit receiver
            if sender != "Bank":
                self.accounts[sender] -= amount
            if receiver not in self.accounts:
                self.accounts[receiver] = 0
            self.accounts[receiver] += amount

        self.chain.append(new_block)  # Append the new block to the blockchain
        self.pending_transactions = []  # Reset pending transactions

    def is_chain_valid(self):
        """
        Check the integrity of the blockchain by verifying the hashes of all blocks.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Validate if the stored hash matches the recalculated hash
            if current_block.hash != current_block.calculate_hash():
                return False

            # Validate if the previous block hash matches the one stored in the current block
            if current_block.previous_hash != previous_block.hash:
                return False

        return True  # If all checks pass, the chain is valid

    def get_balance(self, account):
        """
        Get the current balance of an account.
        """
        return self.accounts.get(account, 0)

    def print_chain(self):
        """
        Print all blocks in the blockchain, displaying transaction details and metadata.
        """
        for block in self.chain:
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Transactions: {block.transactions}")
            print(f"Nonce: {block.nonce}")
            print(f"Timestamp: {block.timestamp}")
            print("-" * 30)


# testing the blockchain

bank_chain = Blockchain()

# Creating and adding transactions
bank_chain.create_transaction("Bank", "Ann", 5000)
bank_chain.create_transaction("Ann", "Ben", 1200)
bank_chain.create_transaction("Emma", "John", 1500)
bank_chain.create_transaction("Bob", "David", 800)

# Mining a block to add the transactions to the blockchain
bank_chain.mine_pending_transactions()

# Creating more transactions and mining another block
bank_chain.create_transaction("Charlie", "Emma", 700)
bank_chain.create_transaction("Emma", "David", 300)
bank_chain.mine_pending_transactions()

# Displaying account balances after transactions
print("\nBalances:")
for account in bank_chain.accounts:
    print(f"{account}: ${bank_chain.get_balance(account)}")

# Verifying blockchain integrity
print(f"\nBlockchain is valid: {bank_chain.is_chain_valid()}")

# Displaying the full blockchain
print("\nBlockchain Data:")
bank_chain.print_chain()
