{
    'name': 'Property Rental',
    'author': "Abu Raihan",
    'installable': True,
    'application': True,
    'depends': ['mail', 'report_xlsx'],
    'license': 'LGPL-3',
    'sequence': -96,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/property_tenant.xml',
        'views/property_type.xml',
        'views/property_tag.xml',
        'views/rental_offers.xml',
        'views/property_view.xml',
        'views/property_rental_menus.xml',
        # 'views/inherit_views.xml',
        'report/rental_property_report.xml',
        'report/rental_report_template.xml'

    ]
}
