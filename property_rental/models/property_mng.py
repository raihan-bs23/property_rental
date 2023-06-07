from dateutil.relativedelta import relativedelta
from odoo import fields, models, tools, api
from odoo.exceptions import UserError, ValidationError


class PropertyDetails(models.Model):
    _name = 'property.details'
    _description = 'This Module includes the property details and business logic related to property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'property_name'
    _order = 'id desc'

    property_name = fields.Char(string="Property Name", required=True, tracking=True)
    property_description = fields.Text(string="Property Description")
    postcode = fields.Char(string="Postcode")
    address = fields.Text(string="Address")
    # expected_rent_price = fields.Integer(string="Expected Rent Price", required=True)
    rented_price = fields.Float(string="Rented Price", readonly=True)
    bedrooms = fields.Integer(string="No. of Bedrooms", default=3)
    living_area = fields.Integer(string="Living Area in (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Have Garage ?")
    garden = fields.Boolean(string="Have Garden ?")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    image = fields.Image("Image")
    date_availability = fields.Date(string="Available From",
                                    default=lambda self: fields.Date.today() + relativedelta(months=1))
    rented_date = fields.Date(string="Rented Date")
    rented_month = fields.Integer("No. of month")
    rented_till = fields.Date(string="Rented Till")
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
        ('offer_received', 'Offer Received'),
        ('reserved', 'Reserved'),
        ('rented', 'Rented'),
        ('returned', 'Returned')
    ], default='available', tracking=True)

    rental_duration = fields.Integer(string="Duration", default=2)
    weekly_rent = fields.Float(string="Weekly Rent(BDT)")
    monthly_rent = fields.Float(string="Monthly Rent(BDT)")
    yearly_rent = fields.Float(string="Yearly Rent(BDT)")

    property_type_ids = fields.Many2many('rental.property.type')
    property_tag_ids = fields.Many2many('rental.property.tag')
    offer_ids = fields.One2many('rental.offers', 'property_ids', string="Offers", tracking=True)
    offer_partner = fields.Many2one(related='offer_ids.partner_id', string="Offer Partner", readonly=True)
    current_user = fields.Many2one('res.users', compute='_get_current_user')
    print(current_user)
    offer_status = fields.Selection(related='offer_ids.status', string="Offer Status", readonly=True, store=True)

    offer_count = fields.Integer(compute='_compute_offer_counts')
    sales_man = fields.Many2one('res.users', default=lambda self: self.env.user.id, readonly=True)

    @api.depends()
    def _get_current_user(self):
        for rec in self:
            rec.current_user = self.env.user
        self.update({'current_user': self.env.user.id})

    @api.constrains('property_name')
    def check_property_name(self):
        for record in self:
            lst = self.search([]).mapped('property_name')
            print(lst)
            rec = lst[1:]
            print(rec)
            if record.property_name in rec:
                raise ValidationError("Property Name Must be Unique !")

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 50
            self.garden_orientation = 'south'
        else:
            self.garden_area = False
            self.garden_orientation = False

    @api.onchange('property_type_ids')
    def _prevent_multiple_property_type(self):
        for record in self:
            if len(record.property_type_ids) > 1:
                raise ValidationError("Multiple Property Type is not Allowed !")

    def property_offer_payment_confirm(self):
        for record in self:
            record.status = 'reserved'
            record.offer_status = ''
            record.sales_man.notify_success(title="Good News !",
                                             message=f'{record.offer_ids.partner_id} Has confirmed the payment !!',
                                             sticky=True)

    @api.constrains('offer_ids')
    def _compute_offer_counts(self):
        for record in self:
            print(record.status)
            record.offer_count = len(record.offer_ids)
            if record.offer_count > 0:
                print("========", record.status)
                self.status = 'offer_received'
            else:
                self.status = 'available'



