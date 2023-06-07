from odoo import fields, models, tools, api


class PropertyTenant(models.Model):
    # _name = 'property.tenant'
    _description = 'This Module includes the property details and business logic related to property'
    _inherit = ['res.users', ]
    _order = 'id desc'

    property_id = fields.One2many('property.details', 'offer_partner')

    offer_ids = fields.One2many('rental.offers', 'partner_id', string="Offers", tracking=True)

    def test_tenant(self):
        for rec in self:
            print(len(rec.offer_ids))
            for i in self.offer_ids:
                if i.status != False:
                    print(i)
                    print("property status", i.status)
                    for j in i.property_ids:
                        print("Property Name", j.property_name)
