# -*- coding: utf-8 -*-
{
    'name': "Purchase Single Tax Field",

    'summary': """
        Automate tax update process with a single tax field 
        """,

    'description': """
         Purchase Single Tax Field is a module that adds a single tax field with an update button
    """,

    'author': "Brain Station 23 Ltd",
    'license': 'LGPL-3',
    'website': "http://www.brainstation-23.com",

    'category': 'Inventory',
    'version': '15.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['purchase'],

    # always loaded
    'data': [
        'views/purchase_order_form_view.xml'

    ],
    'images': ['static/description/banner.gif'],
    'application': True,
    'installable': True,
    'support': 'support@brainstation-23.com',

}
