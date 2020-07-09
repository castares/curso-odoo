# -*- coding: utf-8 -*-
# © 2020 César Castañón
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class HelpdeskTicketTeam(models.Model):
    _name = 'helpdesk.ticket.team'

    name = fields.Char(
        string='Title',
    )
    description = fields.Text(
        string='Description',
    )

    sequence = fields.Integer(default=1)

    color = fields.Integer("Color Index", default=0)

    ticket_ids = fields.One2many(
        comodel_name='helpdesk.ticket',
        inverse_name='team_id',
        string="Tickets")

    todo_ticket_ids = fields.One2many(
        comodel_name='helpdesk.ticket',
        inverse_name='team_id',
        string="Todo tickets")

    todo_ticket_count = fields.Integer(
        string="Number of tickets",
        compute='_compute_todo_tickets')

    @api.depends('ticket_ids')
    def _compute_todo_tickets(self):
        for record in self:
            record.todo_ticket_ids = record.ticket_ids.filtered(
                lambda ticket: ticket.stage_id.closed == False)
            record.todo_ticket_count = len(record.todo_ticket_ids)
