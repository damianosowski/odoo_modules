from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Property module"
    _order = "id desc"

    name = fields.Char('Name of the Property', required=True)
    property_type_id = fields.Many2one('estate.property.type')
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability Date', copy=False, default=lambda self: fields.Datetime.add(fields.Datetime.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Number of bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    state = fields.Selection(string='State', selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], default='new', copy=False, required=True)

    active = fields.Boolean(string="Active", default=True)
    partner_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user, copy=False)
    property_tag_ids = fields.Many2many('estate.property.tag')
    offers_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id', copy=False)
    total_area = fields.Integer("Total area", compute='_compute_total_area')
    best_price = fields.Float('Best Offer', compute='_compute_best_offer')

    _sql_constraints = [
        ('check_expected_price', 'CHECK (expected_price > 0)', 'A property expected price must be strictly positive'),
        ('check_selling_price', 'CHECK (selling_price > 0)', 'A property selling price must be positive'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offers_ids')
    def _compute_best_offer(self):
        for property in self:
            if property.offers_ids:
                property.best_price = max(property.offers_ids.mapped('price'))
            else:
                property.best_price = None

    @api.onchange('garden')
    def _onchange_garden_area_and_orientation(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def set_status_to_sold(self):
        if self.state == 'canceled':
            raise UserError(_('Canceled properties cannot be sold'))
        else:
            self.state = 'sold'

    def set_status_to_canceled(self):
        if self.state == 'sold':
            raise UserError(_('Sold properties cannot be cancelled'))
        else:
            self.state = 'canceled'

    @api.constrains('selling_price', 'expected_price')
    def check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and \
                    float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0:
                raise ValidationError('The selling price cannot be lower than 90% of the expected price.')

    @api.ondelete(at_uninstall=False)
    def _unlink_ony_new_and_canceled(self):
        if any(prop.state not in ('new', 'canceled') for prop in self):
            raise UserError("Only new or canceled properties can be deleted")

