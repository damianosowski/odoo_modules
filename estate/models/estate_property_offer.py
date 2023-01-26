from odoo import fields, models, api
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError
from odoo.tools.translate import _


class EstatePropertyType(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Tags"
    _order = "price desc"

    price = fields.Float('Price')
    status = fields.Selection(string='Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity (Days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_deadline', inverse='_inverse_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id')

    _sql_constraints = [
        ('check_price', 'CHECK (price > 0)', 'An offer price must be strictly positive')
    ]

    @api.depends('validity')
    def _compute_deadline(self):
        for offer in self:
            offer.date_deadline = (offer.create_date or date.today()) + timedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_accept(self):
        if any(status == 'accepted' for status in self.property_id.offers_ids.mapped('status')):
            raise UserError(_('Only one offer can be accepted'))
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id
        self.property_id.salesperson_id = self.env.user
        self.property_id.state = 'offer_accepted'


    def action_refuse(self):
        self.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            property_id.state = 'offer_received'
            max_offer = max(offer.price for offer in property_id.offers_ids)
            if vals['price'] < max_offer:
                raise UserError(f'The offer must be higher than {max_offer}')
            return super(EstatePropertyType, self).create(vals)





