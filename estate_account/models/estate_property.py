from odoo import fields, models, tools, api, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    move_id = fields.Many2one('account.move')

    def property_state_type_sold(self):
        print("Overridden method worked !")
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        for rec in self:
            move = self.env["account.move"].create(
                {
                    "partner_id": rec.buyer_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    "invoice_line_ids": [
                        Command.create({
                                "name": rec.name,
                                "quantity": 1.0,
                                "price_unit": rec.selling_price * .06,
                            }),
                        Command.create({
                                "name": "Administrative fees",
                                "quantity": 1.0,
                                "price_unit": 100.0,
                            }),
                    ]
                })
            rec.move_id = move
        return super().property_state_type_sold()
