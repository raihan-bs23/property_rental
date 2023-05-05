from odoo import fields, models, tools

from src.odoo.odoo import api


class RealEstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type for the Property Table'

    property_type = fields.Selection(string="Property Type", required=True, selection=[
        ('house', 'House'),
        ('apartment', 'Apartment')
    ], default='house')
    buyer = fields.Char(string='Buyer Name')
    seller = fields.Char(string="Salesman", default=lambda self: self.env.user.name)

    def name_get(self):
        result = []
        for record in self:
            property_type = record.property_type
            result.append((record.id, property_type))
        return result
