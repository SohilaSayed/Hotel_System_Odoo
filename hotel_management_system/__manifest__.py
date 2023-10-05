# -*- coding: utf-8 -*-
{
    'name': "Hotel",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Sohila",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Hotel',
    'version': '1.2',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','contacts','hr',],

    # always loaded
    'data': [
        'security/hotel_security.xml',
        'security/ir.model.access.csv',
        'views/hotel_room_facility.xml',
        'views/hotel_reservation.xml',
        'views/hotel_room.xml',
        'views/hotel_statistics.xml',
        'data/data.xml',
        'views/res_partner.xml',
        'security/hotel_security_rules.xml',
        'reports/hotel_room_report.xml',
        'reports/reservations_template.xml',
        'reports/hotel_wizard_template.xml',
        'reports/hotel_wizrd_report.xml',
        'reports/employee_report.xml',
        'reports/employee_template.xml',
        'wizards/hotel_wizard.xml',
        'wizards/employee_wizard.xml',
        'views/hotel_menuitems.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            #'hotel_management_system/static/src/css/hotel.css'
        ]
    }
}

