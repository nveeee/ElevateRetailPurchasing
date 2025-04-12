from flask_wtf import FlaskForm
from wtforms import FormField, FieldList, IntegerField, HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class SingleOrderForm(FlaskForm):
    product_id = HiddenField(validators=[DataRequired()])
    unit_price = StringField(render_kw={"readonly": True})
    quantity = IntegerField(validators=[DataRequired(), NumberRange(min=1)])

class BulkOrderForm(FlaskForm):
    orders = FieldList(FormField(SingleOrderForm), min_entries=0)
    submit = SubmitField('Submit All Orders')
