{
    'name': 'Real Estate',
    'author': "Abu Raihan",
    'installable': True,
    'application': True,
    'sequence': -100,
    'license': 'LGPL-3',
    'depends': ['report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_settings.xml',
        'views/multiple_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'views/inherited_views.xml',
        'report/estate_property_reports.xml',
        'report/estate_property_templates.xml',
    ]
}
