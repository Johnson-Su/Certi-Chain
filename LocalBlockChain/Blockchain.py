import Block as bl
import time

class Blockchain:

    DIFFICULTY = 4

    def __init__(self):
        self.chain = []
        self.unconfirmed_transactions = [] # data not yet validated
    
    def create_genesis_block(self):
        genesis_block = bl.Block(0, [], 0, "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        """
        The last block in the chain, ie. the most recent block added
        """
        return self.chain[-1]

    @staticmethod
    def proof_of_work(block):
        """
        A proof of work is the process of adding a constraint to a block's
        hash. By adding the constraint, it makes it difficult for a valid 
        hash to be computed.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while (not computed_hash.startswith('0' * Blockchain.DIFFICULTY)):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash
    
    def add_block(self, block, proof):
        """
        To add a block into the blockchain, we must determine if the block 
        to be added is in the correct chronological order (no adding 
        transactions that occured before the last block), 
        and we must determine if the data has not been tampered with.  
        """
        previous_hash = self.last_block.hash

        # is the block in the right chronological order?
        if (previous_hash != block.previous_hash):
            return False
        
        # has the block been tampered with 
        if (not Blockchain.is_valid_proof(block, proof)):
            return False

        # if the above constraints are satisfied, add the block
        block.hash = proof
        self.chain.append(block)
        return True
    
    @classmethod
    def is_valid_proof(self, block, block_hash):
        # does the hash satisfy the contraints?
        # does the hash of the block match the proof provided?
        return (block_hash.startswith('0' * Blockchain.DIFFICULTY) and
                block_hash == block.compute_hash())
    
    def add_transaction(self, transaction):
        # Add a transaction to the list
        self.unconfirmed_transactions.append(transaction)
    
    def mine(self):

        # is the list of unconfirmed transactions empty?
        if (not self.unconfirmed_transactions):
            return False

        # get the last block to determine the index and previous_hash of 
        # the new block
        last_block = self.last_block

        new_block = bl.Block(last_block.index + 1,
                          self.unconfirmed_transactions,
                          time.time(),
                          last_block.hash)
        
        # do work to find a valid hash
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        # reset the transactions
        self.unconfirmed_transactions = []
        return True
    
    @classmethod
    def check_chain_validity(cls, chain):
        
        result = True
        previous_hash = "0"

        # Iterate through every block
        for block in chain:
            block_hash = block.hash
            # remove the hash field in order to compute it again
            delattr(block, "hash")

            if not cls.is_valid_proof(block, block.hash) or \
                    previous_hash != block.previous_hash:
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash

        return result




