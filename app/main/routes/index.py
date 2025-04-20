#import os
#from ...api.util import get_products
#from ...main import bp
#from flask import render_template


#@bp.route('/')
#def index():
    #products = get_products(limit=10)

    #return render_template('index.html', active_page='home', products=products, env=os.getenv('FLASK_ENV'))
import os
from app.api.util import get_products  # Absolute import
from app.main import bp  # Absolute import
from flask import render_template


@bp.route('/')
def index():
    products = get_products(limit=10)

    return render_template('index.html', active_page='home', products=products, env=os.getenv('FLASK_ENV'))
