from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Types"
    _order = "sequence, name"

    name = fields.Char('Property Types', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer('Number of offers', compute='_compute_offers')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'A property type name must be unique')
    ]

    def _compute_offers(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)

