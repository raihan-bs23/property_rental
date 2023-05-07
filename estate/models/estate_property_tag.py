from odoo import fields, models, tools

from src.odoo.odoo import api


class RealEstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag for the Property Table'

    tag_name = fields.Char(string="Tag Name", required=True)
    _rec_name = 'tag_name'
