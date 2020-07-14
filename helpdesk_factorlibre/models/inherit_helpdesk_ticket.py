from odoo import models, fields, _, api


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def _get_default_stage_id(self):
        return self.env['helpdesk.ticket.stage'].search([], limit=1).id

    def _get_default_team_id(self):
        return self.env['helpdesk.ticket.team'].search([], limit=1).id

    def _get_default_partner_id(self):
        return self.env.user.partner_id

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['helpdesk.ticket.stage'].search([])
        return stage_ids

    partner_id = fields.Many2one(
        string='Customer',
        comodel_name='res.partner',
        ondelete='restrict',
        default=_get_default_partner_id
    )

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
                              default=_get_default_team_id,
                              ondelete='restrict')

    color = fields.Integer("Color Index", default=0)

    unattended = fields.Boolean(related='stage_id.unattended')

    @api.multi
    @api.onchange('team_id')
    def on_change_team_id(self):
        for record in self:
            least_open_tickets_users = self.env['res.users'].search(
                [('team_ids', '=', record.team_id.id)], order='count_open_tickets asc', limit=1)
            if record.team_id.id not in [team.id for team in record.user_id.team_ids]:
                record.update({
                    'user_id': least_open_tickets_users.id
                })

    @api.multi
    @api.onchange('user_id')
    def on_change_user_id(self):
        for record in self:
            user_first_team = self.env['helpdesk.ticket.team'].search(
                [('user_ids', '=', record.user_id.id)], limit=1)
            if user_first_team:
                record.update({
                    'team_id': user_first_team.id
                })
