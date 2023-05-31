from odoo import fields, models, tools, api

class RentalPropertyType(models.Model):
    _name = 'rental.property.type'
    _description = 'Rental Property Type'
    _rec_name = 'property_type'
    _order = 'id desc'

    property_type = fields.Char(string="Property Type", required=True)
    color = fields.Integer(string="Color")


    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(property_type)', 'Property Type must be Unique')
    ]

