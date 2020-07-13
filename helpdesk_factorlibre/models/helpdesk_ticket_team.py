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

    open_ticket_count = fields.Integer(
        string="Number of tickets",
        compute='_compute_open_tickets')

    open_ticket_count_unassigned = fields.Integer(
        string="Number of tickets unassigned",
        compute='_compute_open_tickets')

    open_ticket_count_unattended = fields.Integer(
        string="Number of tickets unattended",
        compute='_compute_open_tickets')

    open_ticket_count_high_priority = fields.Integer(
        string="Number of tickets in high priority",
        compute='_compute_open_tickets')

    @api.depends('ticket_ids')
    def _compute_open_tickets(self):
        for record in self:
            open_ticket_ids = record.ticket_ids.filtered(
                lambda ticket: ticket.stage_id.closed == False)
            record.open_ticket_count = len(open_ticket_ids)
            record.open_ticket_count_unassigned = len(
                open_ticket_ids.filtered(
                    lambda ticket: not ticket.user_id))
            record.open_ticket_count_unattended = len(
                open_ticket_ids.filtered(
                    lambda ticket: ticket.unattended))
            record.open_ticket_count_high_priority = len(
                open_ticket_ids.filtered(
                    lambda ticket: ticket.priority == '3'))
