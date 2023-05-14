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
    seller_id = fields.Many2one(string="Salesman", related="property_type_id.seller")
    buyer_id = fields.Many2one('res.partner', string="Buyer Name", readonly=True)
    tag_id = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many('estate.property.offers', 'property_ids', string="Offers")
    total_area = fields.Integer(compute='_compute_total_area', string="Total Area", store=True)
    best_price = fields.Float(compute='_compute_best_price', string="Best Offer")
    state = fields.Char(string="Status", readonly=True)

    # _sql_constraints = [
    #     ('positive_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive!'),
    #     ('positive_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive!'),
    #     ('unique_property_name', 'UNIQUE(name)', 'Property name must be unique!'),
    # ]
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

    def property_state_type_sold(self):
        for record in self:
            state = self.state
            print(state)
            if state is False:
                record.state = "SOLD"
                record.status = 'sold'
                print(record.state)
            else:
                if record.state == "SOLD":
                    raise UserError("You have already Sold !")
                elif record.state == "Canceled":
                    raise UserError("Canceled property cannot be Sold !")

    def property_state_type_canceled(self):
        for record in self:
            state = self.state
            print(state)
            if state is False:
                record.state = "Canceled"
                record.status = 'canceled'
                print(record.state)
            else:
                if record.state == "Canceled":
                    raise UserError("You have already Canceled !")
                elif record.state == "SOLD":
                    raise UserError("Sold property cannot be Canceled !")

    @api.constrains('name')
    def _check_property_name(self):
        for record in self:
            lst = self.search([]).mapped('name')
            var = lst[-1:]
            print(var)
            if record.name in var:
                raise ValidationError("Property Name already exist !")

    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError("Expected Price must Should be Positive")

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0:
                raise ValidationError("Selling Price must Should be Positive")

    @api.constrains('offer_ids')
    def offer_received(self):
        for record in self:
            offer_c = len(record.offer_ids)
            print("length - ", offer_c)
            if offer_c > 0:
                print("offer recieved")
                self.status = 'offer_received'
            else:
                print("New")
                print(record.selling_price)
                self.status = 'new'




