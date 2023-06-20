from dateutil.relativedelta import relativedelta
from odoo import fields, models, tools, api
from odoo.exceptions import UserError, ValidationError


class RealEstateProperties(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"
    _order = 'id desc'

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
    seller_id = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    buyer_id = fields.Many2one('res.partner', string="Buyer Name", readonly=True)
    tag_id = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many('estate.property.offers', 'property_ids', string="Property Offers")
    total_area = fields.Integer(compute='_compute_total_area', string="Total Area", store=True)
    best_price = fields.Float(compute='_compute_best_price', string="Best Offer")
    color = fields.Integer(string="color", compute='_compute_color')

    _sql_constraints = [
        ('unique_property_name', 'UNIQUE(name)', 'Property name already exists!'),
        ('check_expected_price', 'CHECK(expected_price >= 0.0 OR expected_price IS NULL)',
         'Expected price must be non-negative!'),
    ]

    @api.depends('status')
    def _compute_color(self):
        for record in self:
            if record.status == 'new':
                record.color = 2
            elif record.status == 'offer_received':
                record.color = 5
            elif record.status == 'offer_accepted':
                record.color = 10
            else:
                record.color = 1

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            if 0.0 in prices:
                raise ValidationError("Offered Price Can't be Zero!")
            elif prices:
                record.best_price = max(prices)
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False

    def property_state_type_sold(self):
        for record in self:
            if record.status != 'sold' and record.status != 'canceled':
                record.status = 'sold'

    def property_state_type_canceled(self):
        for record in self:
            if record.status != 'sold' and record.status != 'canceled':
                record.status = 'canceled'

    @api.constrains('offer_ids')
    def offer_received(self):
        for record in self:
            offer_c = len(record.offer_ids)
            if offer_c > 0:
                self.status = 'offer_received'
            else:
                self.status = 'new'

    @api.ondelete(at_uninstall=False)
    def _unlink_except_state_new_canceled(self):
        for record in self:
            if record.status in ['offer_received', 'offer_accepted', 'sold']:
                raise ValidationError("This Property Can't be deleted! Because this property has dependencies.")

    @api.constrains('selling_price', 'expected_price')
    def check_selling_price(self):
        for record in self:
            exp = record.expected_price * .9
            if record.status not in ['offer_received', 'offer_accepted']:
                pass
            elif record.selling_price < exp:
                raise ValidationError("Selling Price Cannot be less than 90% of expected price ")
