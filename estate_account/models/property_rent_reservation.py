from odoo import fields, models, api


class PropertyRental(models.Model):
    _inherit = 'property.details'

    move_id = fields.Many2one('account.move')
    partner_id = fields.Many2one('res.users')
    current_date = fields.Date(default=lambda self: fields.Date.today())
    accepted_price = fields.Float(compute='_compute_best_price')

    def send_invoice(self):
        print("Overridden method worked!")
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        for rec in self:
            move = self.env["account.move"].create(
                {
                    "partner_id": rec.offer_partner.id,
                    "move_type": "out_invoice",
                    "invoice_date": rec.current_date,
                    "journal_id": journal.id,
                    "invoice_line_ids": [
                        (0, 0, {  # Use (0, 0, {}) to create new records in a One2many field
                            "name": rec.property_name,
                            "price_unit": rec.accepted_price,
                        }),
                        (0, 0, {
                            "name": "Service Charge",
                            "price_unit": 1500,
                        }),
                    ]
                })
            rec.move_id = move
        return super(PropertyRental, self).send_invoice()

    @api.depends('offer_ids.price', 'offer_ids.status')
    def _compute_best_price(self):
        for record in self:
            accepted_offers = record.offer_ids.filtered(lambda offer: offer.status == 'accepted')
            if accepted_offers:
                record.accepted_price = accepted_offers[0].price
            else:
                record.accepted_price = 0.0
