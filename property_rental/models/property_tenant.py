from odoo import fields, models, tools, api


class PropertyTenant(models.Model):
    # _name = 'property.tenant'
    _description = 'This Module includes the property details and business logic related to property'
    _inherit = ['res.users']
    _order = 'id desc'

    property_id = fields.One2many('property.details', 'offer_partner', string="Tenant's Property")
    offer_ids = fields.One2many('rental.offers', 'partner_id', string="Offers")
    rented_property_ids = fields.Many2many(
        'property.details',
        string='Rented Properties',
        compute='compute_rented_properties',
        store=True
    )

    @api.constrains('property_id')
    def compute_rented_properties(self):
        for record in self:
            record.rented_property_ids = record.property_id.filtered(
                lambda prop: prop.status == 'rented' and prop.renter == self.name)
            print("Rented Properties", record.rented_property_ids)

