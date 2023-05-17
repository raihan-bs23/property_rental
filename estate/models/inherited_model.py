from dateutil.relativedelta import relativedelta
from odoo import fields, models, tools, http, api


class InheritedModel(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'seller_id', domain=[
        ('status', '!=', ['sold', 'canceled'])
    ])
