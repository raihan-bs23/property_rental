from odoo import fields, models, tools

from src.odoo.odoo import api
from src.odoo.odoo.exceptions import ValidationError


class RealEstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type for the Property Table'
    _order = 'type_sequence, property_type'

    property_type = fields.Selection(string="Property Type", required=True, selection=[
        ('house', 'House'),
        ('apartment', 'Apartment')
    ], default='house')
    buyer = fields.Many2one('res.partner', readonly=True)
    seller = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', required=True)
    type_sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many('estate.property.offers', 'property_type_id', string="Offers")
    offer_count = fields.Integer(compute='_compute_offer_counts')
    views = fields.Many2many('ir.ui.view', string="Views", readonly=True,
                             default=lambda self: self.env.ref('estate.property.offers.view_estate_property_offers_tree').id)
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

    @api.depends('offer_ids')
    def _compute_offer_counts(self):
        for record in self:
            print(record.offer_ids)
            record.offer_count = len(record.offer_ids)
            print(record.offer_count)

    def show_all_offers(self):
        print("hello")
        return {
            'name': 'Offers',
            'res_model': 'estate.property.offers',
            'view_mode': 'tree,form',
            'context': {},
            'domain': [('property_type_id', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',

        }
