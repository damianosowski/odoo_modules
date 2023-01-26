from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.tag'
    _description = "Estate Property Tags"
    _order = "name"

    name = fields.Char('Property Tags', required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'A property tag name must be unique')
    ]

