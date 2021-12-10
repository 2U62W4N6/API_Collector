import enum

class API_Version(enum.Enum):
    OLD =  'v1/'
    CURRENT = 'v1_3/'

class API_Endpoint(enum.Enum):
    PRODUCTS = 'products'
    ORDERS = 'orders'
    PACKAGES = 'packages'

