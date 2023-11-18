# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Message(models.Model):
    _inherit = 'mail.message'

    email_cc_ids = fields.Many2many('res.partner', 'mail_message_res_partner_cc_rel', 'message_id', 'partner_id', string='CC')

    def message_format(self):
        vals_list = super(Message, self).message_format()
        for vals in vals_list:
            message_sudo = self.browse(vals['id']).sudo().with_prefetch(self.ids)
            if message_sudo.email_cc_ids:
                vals.update({'email_cc_ids': ','.join(message_sudo.email_cc_ids.mapped('display_name'))})
        return vals_list
