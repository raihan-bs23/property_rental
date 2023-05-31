from odoo import fields, models, tools, api
from odoo.exceptions import UserError, ValidationError

class PropertyDetails(models.Model):
    _name = 'property.details'
    _description = 'This Module includes the property details and business logic related to property'
    _rec_name = 'property_name'
    _order = 'id desc'

    property_name = fields.Char(string="Property Name", required=True)
    property_description = fields.Text(string="Property Description")
    postcode = fields.Char(string="Postcode")
    address = fields.Text(string="Address")
    expected_rent_price = fields.Integer(string="Expected Rent Price", required=True)
    rented_price = fields.Float(string="Rented Price", readonly=True)
    bedrooms = fields.Integer(string="No. of Bedrooms", default=3)
    living_area = fields.Integer(string="Living Area in (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Have Garage ?")
    garden = fields.Boolean(string="Have Garden ?")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    image = fields.Image("Image")
    garden_orientation = fields.Selection(string="Garden Orientation Type", selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    active = fields.Boolean(string='is active?', default=False)
    property_condition = fields.Selection(string="Property Condition", selection=[
        ('new', 'New'),
        ('used', 'Used')
    ], default='new')
    status = fields.Selection(string="Status", selection=[
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('rented', 'Rented'),
        ('returned', 'Returned')
    ], default='available')

    property_type_ids = fields.Many2many('rental.property.type')
    property_tag_ids = fields.Many2many('rental.property.tag')
    sales_man = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)

    @api.constrains('property_name')
    def check_property_name(self):
        for record in self:
            if record.property_name in self.search([]).mapped('property_name'):
                raise ValidationError("Property Name Must be Unique !")

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 50
            self.garden_orientation = 'south'
        else:
            self.garden_area = False
            self.garden_orientation = False

    @api.onchange('expected_rent_price')
    def _check_expected_rent_price(self):
        for record in self:
            if record.expected_rent_price < 0:
                raise ValidationError("Expected Rent Price Can't be less than Zero !!")

    @api.onchange('property_type_ids')
    def _prevent_multiple_property_type(self):
        for record in self:
            if len(record.property_type_ids) > 1:
                raise ValidationError("Multiple Property Type is not Allowed !")

    # property_condition_color = fields.Integer(string="color", compute='_compute_property_condition_color')
    #
    # @api.depends('property_condition')
    # def _compute_property_condition_color(self):
    #     for record in self:
    #         if record.property_condition == 'new':
    #             record.property_condition_color = '#00FF00'  # Green
    #         elif record.property_condition == 'used':
    #             record.property_condition_color = '#FF0000'  # Red
    #         else:
    #             record.property_condition_color = '#000000'  # Black
