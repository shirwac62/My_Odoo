# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'category': 'Website',
    'author': 'Shirwac',
    'sequence': -100,
    'summary': 'Hospital Management System',
    'description': """Hospital Management System""",
    'depends': ['mail', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/patient_tag_data.xml',
        'data/sequence_data.xml',
        'data/patient.tag.csv',
        'wizard/cancel_appointment_view.xml',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/patient_female_view.xml',
        'views/appointment_view.xml',
        'views/patient_tag.xml',
        'views/less_than_20.xml',
        'views/odoo_playground_view.xml',
        'views/res_config_settings_views.xml',
        'views/operation_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
