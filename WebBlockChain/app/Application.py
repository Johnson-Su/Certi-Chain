import datetime, json, requests, time, re
import Blockchain, Block

from flask import render_template, redirect, request, Flask

app = Flask(__name__)

# Node in the blockchain network that our application will communicate with
# to fetch and add data.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:5000"

WAIT_TIME = 1

# List of errors
errors = []

# init blockchain
blockchain = Blockchain.Blockchain()
blockchain.create_genesis_block()

# The last thing requested
tx_search = None

# List of accepted accounts
accounts = ["1001"]

# Number of transactions in the current block to be
tx_number = 1

# Set of adresses of peers within the network
peers = set()

def grab_errors():
    global errors
    err_list = errors
    errors = []
    return err_list

@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application
    """

    global errors
    global tx_number

    name = request.form["name"]
    year = request.form["year"]
    brand = request.form["brand"]
    post_desc = request.form["description"]
    materials = request.form["materials"]
    location = request.form["location"]
    journey = request.form["journey"]
    key = request.form["key"]

    post_object = {
        'name': name,
        'brand': brand,
        'year': year,
        'description': post_desc,
        'materials': materials,
        'location': location,
        'journey': journey,
        'key': key
    }

    # Get the tx data
    tx_data = post_object

    # Required information
    required_fields = ["name", "description", "materials", "location",
                       "brand", "year", "journey", "key"]

    for field in required_fields:
        # If informtaion is missing, do not add this transaction
        if (not tx_data.get(field)):
            errors = ["missing_args"]

    if (not tx_data["key"] in accounts):
        errors = ["invalid_user"]
    else:
        errors = ["none"]
    
    # Time tx was made
    tx_data["timestamp"] = time.time()
    # Block tx will belong to
    tx_data["block_num"] = blockchain.last_block.index + 1
    # the number the tx has within the block
    tx_data["tx_num"] = tx_number
    # increment tx number
    tx_number += 1
    
    blockchain.add_transaction(tx_data)

    # Return to the homepage
    time.sleep(WAIT_TIME)
    return redirect('/')

@app.route('/resultpage')
def result():
    """
    The page for the result of the search.
    """
    return render_template('result.html',
                           title='Results of item check',
                           product_info=tx_search,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string
                           )

@app.route('/')
def index():
    """
    The page to add product information to the chain.
    """
    return render_template('companyside.html',
                           title='Company Data Submit Page',
                           pending=blockchain.unconfirmed_transactions,
                           errors=grab_errors(),
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)
                           
def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')

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

@app.route('/pending_tx', methods=["GET"])
def get_pending_tx():
    """
    The end point for the number of pending transactions.
    """
    return json.dumps(blockchain.unconfirmed_transactions)

@app.route('/check', methods=['GET'])
def add_check():
    """
    Check if the given transaction id is in the blockchain. Set the /check 
    endpoint to have the information of the given transaction id, if it exists.
    Leave an error if there does not exists a tx with the given id, or if the 
    id is not in the correct format. 
    """
    global tx_search

    # Get the tx id
    #tx_data = request.get_json()
    tx_data = {"tx_id": request.args.get('id')}
    
    # If there is no id
    if (not tx_data.get("tx_id")):
        tx_search = {"error": "inv_tx_id"}
        time.sleep(WAIT_TIME)
        return redirect('/resultpage')


    # If the id is not in the correct format
    tx_id = tx_data["tx_id"]
    if not re.match("[0-9]+b[0-9]+t", tx_id):
        tx_search = {"error": "inv_tx_id"}
        time.sleep(WAIT_TIME)
        return redirect('/resultpage')


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
                    time.sleep(WAIT_TIME)
                    return redirect('/resultpage')


    # There does not exists a transaction with the given id
    tx_search = {"error": "no_tx"}
    time.sleep(WAIT_TIME)
    return redirect('/resultpage')


@app.route('/checkout', methods=['GET'])
def output_validity():
    """
    The endpoint for the needed product info.
    """
    return json.dumps(tx_search)

@app.route('/start_mine', methods=['POST'])
def mine_unconfirmed_transactions():
    """
    Mine all pending transactions and announce to all nodes there is a new 
    block.
    """
    blockchain.mine()
    global tx_number
    tx_number = 1
    time.sleep(WAIT_TIME)
    return redirect('/')
