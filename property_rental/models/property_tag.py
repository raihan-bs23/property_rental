from odoo import fields, models, tools, api

class RentalPropertyType(models.Model):
    _name = 'rental.property.tag'
    _description = 'Rental Property Tag'
    _rec_name = 'tag_name'
    _order = 'id desc'

    tag_name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer(string="Color")


    _sql_constraints = [
        ('unique_property_tag', 'UNIQUE(tag_name)', 'Property Tag must be Unique')
    ]

