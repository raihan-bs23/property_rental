from dateutil.relativedelta import relativedelta
from odoo import fields, models, tools
from src.odoo.odoo import api


class RealEstateProperties(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"

    name = fields.Char(string='Estate Name', required=True)
    description = fields.Text(string="description")
    postcode = fields.Char(string="postcode")
    date_availability = fields.Date(string="Availability Date",
                                    default=lambda self: fields.Date.today() + relativedelta(months=3))
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
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    seller_id = fields.Char(string="Salesman", related="property_type_id.seller")
    buyer_id = fields.Char(string="Buyer Name", related="property_type_id.buyer")
    tag_id = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many('estate.property.offers', 'property_ids', string="Offers")
    total_area = fields.Integer(compute='_compute_total_area', string="Total Area", store=True)
    best_price = fields.Float(compute='_compute_best_price', string="Best Offer")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            if prices:
                record.best_price = max(prices)
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            print(self.garden)
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False
