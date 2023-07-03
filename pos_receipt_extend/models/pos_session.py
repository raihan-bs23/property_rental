import re

from odoo import models, fields, api
import math


class PosOrder(models.Model):
    _inherit = 'pos.order'

    pos_config = fields.Many2many('pos.config', 'pos_receipt')

    @api.model
    def get_custom_data(self, id):
        pos_order_id = self.search([('id', '=', id)])

        return {
            'order_id': pos_order_id.id,
            'order_name': pos_order_id.name,
        }
