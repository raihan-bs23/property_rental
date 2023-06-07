from dateutil.relativedelta import relativedelta
from odoo import fields, models, tools, http, api
from odoo.exceptions import ValidationError


class RentalPropertyOffers(models.Model):
    _name = 'rental.offers'
    _description = "This is Rental Property Offer Description"
    _order = 'price desc'
    _rec_name = 'property_ids'

    price = fields.Float(default=0.0, string="Offered Price")
    status = fields.Selection(string="Offer Status", selection=[
        ('accepted', 'Accepted'),
        ('wishlist', 'Wishlist'),
        ('refused', 'Refused')
    ], readonly=True)
    partner_id = fields.Many2one('res.users', string="Offer By", required=True, readonly=True,
                                 default=lambda self: self.env.user.id)
    property_ids = fields.Many2one('property.details')
    rental_type = fields.Selection(string="Rental Type", selection=[
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ], default='monthly')
    rental_duration = fields.Integer(string="Duration", default=2)
    weekly_rent = fields.Float(compute='_compute_rent', string="Weekly Rent(BDT)", store=True)
    monthly_rent = fields.Float(compute='_compute_rent', string="Monthly Rent(BDT)", store=True)
    yearly_rent = fields.Float(compute='_compute_rent', string="Yearly Rent(BDT)", store=True)
    total_expected_rent = fields.Float(string="Total Expected Rent", compute='_compute_rent', store=True)
    validity = fields.Integer(default=7, string="Offer Validity Days", store=True)
    date_deadline = fields.Date(compute='_compute_date_validity', inverse='_inverse_date_deadline',
                                string="Offer Deadline", store=True)

    @api.depends('property_ids.weekly_rent', 'property_ids.monthly_rent', 'property_ids.yearly_rent', 'rental_type',
                 'rental_duration', 'total_expected_rent')
    def _compute_rent(self):
        for record in self:
            record.weekly_rent = record.property_ids.weekly_rent
            record.monthly_rent = record.property_ids.monthly_rent
            record.yearly_rent = record.property_ids.yearly_rent
            if record.rental_type == 'weekly':
                # record.rental_duration = 8
                record.total_expected_rent = record.rental_duration * record.weekly_rent
            elif record.rental_type == 'monthly':
                # record.rental_duration = 2
                record.total_expected_rent = record.rental_duration * record.monthly_rent
            elif record.rental_type == 'yearly':
                # record.rental_duration = 1
                record.total_expected_rent = record.rental_duration * record.yearly_rent
            else:
                record.total_expected_rent = 0.0

    @api.depends('validity', 'create_date')
    def _compute_date_validity(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(self.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_validation(self):
        for record in self:
            if record.date_deadline:
                record.validity = fields.Date.add(days=record.date_deadline - record.create_date)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                create_date = fields.Datetime.from_string(record.create_date)
                deadline = fields.Datetime.from_string(record.date_deadline)
                validity = (deadline - create_date).days + 1
                if validity >= 0:
                    record.validity = validity

    def property_offer_status_accept(self):
        for record in self:
            record.status = "accepted"
            record.partner_id.notify_success(title="Congratulations !",
                                             message=f'Your Offers has been Accepted for {record.property_ids.property_name} Property !!',
                                             sticky=True)

    def property_offer_status_refuse(self):
        for record in self:
            record.status = "refused"
            record.partner_id.notify_warning(title="Opps !",
                                             message=f'Your Offers has been Refused for {record.property_ids.property_name} Property!!',
                                             sticky=True)

    def property_offer_status_wishlist(self):
        for record in self:
            record.status = "wishlist"
            record.partner_id.notify_info(title="Have a Relax!",
                                             message=f'Your Offer has been wish listed for {record.property_ids.property_name} Property!!',
                                             sticky=True)

    @api.onchange('price')
    def _check_offered_price(self):
        for record in self:
            if record.price < 0:
                raise ValidationError("Offered price must be a positive value !")

    @api.onchange('rental_duration', 'rental_type')
    def _check_rental_duration(self):
        for record in self:
            if record.rental_type == 'weekly' and record.rental_duration < 8:
                raise ValidationError("Rental Duration should be at least 8 week!")
            elif record.rental_type == 'monthly' and record.rental_duration < 2:
                raise ValidationError("Rental Duration should be at least 2 month!")
            elif record.rental_type == 'yearly' and record.rental_duration < 1:
                raise ValidationError('Rental Duration should not be less than 1 year !')

    # @api.model
    # def create(self, vals):
    #     existing_offers = self.search([('property_ids', '=', vals['property_ids'])])
    #     if existing_offers and vals['price'] <= max(existing_offers.mapped('price')):
    #         raise ValidationError("Offered price can't be equal or lower than an existing offer!")
    #     return super(RentalPropertyOffers, self).create(vals)
