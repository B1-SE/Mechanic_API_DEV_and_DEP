from app.extensions import ma
from app.models import Inventory

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True
        include_fk = True
    
    name = ma.Str(required=True)
    price = ma.Float(required=True)

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)