# -*- coding: utf-8 -*-

{
    'name': 'Helpdesk Curso Odoo',
    'version': '11.0',
    'author': 'César Castañón',
    'license': 'AGPL-3',
    'category': 'Helpdesk',
    'description': """
Helpdesk creado durante el curso de Odoo de Factor Libre
    """,
    'depends': ['mail'],
    'data': [
        'views/helpdesk_ticket_views.xml',
        'views/helpdesk_ticket_tag_views.xml',
        'views/inherit_res_partner_views.xml',
        'security/helpdesk_ticket_security.xml',
        'data/helpdesk_data.xml',
        'security/ir.model.access.csv',
        'views/helpdesk_ticket_stages_views.xml',
        'views/helpdesk_ticket_team_view.xml',
        'views/inherit_helpdesk_ticket_views.xml',
        'views/inherit_res_users.xml'

    ],
    'installable': True
}
