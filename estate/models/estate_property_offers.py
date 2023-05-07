from odoo import fields, models, tools

from src.odoo.odoo import api


class RealEstatePropertyOffers(models.Model):
    _name = 'estate.property.offers'
    _description = "This is Real Estate Property Offer Description"

    price = fields.Float(string="Offered Price")
    status = fields.Selection(string="Offer Status", selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_ids = fields.Many2one('estate.property', required=True)
