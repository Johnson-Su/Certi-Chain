# Certi-Chain
**Blockchain based authentication for luxury/artisan goods using python**


![](https://github.com/Johnson-Su/Certi-Chain/blob/main/certi-chain.gif)

**Certi-Chain** allows companies to combat counterfeiting and reduce the number of fakes on the market. It uses the immutability proporty of blockchains to prevent records of existing products being tampered. **Certi-Chain** is cheap and easy to implement in every product, just stick a certified NFC tag onto any product to ensure that one is real! See it live [here!](https://certi-chain-hw.herokuapp.com)

*There are 2 ways to try Certi-Chain*
  - Easily add items to the blockchain or check if an item exists using the Cert-Chain website
  - Run the python client onto your local machine for a more polished experience, and try adding multiple nodes!
  
 
# Try the program using the Certi-Chain webite
* Go to the [Certi-Chain Website](https://certi-chain-hw.herokuapp.com) and fill out the fields (All fields are needed!). **For now the universal account number is 1001**
* This is the product information submition page, this is where you can add information into the blockchain.
* Click 'Save Submition', this uploads your product to a list of pending products.
* Scroll down and keep track of the **Product ID** (ex. `1b1t`), you will need it to verify that your product is in the blockchain!
* Once you click 'Finalize Submition' you will submit all pending transactions into a Block. This block is then verified and added onto the chain.
* To verify your product has been added go to https://certi-chain-hw.herokuapp.com/check?id=PRODUCT_ID where PRODUCT_ID is the product ID you saver earlier.
* You will be able to see that your product is indeed in the chain!
* Want to see what's in the chain? Go to https://certi-chain-hw.herokuapp.com/chain to check it out!

# Try the program on your local machine. 
* Pull the [LocalBlockChain](https://github.com/Johnson-Su/Certi-Chain/tree/main/LocalBlockChain) from the repo
* Make sure you have Python 3.6 and the required dependancies:
  * Flask
  * requests
* Navigate to the LocalBlockChain directory on your machine
* Start up the first node by typing the following in the terminal/cmd:
  * **Windows Users (cmd)**: \
  `set FLASK_APP=Node_Server.py`
  `flask run --port 8000`
  * **Linux (terminal)**: \
  `export FLASK_APP=Node_Server.py`
  `flask run --port 8000`
* Then open up a *second* terminal/cmd and navigate to the same folder.
* Run the file run_app.py by entering `python run_app.py`
* Now if you navigate on your browser to http://localhost:5000/ you should see an information submition page.
* You can submit information according to instructions above for the website.
* You can check what the blockchain looks like by going to http://localhost:8000/chain

## Add New Nodes!
* Once you have 2 terminals up and running from the instuctions above its time to add a new node.
  * *What is a node?* In this case a node just represents another computer. A blockchain is decentralized, so multiple computers are used to keep this database running. Each node needs to sync up with one another to keep up to date!
* Open a *third* terminal and navigate to the same directory.
* Start up another node by typing the following in the terminal/cmd:
  * **Windows Users (cmd)**:
  `set FLASK_APP=Node_Server.py`
  `flask run --port 8001`
  * **Linux (terminal)**
  `export FLASK_APP=Node_Server.py`
  `flask run --port 8001`
* The only difference is the port, which does not have to be 8001 but we use 8001, 8002, 8003, etc. just for simplicity.
* Now that a new node is running we must sync it up with the other nodes.
* Open up the terminal and type the following *(Windows users should use the bash shell as it does not work on cmd)*
* Type the following: \
`curl -X POST \
  http://127.0.0.1:8001/register_with \
  -H 'Content-Type: application/json' \
  -d '{"node_address": "http://127.0.0.1:8000"}'`
* Replace `8001` before the `/register_with` to the port you specified when starting up the node (ex. 8002, 8003 if you are starting up multple nodes).
* This allows the new node to sync up with the other nodes.
* Now if you add a new product to the chain and see that it updates at http://localhost:8000/chain, it should also update at http://localhost:8001/chain!
