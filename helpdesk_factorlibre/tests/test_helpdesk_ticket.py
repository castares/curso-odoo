from odoo.tests import common


class TestHelpdeskTicket(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestHelpdeskTicket, cls).setUpClass()
        helpdesk_ticket = cls.env['helpdesk.ticket']
        cls.stage_closed = cls.env.ref(
            'helpdesk_mgmt.helpdesk_ticket_stage_done'
        )

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
