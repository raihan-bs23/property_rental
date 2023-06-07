{
    'name': 'Property Rental',
    'author': "Abu Raihan",
    'installable': True,
    'application': True,
    'depends': ['mail'],
    'sequence': -96,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/property_type.xml',
        'views/property_tag.xml',
        'views/rental_offers.xml',
        'views/property_view.xml',
        'views/property_rental_menus.xml',

    ]
}
