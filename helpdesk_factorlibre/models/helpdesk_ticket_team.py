# -*- coding: utf-8 -*-
# © 2020 César Castañón
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class HelpdeskTicketTeam(models.Model):
    _name = 'helpdesk.ticket.team'

    name = fields.Char(
        string='Title',
    )
    description = fields.Text(
        string='Description',
    )

    color = fields.Integer("Color Index", default=0)

    ticket_ids = fields.One2many(
        'helpdesk.ticket',
        'team_id',
        string="Tickets")

    todo_ticket_ids = fields.One2many(
        'helpdesk.ticket',
        'team_id',
        string="Todo tickets")
