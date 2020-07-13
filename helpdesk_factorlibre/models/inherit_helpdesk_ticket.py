from odoo import models, fields, _, api


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def _get_default_stage_id(self):
        return self.env['helpdesk.ticket.stage'].search([], limit=1).id

    def _get_default_team_id(self):
        return self.env['helpdesk.ticket.team'].search([], limit=1).id

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['helpdesk.ticket.stage'].search([])
        return stage_ids

    stage_id = fields.Many2one(
        comodel_name='helpdesk.ticket.stage',
        string='Stage',
        group_expand='_read_group_stage_ids',
        default=_get_default_stage_id,
        track_visibility='onchange',
    )

    kanban_state = fields.Selection([
        ('normal', 'Default'),
        ('done', 'Ready for next stage'),
        ('blocked', 'Blocked')], string='Kanban State')

    team_id = fields.Many2one('helpdesk.ticket.team',
                              default=_get_default_team_id)

    color = fields.Integer("Color Index", default=0)

    unattended = fields.Boolean(related='stage_id.unattended')
