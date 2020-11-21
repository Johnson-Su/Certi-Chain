from flask import Flask, request
import requests, json, time, re
import Blockchain, Block

# init flask
app = Flask(__name__)

# init blockchain
blockchain = Blockchain.Blockchain()
blockchain.create_genesis_block()

tx_search = None

# Number of transactions in the current block to be
tx_number = 1

# Set of adresses of peers within the network
peers = set()

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    """
    Defines the endpoint to create a new transaction to add to the chain.
    Checks if a transaction has the valid information before adding it 
    to the list of transactions to add
    """

    global tx_number

    # Get the tx data
    tx_data = request.get_json()

    # Required information
    required_fields = ["name", "description", "materials", "location",
                       "brand", "year", "journey", "key"]

    for field in required_fields:
        # If informtaion is missing, do not add this transaction
        if (not tx_data.get(field)):
            return "Invalid transaction data", 404
    
    # Time tx was made
    tx_data["timestamp"] = time.time()
    # Block tx will belong to
    tx_data["block_num"] = blockchain.last_block.index + 1
    # the number the tx has within the block
    tx_data["tx_num"] = tx_number
    # increment tx number
    tx_number += 1
    
    blockchain.add_transaction(tx_data)
    return "Success", 201

@app.route('/chain', methods=['GET'])
def get_chain():
    """
    The end point for the data of the chain
    """

    # Data for every block in the chain
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data,
                        "peers": list(peers)})

@app.route('/pending_tx')
def get_pending_tx():
    """
    The end point for the number of pending transactions.
    """
    return json.dumps(blockchain.mine_unconfirmed_transactions)

@app.route('/check', methods=['POST'])
def add_check():
    """
    Check if the given transaction id is in the blockchain. Set the /check 
    endpoint to have the information of the given transaction id, if it exists.
    Leave an error if there does not exists a tx with the given id, or if the 
    id is not in the correct format. 
    """
    global tx_search

    # Get the tx id
    tx_data = request.get_json()
    
    # If there is no id
    if (not tx_data.get("tx_id")):
        tx_search = {"error": "inv_tx_id"}
        return "Invalid", 404

    # If the id is not in the correct format
    tx_id = tx_data["tx_id"]
    if not re.match("[0-9]+b[0-9]+t", tx_id):
        tx_search = {"error": "inv_tx_id"}
        return "Invalid", 404

    # Parse out the block number from the id
    block_num = tx_id[0:tx_id.index("b")]
    # Parse out the tx number from the id
    tx_num = tx_id[tx_id.index("b") + 1 : tx_id.index("t")]

    # Find the block with the given block number
    for block in blockchain.chain:
        if block.index == int(block_num):
            # Find the transaction
            for tx in block.transactions:
                if tx["tx_num"] == int(tx_num):
                    # Grab the relevant info
                    tx_search = tx
                    tx_search["error"] = "None"
                    return "Success", 201

    # There does not exists a transaction with the given id
    tx_search = {"error": "no_tx"}
    return "Cannot find", 400

@app.route('/checkout', methods=['GET'])
def output_validity():
    """
    The endpoint for the needed product info.
    """
    return json.dumps(tx_search)

# Now establish decentralization and concensus

# Endpoint to add new peers
@app.route('/register_node', methods=['POST'])
def register_new_peers():
    """
    Add a new peer to the list.
    """
    # The host address to the peer node 
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400

    # Add the node to the peer list
    peers.add(node_address)

    # Return the blockchain to the newly registered node so that it can sync
    return get_chain()

@app.route('/register_with', methods=['POST'])
def register_with_existing_node():
    """
    Internally calls the `register_node` endpoint to
    register current node with the remote node specified in the
    request, and sync the blockchain as well with the remote node.
    """
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400

    data = {"node_address": request.host_url}
    headers = {'Content-Type': "application/json"}

    # Make a request to register with remote node and obtain information
    response = requests.post(node_address + "/register_node",
                             data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        global blockchain
        global peers
        # update chain and the peers
        chain_dump = response.json()['chain']
        blockchain = create_chain_from_dump(chain_dump)
        peers.update(response.json()['peers'])
        return "Registration successful", 200
    else:
        # if something goes wrong, pass it on to the API response
        return response.content, response.status_code

def create_chain_from_dump(chain_dump):
    """
    Create a blockchain from the json object of a block chain. (Init a copy of 
    the parent blockchain to the node)
    """
    generated_blockchain = Blockchain.Blockchain()
    generated_blockchain.create_genesis_block()
    for idx, block_data in enumerate(chain_dump):
        if idx == 0:
            continue  # skip genesis block
        block = Block.Block(block_data["index"],
                      block_data["transactions"],
                      block_data["timestamp"],
                      block_data["previous_hash"],
                      block_data["nonce"])
        proof = block_data['hash']
        added = generated_blockchain.add_block(block, proof)
        if not added:
            raise Exception("The chain dump is tampered!!")
    return generated_blockchain
    
def consensus():
    """
    Consensus algorithm. If a longer valid chain is
    found, our chain is replaced with it.
    """
    global blockchain

    longest_chain = None
    current_len = len(blockchain.chain)

    for node in peers:
        response = requests.get(f'{node}chain')
        length = response.json()['length']
        chain = response.json()['chain']
        if length > current_len and blockchain.check_chain_validity(chain):
            # Longer valid chain found!
            current_len = length
            longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True

    return False

@app.route('/add_block', methods=['POST'])
def verify_and_add_block():
    """
    Once the blockchain is updated, add the updated block and check if 
    that block is valid before updating the local chain.
    """
    block_data = request.get_json()
    block = Block.Block(block_data["index"],
                  block_data["transactions"],
                  block_data["timestamp"],
                  block_data["previous_hash"],
                  block_data["nonce"])

    proof = block_data['hash']
    added = blockchain.add_block(block, proof)

    if not added:
        return "The block was discarded by the node", 400

    return "Block added to the chain", 201


def announce_new_block(block):
    """
    Announce to the network once a block has been mined.
    Other blocks can simply verify the proof of work and add it to their
    respective chains.
    """
    for peer in peers:
        url = f"{peer}add_block"
        headers = {'Content-Type': "application/json"}
        requests.post(url,
                      data=json.dumps(block.__dict__, sort_keys=True),
                      headers=headers)

@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    """
    Mine all pending transactions and announce to all nodes there is a new 
    block.
    """
    result = blockchain.mine()
    if not result:
        return "No transactions to mine"
    else:
        # Making sure we have the longest chain before announcing to the network
        chain_length = len(blockchain.chain)
        consensus()
        if chain_length == len(blockchain.chain):
            # announce the recently mined block to the network
            announce_new_block(blockchain.last_block)
        return f"Block #{blockchain.last_block.index} is mined."