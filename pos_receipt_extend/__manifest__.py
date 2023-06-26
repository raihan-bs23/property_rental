{
    'name': "POS Receipt",
    'summary': """
        This module will add an order name into the invoice while creating the invoice from Point of Sale 
        """,

    'description': """
         POS Receipt is a module which performs adding additional fields to the POS order invoice while creating it. 
    """,

    "category": "Point of Sale",
    "version": "16.0",
    'author': "Brain Station 23 Ltd",
    'license': 'LGPL-3',
    'website': "http://www.brainstation-23.com",
    'depends': ['point_of_sale', 'sale', ],
    'data': [
        'views/POSConfig.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_receipt_extend/static/src/xml/OrderReceipt.xml',
            'pos_receipt_extend/static/src/js/payment.js',

        ]
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
