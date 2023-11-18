# -*- coding: utf-8 -*-

{
    'name': 'PwC tasks module',
    'version': '14.0.1.0.01',
    'author': 'Damian Osowski',
    'description': """
    Module with tasks for PwC
    """,
    'depends': ['helpdesk', 'project', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'views/helpdesk_views.xml',
        'wizard/mail_compose_message_view.xml',
        'wizard/wizard_task_calendar.xml',
        'report/report_task_pivot_xlsx.xml',
        'report/report_task_calendar.xml',
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/message_inherit.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
