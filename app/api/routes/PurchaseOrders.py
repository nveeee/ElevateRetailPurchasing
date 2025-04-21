# New routes for products
bp.route('/products', methods=['GET'])
def list_products():
    """List all products or get product by id"""
    product_id = request.args.get('product_id')
    if product_id:
        product = Product.query.get(product_id)
        if product:
            return jsonify({
                'Product_ID': product.Product_ID,
                'Name': product.Name,
                'Description': product.Description,
                'Price': product.Price,
                'Supplier_ID': product.Supplier_ID,
                'Category_ID': product.Category_ID
            })
        else:
            return jsonify({'message': 'Product not found'}), 404
    else:
        products = Product.query.all()
        product_list = []
        for product in products:
            product_list.append({
                'Product_ID': product.Product_ID,
                'Name': product.Name,
                'Description': product.Description,
                'Price': product.Price,
                'Supplier_ID': product.Supplier_ID,
                'Category_ID': product.Category_ID
            })
        return jsonify(product_list)