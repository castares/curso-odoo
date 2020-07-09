from odoo.tests import common


class TestHelpdeskTicket(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestHelpdeskTicket, cls).setUpClass()
        helpdesk_ticket = cls.env['helpdesk.ticket']
        cls.stage_closed = cls.env.ref(
            'helpdesk_factorlibre.helpdesk_ticket_stage_done'
        )
        cls.user_root = cls.env.ref('base.user_root')
        cls.user_demo = cls.env.ref('base.user_demo')
        cls.ticket = helpdesk_ticket.create({
            'name': 'Test 1',
            'description': 'Ticket test',
        })

    # TODO: Incluir texto en cada método para saber el momento del fallo.

    def test_helpdesk_ticket_assign_to_me(self):

        # Remove assigned user
        self.ticket.user_id = False

        # Execute the method
        self.ticket.assign_to_me()

        # Verify the method
        self.assertEquals(self.ticket.user_id.id, self.env.user.id)

    def test_helpdesk_ticket_onchange_partner_id(self):
        # Assign a partner to the ticket
        partner = self.env["res.partner"].search([], limit=1)
        self.ticket.partner_id = partner.id

        # Execute the method
        self.ticket.onchange_partner_id()

        # Verify that mail and email change
        self.assertEquals(self.ticket.customer_name, partner.name)
        self.assertEquals(self.ticket.customer_mail, partner.email)
