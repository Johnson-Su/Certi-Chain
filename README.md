# Certi-Chain
Blockchain based authentication for luxury/artisan goods using python

![](https://github.com/Johnson-Su/Certi-Chain/blob/main/certi-chain.gif)

*There are 2 ways to try Certi-Chain*
  - Easily add items to the blockchain or check if an item exists using the Cert-Chain website
  - Run the python client onto your local machine for a more polished experience, and try adding multiple nodes!
  
 
# Try the program using the Cert-Chain webite
Go to the [Certi-Chain Website](https://certi-chain-hw.herokuapp.com) and fill out the fields (All fields are needed!). 

**For now the universal account number is 1001**

This is the product information submition page, this is where you can add information into the blockchain.

Click 'Save Submition', this uploads your product to a list of pending products.
Scroll down and keep track of the **Product ID**, you will need it to verify that your product is in the blockchain!
Once you click 'Finalize Submition' you will submit all pending transactions into a Block. This block is then verified and added onto the chain.
To verify your product has been added go to https://certi-chain-hw.herokuapp.com/check?id=PRODUCT_ID where PRODUCT_ID is the product ID you saver earlier.
You will be able to see that your product is indeed in the chain!
Want to see whats in the chain? Go to https://certi-chain-hw.herokuapp.com/chain to check it out!

