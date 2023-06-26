from odoo import models, fields, api


class PosConfigure(models.Model):
    _inherit = 'pos.config'

    pos_receipt = fields.Boolean(string="Pos Receipt", help="Create Order receipt along with your pos order invoice.")

    @api.onchange('pos_receipt')
    def test(self):
        for record in self:
            print("Recepit - ", record.pos_receipt)



