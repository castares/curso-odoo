# -*- coding: utf-8 -*-
# © 2020 César Castañón
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class HelpdeskTicketTag(models.Model):
    _name = 'helpdesk.ticket.tag'

    name = fields.Char(
        string='Title',
    )
    description = fields.Text(
        string='Description',
    )
