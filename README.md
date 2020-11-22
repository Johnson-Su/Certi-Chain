# Certi-Chain
Blockchain based authentication for luxury/artisan goods using python

![](https://github.com/Johnson-Su/Certi-Chain/blob/main/certi-chain.gif)

*There are 2 ways to try Certi-Chain*
  - Easily add items to the blockchain or check if an item exists using the Cert-Chain website
  - Run the python client onto your local machine for a more polished experience, and try adding multiple nodes!
  
 
# Try the program using the Cert-Chain webite
* Go to the [Certi-Chain Website](https://certi-chain-hw.herokuapp.com) and fill out the fields (All fields are needed!). **For now the universal account number is 1001**
* This is the product information submition page, this is where you can add information into the blockchain.
* Click 'Save Submition', this uploads your product to a list of pending products.
* Scroll down and keep track of the **Product ID** (ex. `1b1t`), you will need it to verify that your product is in the blockchain!
* Once you click 'Finalize Submition' you will submit all pending transactions into a Block. This block is then verified and added onto the chain.
* To verify your product has been added go to https://certi-chain-hw.herokuapp.com/check?id=PRODUCT_ID where PRODUCT_ID is the product ID you saver earlier.
* You will be able to see that your product is indeed in the chain!
* Want to see what's in the chain? Go to https://certi-chain-hw.herokuapp.com/chain to check it out!

# Try the program on your local machine. Add new nodes at will!
* Pull the [LocalBlockChain](https://github.com/Johnson-Su/Certi-Chain/tree/main/LocalBlockChain) from the repo
* Make sure you have Python 3.6 and the required dependancies:
  * Flask
  * requests
* Navigate to the LocalBlockChain directory on your machine
* Start up the first node by typing the following in the terminal/cmd:
  * **Windows Users (cmd)**:
  `set FLASK_APP=Node_Server.py`
  `flask run --port 8000`
  * **Linux (terminal)**
  `export FLASK_APP=Node_Server.py`
  `flask run --port 8000`
* Then open up a *second* terminal/cmd and navigate to the same folder.
* Run the file run_app.py by entering `python run_app.py`
* Now if you navigate on your browser to http://localhost:5000/ you should see an information submition page.
* You can submit information according to instructions above for the website.

## Add New Nodes!
* Once 

