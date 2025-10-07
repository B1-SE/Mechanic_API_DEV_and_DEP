swagger_config = {
    "swagger": "2.0",
    "info": {
        "title": "Mechanic API",
        "description": "API for managing customers, mechanics, service tickets, and inventory",
        "version": "1.0.0"
    },
    "host": "https://be1-mechanic-shop-assignment.onrender.com",
    "basePath": "/",
    "schemes": ["https"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    },
    "definitions": {
        "Customer": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"},
                "dob": {"type": "string", "format": "date"}
            }
        },
        "CustomerInput": {
            "type": "object",
            "required": ["name", "email", "password"],
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "password": {"type": "string"},
                "dob": {"type": "string", "format": "date"}
            }
        },
        "Mechanic": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"},
                "specialization": {"type": "string"},
                "experience": {"type": "integer"}
            }
        },
        "MechanicInput": {
            "type": "object",
            "required": ["name", "email", "specialization", "experience"],
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "specialization": {"type": "string"},
                "experience": {"type": "integer"}
            }
        },
        "ServiceTicket": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "service_date": {"type": "string", "format": "date"},
                "customer_id": {"type": "integer"}
            }
        },
        "ServiceTicketInput": {
            "type": "object",
            "required": ["service_date", "customer_id"],
            "properties": {
                "service_date": {"type": "string", "format": "date"},
                "customer_id": {"type": "integer"}
            }
        },
        "Inventory": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "price": {"type": "number"}
            }
        },
        "InventoryInput": {
            "type": "object",
            "required": ["name", "price"],
            "properties": {
                "name": {"type": "string"},
                "price": {"type": "number"}
            }
        },
        "LoginInput": {
            "type": "object",
            "required": ["email", "password"],
            "properties": {
                "email": {"type": "string"},
                "password": {"type": "string"}
            }
        },
        "Error": {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        }
    }
}