


from flask import Flask

app = Flask(__name__)

# Define Shipping class

# Define Payment class

# Define Item class

# Define Order class
# An order is expected to have:
# one or many items, shipping information, payment information

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/order', methods=['POST'])
def place_order():
    return 'Order'





if __name__ == '__main__':
    app.run()
