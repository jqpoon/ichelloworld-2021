from flask_table import Table, Col

class Results(Table):
    id = Col('Id', show=False)
    product = Col('Product')
    price = Col('Price')
    supermarket = Col('Supermarket')
    link = Col('Link')