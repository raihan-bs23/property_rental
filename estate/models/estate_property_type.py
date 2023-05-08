from odoo import fields, models, tools

from src.odoo.odoo import api


class RealEstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type for the Property Table'

    property_type = fields.Selection(string="Property Type", required=True, selection=[
        ('house', 'House'),
        ('apartment', 'Apartment')
    ], default='house')
    buyer = fields.Many2one('res.partner')
    seller = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    _rec_name = 'property_type'
