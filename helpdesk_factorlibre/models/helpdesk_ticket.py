# -*- coding: utf-8 -*-
# © 2020 César Castañón
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, _, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_user_id(self):
        return 1

    def _get_default_priority(self):
        return "Medium"

    name = fields.Char(
        string='Title',
        required=True
    )
    description = fields.Html(
        string='Description',
    )

    assignation_date = fields.Datetime(
        string="Assignation Date",
        compute="_compute_assignation_date",
        store=True
    )

    closing_date = fields.Datetime(
        string="Closing Date",
        compute="_compute_closing_date",
        store=True)

    ticket_id = fields.Integer(string="Ticket Number")

    priority = fields.Selection([
        ('Zero', _('Sin prioridad')),
        ('Low', _('Prioridad Baja')),
        ('Medium', _('Prioridad Media')),
        ('High', _('Prioridad Alta')),
    ], string='Priority', default=_get_default_priority, help="Choose a priority for the ticket")

    user_id = fields.Many2one(
        string='Assigned to',
        comodel_name='res.users',
        ondelete='restrict',
        default=_get_default_user_id
    )

    tag_ids = fields.Many2many(
        string="Tags",
        comodel_name='helpdesk.ticket.tag'
    )

    partner_id = fields.Many2one(
        string='Customer',
        comodel_name='res.partner',
        ondelete='restrict'
    )

    customer_name = fields.Char(string='Customer Name')

    customer_mail = fields.Char(string='Customer Mail')

    @api.multi
    def assign_to_me(self):
        self.write({
            'user_id': self.env.user.id
        })

    ### On Change Methods ###

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for record in self:
            partner = record.partner_id
            if partner:
                record.update({
                    'customer_name': partner.name,
                    'customer_mail': partner.email
                })

    ### Depends Methods ###

    @api.depends('user_id')
    def _compute_assignation_date(self):
        self.assignation_date = fields.Datetime.now()

    @api.depends('stage_id')
    def _compute_closing_date(self):
        for record in self:
            stage_id = record.stage_id
            if stage_id.name in ["Done", "Cancelled"]:
                record.closing_date = fields.Datetime.now()

    ### CRUD Methods ###

    @api.model
    def create(self, vals):
        if vals.get("partner_id") and ("customer_name" not in vals or "customer_mail" not in vals):
            partner = self.env["res.partner"].browse(vals["partner_id"])
            vals.setdefault("customer_name", partner.name)
            vals.setdefault("customer_mail", partner.email)

        return super().create(vals)
