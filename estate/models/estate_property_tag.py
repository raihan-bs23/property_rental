from odoo import fields, models, tools, api


class RealEstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag for the Property Table'
    _order = 'tag_name'

    tag_name = fields.Char(string="Tag Name", required=True)
    tag_sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    color = fields.Integer(string='Color')
    _rec_name = 'tag_name'

    _sql_constraints = [
        ('unique_property_tag_name', 'UNIQUE(tag_name)', 'Property tag name must be unique!'),
    ]