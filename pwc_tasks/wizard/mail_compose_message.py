# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'

    email_cc_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='mail_compose_message_res_partner_cc_rel',
        column1='composer_id',
        column2='partner_cc_id',
        string='CC')

    @api.model
    def default_get(self, fields):
        result = super(MailComposer, self).default_get(fields)
        if result.get('model') and result.get('model') == 'helpdesk.ticket':
            ticket_id = result.get('res_id')
            ticket = self.env['helpdesk.ticket'].browse(ticket_id)
            if result.get('partner_ids'):
                if ticket.email_cc_partners:
                    self.email_cc_ids = ticket.email_cc_partners
                for partner_ids in result['partner_ids']:  # - tuple with nested list e.g. (6, 0, [1, 2])
                    for partner_id in partner_ids[-1][::-1]:
                        if partner_id in ticket.email_cc_partners.ids:
                            partner_ids[-1].remove(partner_id)
        return result
