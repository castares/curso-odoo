from odoo.tests import common


class TestHelpdeskTicket(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestHelpdeskTicket, cls).setUpClass()
        helpdesk_ticket = cls.env['helpdesk.ticket']
        cls.stage_closed = cls.env.ref(
            'helpdesk_factorlibre.helpdesk_ticket_stage_done'
        )
        cls.user_demo = cls.env.ref('base.user_demo')
        cls.ticket = helpdesk_ticket.create({
            'name': 'Test 1',
            'description': 'Ticket test',
        })

    def test_helpdesk_ticket_assign_to_me(self):
        # Verify the ticket is unassigned
        self.assertFalse(self.ticket.assignation_date)

        # Execute the method
        self.ticket.assign_to_me()

        # Verify the method
        self.assertEquals(self.ticket.user_id, self.env.user.id)

    def test_helpdesk_ticket_onchange_partner_id(self):
        # Verify the parter is undefined
        self.assertFalse(self.ticket.partner_id)

        # Assign a partner to the ticket
        self.ticket.partner_id = self.user_demo.id

        # Verify that mail and email change
        self.assertEquals(self.ticket.customer_name, self.user_demo.name)
        self.assertEquals(self.ticket.customer_mail, self.user_demo.email)
