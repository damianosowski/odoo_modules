from odoo import fields, models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def set_status_to_sold(self):
        move_id = self.env['account.move'].create(
            {
                'move_type': 'out_invoice',
                'partner_id': self.partner_id.id,
                "line_ids": [
                    Command.create({
                        "name": self.name,
                        "quantity": 0.06,
                        "price_unit": self.selling_price,
                    }),
                    Command.create({
                        "name": 'Administrative fees',
                        "quantity": 1,
                        "price_unit": 100,
                    }),
                ],
            })
        super(EstateProperty, self).set_status_to_sold()
