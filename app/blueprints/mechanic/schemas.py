from app.extensions import ma
from app.models import Mechanic

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        include_fk = True
    
    email = ma.Email(required=True)
    specialization = ma.Str(required=True)
    name = ma.Str(required=True)
    experience = ma.Int(required=True)

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)