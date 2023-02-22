from pathlib import Path
from dotenv import load_dotenv
from os import environ


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
text_logs = Path('.') / 'logs.txt'

class Settings:
    RUTA_MONGO = environ.get('RUTA_MONGO')
    SECRET_KEY = environ.get('SECRET_KEY')
    ALGORITHM = environ.get('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = 11500
    REFRESH_TOKEN_EXPIRE_MINUTES = 10
    DOCS = environ.get('DOCS')
    REDOCS = environ.get('REDOCS')
    URL_WEB = environ.get('URL_WEB')
    LOGS = text_logs
    TITLE = "Little Ecommerce"
    VERSION = "1.0.0.1"
    CONTACT = {
                    "name": "Diego Luque - Backend Developer",
                    "url": "https://www.diego-luque.com",
                    "email": "ds.diegoluque@gmail.com",
    }
    DESCRIPTION = """
    API E-commerce 😀
    Little project E-commerce.
# Route
    - https://api-products.diego-luque.com/
    
# Permissions

## Free
    username:tanjiro
    password:tanjiro

    Actions:
        - Get Products Free 5 calls per Minute
        - Get Product One Product 5 calls per Minute
        - Get Products Pagination 

    Products
        - cost ❌
        - stock❌
        - sale 
        - code
        - description
        - name
        - brand
        - images
    
## Premium
    username:cabo
    password:cabo

    Actions:
        - Get Products Premium 5 calls per 30 seconds
        - Get One Product 5 calls per Minute
        - Add New Product 5 calls per Hour
        - Patch Product 3 calls per Hour

    Products
        - cost ❌
        - stock
        - sale
        - code
        - description
        - name
        - brand
        - images

## Admin
    username:jurassic
    password:jurassic

    Actions:
        - Add New Product 3 calls per Hour
        - Get Products 3 calls per Hour
        - Get One Product 5 calls per Minute
        - Add New User 1 calls per 15 seconds
        - Patch Product 3 calls per Hour
        - Delete Product 3 calls per Hour

    Products
        - cost ✅
        - stock✅
        - sale 
        - code
        - description
        - name
        - brand
        - images
    """
    DESCRIPTION_ROUTE = """
   # Authentication is Required
    Admin               Premium           Free
    username:jurassic | username:cabo   | username:tanjiro
    password:jurassic | password:cabo   | password:tanjiro
"""
    
    #Data Email
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_FROM = environ.get('MAIL_FROM')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_STARTTLS = environ.get('MAIL_STARTTLS')
    MAIL_SSL_TLS = environ.get('MAIL_SSL_TLS')
    USE_CREDENTIALS = environ.get('USE_CREDENTIALS')
    VALIDATE_CERTS = environ.get('VALIDATE_CERTS')

settings = Settings()
