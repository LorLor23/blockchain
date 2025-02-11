# blockchain
Detyre Kursi

This project is a blockchain-based banking system built with Python, enabling users to conduct secure transactions through blockchain technology. 
The implementation includes core functionalities such as block creation, transaction management, mining, and integrity verification of the blockchain.

The system includes:
- **Block creation** with unique cryptographic hashes.
- **Mining using Proof of Work (PoW)** for security.
- **Transaction verification** and balance updates.
- **Blockchain integrity validation** to ensure data consistency.


## Libraries Used
This project relies only on built-in Python libraries:
- `datetime` → Handles timestamps for block creation.
- `hashlib` → Generates SHA-256 hashes for security.
- `json` → Formats transaction data for consistency.

 How the Blockchain Works
1.	Creating a Transaction
Users can send money between accounts. The system checks if the sender has sufficient funds before adding the transaction.
2.	Mining Blocks
Transactions are grouped and mined using Proof of Work (PoW). Mining ensures security by requiring computational work.
3.	Validating the Blockchain
After each transaction, the blockchain verifies its integrity by checking if all hashes are correct.
4.	Checking Balances
After mining, balances are updated based on the transactions stored in the blocks.

Secure transactions stored in blockchain blocks
Proof of Work mining for transaction validation
Built-in balance tracking for each account
Blockchain validation to prevent tampering

1. Block Creation & Hashing
Each block contains transactions, a timestamp, a nonce, and the previous block’s hash. The SHA-256 algorithm ensures security.

block = Block("0000abcd1234", [{"sender": "Alice", "receiver": "Bob", "amount": 100}])
print(block.hash)  # Generated block hash

3. Proof-of-Work Mining
   
Mining requires finding a valid nonce that produces a hash matching the difficulty requirement.

new_block = Block("0000abcd1234", [{"sender": "Charlie", "receiver": "David", "amount": 50}])
new_block.mine_block(3)  # Mines block with difficulty 3

3. Transaction Handling & Mining
Transactions are created and stored as pending transactions before mining.

bank_chain.create_transaction("Alice", "Bob", 500)
bank_chain.mine_pending_transactions()

4. Blockchain Validation

Checks data integrity by verifying each block’s hash and previous hash reference.
print(f"Blockchain is valid: {bank_chain.is_chain_valid()}")


