from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields import FieldList, HiddenField

class POForm(FlaskForm):
    selected_products = FieldList(HiddenField(), min_entries=0)
    submit = SubmitField('Order Selected Products')
