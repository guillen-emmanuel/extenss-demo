# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Extenss Request',
    'version' : '1.0',
    'summary': 'Extenss Request Loan',
    'description': 'Extenss Request Loan',
    'author': 'Mastermind Software Services',
    'depends': ['crm','sale'],
    'application': False,
    'website': 'https://www.mss.mx',
    'category': 'Sales/CRM',
    'data': [
        'security/extenss_request_security.xml',
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/sale_order_views.xml',

    ],
}
