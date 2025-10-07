from app.extensions import ma
from app.models import Customer
from marshmallow import validates, ValidationError

class CustomerSchema(ma.SQLAlchemyAutoSchema):
      class Meta:
          model = Customer
          load_instance = True
          include_fk = True

      email = ma.Email(required=True)
      password = ma.Str(load_only=True)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)