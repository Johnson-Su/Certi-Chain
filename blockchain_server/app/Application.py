import datetime, json, requests

from flask import render_template, redirect, request

from auth import Authenification as auth
from app import app

# Node in the blockchain network that our application will communicate with
# to fetch and add data.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

user_key = auth.read_public_key('app\\user_key\\public_pem.pem')

posts = []
item_info = {}
errors = []
t_id = ""

def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data, and store it locally.
    """
    get_chain_address = f"{CONNECTED_NODE_ADDRESS}/chain"
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content,
                       key=lambda k: k['timestamp'],
                       reverse=True)

def grab_errors():
    global errors
    err_list = errors
    errors = []
    return err_list

def fetch_item_info():
    """
    Fetch the info for the last item requested.
    """
    output_address = f'{CONNECTED_NODE_ADDRESS}/checkout'
    response = requests.get(output_address)

    if response.status_code == 200:
        global item_info
        product = json.loads(response.content)
        item_info = product

@app.route('/start_mine', methods=['POST'])
def start_mine():
    """
    Begin the mining process.
    """
    output_address = f'{CONNECTED_NODE_ADDRESS}/mine'
    requests.get(output_address)

    return redirect('/')

@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application
    """

    global errors

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

    # Submit a transaction
    new_tx_address = f"{CONNECTED_NODE_ADDRESS}/new_transaction"

    tx_request = requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    if tx_request.status_code == 404:
        errors = ["missing_args"]
    elif tx_request.status_code == 405:
        errors = ["invalid_user"]
    else:
        errors = ["none"]

    # Return to the homepage
    return redirect('/')

@app.route('/check', methods=['POST'])
def submit_check():
    """
    Endpoint to submit a tx id to get the info for.
    """
    tx_id = request.form["tx_id"]

    post_object = {
        'tx_id': tx_id
    }

    tocheck_address = f"{CONNECTED_NODE_ADDRESS}/check"

    requests.post(tocheck_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})
    
    # Go to the page with the results if the search
    return redirect('/resultpage')

@app.route('/resultpage')
def result():
    """
    The page for the result of the search.
    """

    tx_id = request.args.get('t')

    post_object = {
        'tx_id': tx_id
    }

    tocheck_address = f"{CONNECTED_NODE_ADDRESS}/check"

    requests.post(tocheck_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})
    fetch_item_info()
    return render_template('result.html',
                           title='Results of item check',
                           product_info=item_info,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string,
                           t_id = t_id
                           )

@app.route('/')
def index():
    """
    The page to add product information to the chain.
    """
    fetch_posts()
    pending_tx_address = f'{CONNECTED_NODE_ADDRESS}/pending_tx'
    pending_tx = requests.get(pending_tx_address)
    return render_template('companyside.html',
                           title='Company Data Submit Page',
                           posts=posts,
                           pending=json.loads(pending_tx.content),
                           errors=grab_errors(),
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)
                           
def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')

@app.route('/validate')
def validate():
    """
    The page to validate the product.
    """
    fetch_posts()
    return render_template('validate.html',
                           title='Customer Check Page',
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)
                           
def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')


    