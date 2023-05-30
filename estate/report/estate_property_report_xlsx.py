from odoo import api, fields, models


class EstatePropertyXlsx(models.AbstractModel):
    _name = 'report.estate.property_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, property):
        bold = workbook.add_format({'bold': True})
        sheet = workbook.add_worksheet("Properties")
        sheet.set_column('A:R', 18)
        row = 1
        col = 0
        label_name = [
            "Name",
            "Expected Price",
            "Selling Price",
            "Best Price",
            "Bedrooms",
            "living Area",
            "Garage",
            "Garden",
            "Garden Area",
            "Garden Orientation",
            "Status",
            "Property Type",
            "Seller",
            "Buyer",

        ]
        for obj in property:
            value = {
                'Name': obj.name,
                'Expected Price': obj.expected_price,
                'Selling Price': obj.selling_price,
                'Best Price': obj.best_price,
                'Bedrooms': obj.bedrooms,
                'living Area': obj.living_area,
                'Garage': obj.garage,
                'Garden': obj.garden,
                'Garden Area': obj.garden_area,
                'Garden Orientation': obj.garden_orientation,
                'Status': obj.status,
                'Property Type': obj.property_type_id.property_type,
                'Seller': obj.seller_id.display_name,
                'Buyer': obj.buyer_id.display_name,
            }
            if col == 0:
                for i in label_name:
                    sheet.write(0, col, i, bold)
                    col += 1
            col = 0
            for j in value.values():
                sheet.write(row, col, j)
                col += 1
            row += 1
