# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    email_cc_partners = fields.Many2many(
        'res.partner',
        'helpdesk_ticket_res_partner_cc_rel',
        'ticket_id',
        'partner_id', string='Email cc')

    def _notify_by_email_add_values(self, base_mail_values):
        """ Add CC emails
        """
        base_mail_values = super(HelpdeskTicket, self)._notify_by_email_add_values(base_mail_values)
        if self.email_cc_partners:
            cc_email_list = self.email_cc_partners.mapped('email')
            cc_email = {
                'email_cc': ", ".join(cc_email_list),
            }
            base_mail_values.update(cc_email)
        return base_mail_values

    def _message_get_suggested_recipients(self):
        recipients = super(HelpdeskTicket, self)._message_get_suggested_recipients()
        try:
            for ticket in self.filtered(lambda rec: rec.email_cc_partners):
                for email in self.email_cc_partners.mapped('email'):
                    ticket._message_add_suggested_recipient(recipients, email=email, reason=_('CC'))
        except AccessError:  # no read access rights -> just ignore suggested recipients because this implies modifying followers
            pass
        return recipients

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, *,
                     body='', subject=None, message_type='notification',
                     email_from=None, author_id=None, parent_id=False,
                     subtype_xmlid=None, subtype_id=False, partner_ids=None, channel_ids=None,
                     attachments=None, attachment_ids=None,
                     add_sign=True, record_name=False,
                     **kwargs):
        if partner_ids:
            partner_ids = [partner for partner in partner_ids if partner not in self.email_cc_partners.ids]
        if self.email_cc_partners:
            kwargs.update({'email_cc_ids': self.email_cc_partners})
        new_message = super(HelpdeskTicket, self).message_post(
            body=body, subject=subject, message_type=message_type,
            email_from=email_from, author_id=author_id, parent_id=parent_id,
            subtype_xmlid=subtype_xmlid, subtype_id=subtype_id, partner_ids=partner_ids, channel_ids=channel_ids,
            attachments=attachments, attachment_ids=attachment_ids,
            add_sign=add_sign, record_name=record_name,
            **kwargs)
        return new_message
