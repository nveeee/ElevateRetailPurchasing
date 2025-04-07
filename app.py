from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/order-success')
def order_success():
    return render_template('order_success.html')

# Example: After placing an order
@app.route('/place-order', methods=['POST'])
def place_order():
    # Your order logic here...
    return redirect(url_for('order_success'))

# Home route for "/"
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
