from odoo import fields, models, tools

from src.odoo.odoo import api
from src.odoo.odoo.exceptions import ValidationError


class RealEstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type for the Property Table'

    property_type = fields.Selection(string="Property Type", required=True, selection=[
        ('house', 'House'),
        ('apartment', 'Apartment')
    ], default='house')
    buyer = fields.Many2one('res.partner', readonly=True)
    seller = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    _rec_name = 'property_type'

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(property_type)', 'Property Type must be Unique')
    ]

    # @api.constrains('property_type')
    # def _check_property_type_duplication(self):
    #     for record in self:
    #         type_house = 'house'
    #         type_apartment = 'apartment'
    #         if type_house in record.property_type:
    #             print(record.property_type)
    #             raise ValidationError("Property Type: House exist !")
    #         elif type_apartment in record.property_type:
    #             print(record.property_type)
    #             raise ValidationError("Property Type: Apartment exist !")