import pdfkit
from flask import Response

@app.route('/purchase-order/<int:order_id>/pdf')
def download_purchase_order_pdf(order_id):
    # same order generation as before...
    html = render_template('purchase_order.html', order=order)

    pdf = pdfkit.from_string(html, False)
    response = Response(pdf, mimetype='application/pdf')
    response.headers['Content-Disposition'] = f'attachment; filename=purchase_order_{order_id}.pdf'
    return response