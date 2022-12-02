from odoo import models, fields, api


class SaleOrderArchived(models.Model):
    _name = "sale.order.archived"

    order_id = fields.Many2one(comodel_name='sale.order', string="Sale Order")
    order_name = fields.Char(string="Name", related='order_id.name')
    final_price = fields.Monetary(string='Final price', related='order_id.amount_total')
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency", readonly=True, related="order_id.currency_id")
    partner_id = fields.Many2one(comodel_name="res.partner", related="order_id.partner_id", string="Partner")
    date = fields.Datetime(string='Order Date', related="order_id.date_order")

