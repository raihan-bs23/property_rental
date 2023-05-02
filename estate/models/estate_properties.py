from odoo import fields, models, tools


class RealEstateProperties(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"

    name = fields.Char(string='Estate Name', required=True)
    description = fields.Text(string="description")
    postcode = fields.Char(string="postcode")
    date_availability = fields.Date(string="Date")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="No. of Bedrooms")
    living_area = fields.Integer(string="Living Area in SQ.")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Have Garage ?")
    garden = fields.Boolean(string="Have Garden ?")
    garden_area = fields.Boolean(string="Garden Area")
    garden_orientation = fields.Selection(string="Garden Orientation Type", selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
