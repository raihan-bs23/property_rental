# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    tax_ids = fields.Many2many('account.tax', string='Tax/Vat')
    show_update_tax_button = fields.Boolean(string='Show update tax button', default=False)

    @api.onchange('tax_ids', 'order_line')
    def _onchange_tax_ids(self):
        current_tax_ids = []
        for tax_id in self.tax_ids:
            current_tax_ids.append(tax_id.id.origin)
        if self.order_line and self.tax_ids and self._origin.tax_ids.mapped('id') != current_tax_ids:
            self.show_update_tax_button = True
        elif self._origin.tax_ids and not self.tax_ids:
            self.show_update_tax_button = True
        else:
            self.show_update_tax_button = False

    def update_tax_vat(self):
        self.ensure_one()
        for line in self.order_line:
            if line.display_type == 'line_section':
                continue
            line.update({'taxes_id': [(6, 0, self.tax_ids.ids)]})
        self.show_update_tax_button = False


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _compute_tax_id(self):
        for line in self:
            line = line.with_company(line.company_id)
            fpos = line.order_id.fiscal_position_id or line.order_id.fiscal_position_id.get_fiscal_position(
                line.order_id.partner_id.id)
            # filter taxes by company
            taxes = line.product_id.supplier_taxes_id.filtered(lambda r: r.company_id == line.env.company)
            if line.order_id.tax_ids:
                taxes = line.order_id.tax_ids
            else:
                return
            line.taxes_id = fpos.map_tax(taxes)
