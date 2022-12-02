from odoo import models, fields, api
from datetime import datetime, timedelta


class SaleOrderArchived(models.Model):
    _inherit = "sale.order"

    active = fields.Boolean(string="Active", default=True)

    def _archive_orders(self):
        orders_to_archive = self.env['sale.order'].search([
            ('state', 'in', ['sale', 'done', 'cancel']),
            ('date_order', '<=', datetime.today() + timedelta(days=-30)),
            ('active', '=', True)])
        for order in orders_to_archive:
            self.env['sale.order.archived'].create({'order_id': order.id})
            order.active = False
