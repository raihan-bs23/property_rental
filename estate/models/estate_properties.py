from dateutil.relativedelta import relativedelta
from odoo import fields, models, tools


class RealEstateProperties(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"

    name = fields.Char(string='Estate Name', required=True)
    description = fields.Text(string="description")
    postcode = fields.Char(string="postcode")
    date_availability = fields.Date(string="Availability Date", default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="No. of Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area in (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Have Garage ?")
    garden = fields.Boolean(string="Have Garden ?")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(string="Garden Orientation Type", selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    active = fields.Boolean(string='is active?', default=False)
    status = fields.Selection(string="Status", selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], default='new')


# class AddNewFields(models.Model):
#     _inherit = 'estate.property'
#
#     active = fields.Boolean(string='is active?', default=False)
#     status = fields.Selection(string="Status", selection=[
#         ('new', 'New'),
#         ('offer_received', 'Offer Received'),
#         ('offer_accepted', 'Offer Accepted'),
#         ('sold', 'Sold'),
#         ('canceled', 'Canceled')
#     ], default='new') 26334
