from dateutil.relativedelta import relativedelta
from odoo import fields, models, tools

from src.odoo.odoo import api
from src.odoo.odoo.exceptions import ValidationError


class RealEstatePropertyOffers(models.Model):
    _name = 'estate.property.offers'
    _description = "This is Real Estate Property Offer Description"

    price = fields.Float(default=0.0, string="Offered Price")
    status = fields.Selection(string="Offer Status", selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False, readonly=True)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_ids = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7, string="Validity Days", store=True)
    date_deadline = fields.Date(compute='_compute_date_validity', inverse='_inverse_date_deadline',
                                string="Offer Deadline", store=True)

    # _sql_constraints = [
    #     ('check_offered_price', 'CHECK(price > 0)', 'Offered Price must be Positive !')
    # ]

    @api.depends('validity', 'create_date')
    def _compute_date_validity(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.from_string(record.create_date) + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    # def _inverse_date_validation(self):
    #     for record in self:
    #         if record.date_deadline:
    #             record.validity = fields.Date.to_string(record.date_deadline - record.create_date)

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
            exp = record.property_ids.expected_price * .9
            if record.price < exp:
                raise ValidationError("Selling Price Cannot be less than 90% of expected price ")
            else:
                record.status = "accepted"
                record.property_ids.selling_price = record.price
                record.property_ids.buyer_id = record.partner_id


    def property_offer_status_refuse(self):
        for record in self:
            record.status = "refused"
            record.property_ids.selling_price = 0.0
            record.property_ids.buyer_id = None

    @api.constrains('price')
    def _check_offered_price(self):
        for record in self:
            if record.price < 0:
                raise ValidationError("Offered price must be a positive value !")

    # @api.constrains('price')
    # def _check_offered_price(self):
    #     for record in self:

