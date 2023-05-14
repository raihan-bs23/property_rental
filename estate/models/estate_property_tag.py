from odoo import fields, models, tools

from src.odoo.odoo import api
from src.odoo.odoo.cli.scaffold import env
from src.odoo.odoo.exceptions import ValidationError


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

    # @api.constrains('tag_name')
    # def check_property_tag(self):
    #     for record in self:
    #         lst = self.search([]).mapped('tag_name')
    #         var = lst[:-1]
    #         if record.tag_name in var:
    #             raise ValidationError("Property Tag already exist !")
