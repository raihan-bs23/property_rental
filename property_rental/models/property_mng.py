from dateutil.relativedelta import relativedelta
from odoo import fields, models, tools, api
from odoo.exceptions import UserError, ValidationError

from src.odoo.odoo.fields import Date


class PropertyDetails(models.Model):
    _name = 'property.details'
    _description = 'This Module includes the property details and business logic related to property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'property_name'
    _order = 'id desc'

    property_name = fields.Char(string="Property Name", required=True, tracking=True)
    property_description = fields.Text(string="Property Description")
    postcode = fields.Char(string="Postcode", required=True)
    address = fields.Text(string="Address", required=True)
    bedrooms = fields.Integer(string="No. of Bedrooms", default=3)
    living_area = fields.Integer(string="Living Area in (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Have Garage ?")
    garden = fields.Boolean(string="Have Garden ?")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    image = fields.Image("Image", required=True)
    date_availability = fields.Date(string="Available From",
                                    default=lambda self: fields.Date.today() + relativedelta(months=1))

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
        ('rented', 'Rented')
    ], default='available', tracking=True)
    offer_ids = fields.One2many('rental.offers', 'property_ids', string="Rental Offers")

    # Rental Infornation
    rental_duration = fields.Integer(related='offer_ids.rental_duration', string="Rental Duration")
    weekly_rent = fields.Float(string="Weekly Rent(BDT)", required=True)
    monthly_rent = fields.Float(string="Monthly Rent(BDT)", required=True)
    yearly_rent = fields.Float(string="Yearly Rent(BDT)", required=True)
    rented_price = fields.Float(related='offer_ids.price', string="Rented Price", readonly=True)
    rented_date = fields.Date(string="Rent Date", default=lambda self: fields.Date.today())
    rented_till = fields.Date(string="Rented Till", compute='')

    property_type_ids = fields.Many2many('rental.property.type')
    property_tag_ids = fields.Many2many('rental.property.tag')

    tenant_property_ids = fields.One2many('res.users', 'rented_property_ids', string="Rented Property")
    offer_partner = fields.Many2one(related='offer_ids.partner_id', string="Offer Partner", readonly=True)
    current_user = fields.Many2one('res.users', compute='_get_current_user')
    offer_status = fields.Selection(related='offer_ids.status', string="Offer Status", readonly=True, store=True)
    renter = fields.Char(string="Property Renter")

    offer_count = fields.Integer(compute='_compute_offer_counts')
    sales_man = fields.Many2one('res.users', default=lambda self: self.env.user.id, readonly=True)
    invoice_sent = fields.Boolean("Invoice Status", default=False)
    invoice_count = fields.Integer(string="Invoice Count", compute='_get_invoiced')

    def offer_partner_test(self):
        for rec in self:
            print("Offer Partner", rec.offer_partner)

    @api.depends('rental_duration', 'rented_date')
    def _compute_rent_till_date(self):
        for record in self:
            record.rented_till = record.rented_date + relativedelta(months=record.rental_duration)
            print("Rented Till", record.rented_till)

    @api.depends()
    def _get_current_user(self):
        for rec in self:
            rec.current_user = self.env.user
        self.update({'current_user': self.env.user.id})

    @api.constrains('property_name')
    def check_property_name(self):
        for record in self:
            lst = self.search([]).mapped('property_name')
            rec = lst
            rec.remove(self.property_name)
            print(rec)
            print(self.property_name)
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

    @api.constrains('offer_ids', 'offer_count', 'move_id.payment_state')
    def _compute_offer_counts(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
            if record.offer_count == 0:
                record.status = 'available'
                record.renter = ''
                record.move_id.payment_state = 'not_paid'
                record.invoice_sent = False
            elif record.status == 'available' and record.offer_count > 0:
                record.status = 'offer_received'
            elif record.status == 'offer_received' or record.status == 'available':
                record.renter = ''

    def property_rent_confirm(self):
        for record in self:
            if record.current_user == record.sales_man:
                record.rented_till = Date.today() + relativedelta(months=record.rental_duration)
                record.status = 'rented'
                form_view_id = self.env.ref('property_rental.confirm_rent_to_tenant_form').id
                action = {
                    'type': 'ir.actions.act_window',
                    'name': 'Confirm Rent',
                    'view_mode': 'form',
                    'res_model': 'property.details',
                    'view_id': form_view_id,
                    'res_id': self.id,
                    'target': 'new',
                }
                return action
            else:
                raise ValidationError("You are not allowed to do this !!")

    def send_invoice(self):
        for record in self:
            if not record.invoice_sent:
                record.invoice_sent = True
                record.offer_partner.notify_success(title="Invoice Created !",
                                                    message=f'A new Invoice has been craeted for {record.property_name} Property !!',
                                                    sticky=True)

    @api.constrains('move_id')
    def property_offer_payment_confirm(self):
        for record in self:
            if record.move_id.payment_state == 'paid':
                if record.current_user == record.offer_partner:
                    record.status = 'reserved'
                    record.renter = record.current_user.name
                    record.offer_status = ''
                    record.sales_man.notify_success(title="Good News!",
                                                    message=f'{record.offer_partner.name} has confirmed the payment!!',
                                                    sticky=True)
            elif record.move_id.payment_state == 'not_paid' and record.offer_count > 0:
                record.status = 'offer_received'

    def _get_invoiced(self):
        for order in self:
            invoices = order.move_id.filtered(
                lambda r: r.move_type in ('out_invoice', 'out_refund'))
            order.move_id = invoices
            order.invoice_count = len(invoices)

    def get_view_invoice(self):
        invoices = self.mapped('move_id')
        action = self.env['ir.actions.actions']._for_xml_id('account.action_move_out_invoice_type')
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            'default_move_type': 'out_invoice',
        }
        if len(self) == 1:
            context.update({
                'default_partner_id': self.offer_partner.id,
            })
        action['context'] = context
        return action
