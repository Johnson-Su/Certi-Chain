from hashlib import sha256
import json

class Block:

    def __init__(self, index, transactions, timestamp, previous_hash, nonce = 0):
        """
        Constructor for the 'Block' class, initialize class variables
        
        Args:
            index: Unique block ID
            transactions: A list of transactions
            timestamp: The time the block was generated
            previous_hash: Hash of the previous block in the blockchain
        """
        
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys = True)
        return sha256(block_string.encode()).hexdigest()

    