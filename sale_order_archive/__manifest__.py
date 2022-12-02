# -*- coding: utf-8 -*-
{
    'name': 'Sale order archive',
    'version': '14.0.0.0.1"',
    'category': 'Sale',
    'sequence': 50,
    'summary': 'Sale order archive',
    'description': """
Auto Sale Order archive for orders older than 30 days 
""",
    'author': "Damian Osowski",
    'depends': [
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sale_cron_data.xml',
        'views/sale_order_archived_view.xml',
    ],
    'qweb': [],
    'images': [],
    'installable': True,
}
