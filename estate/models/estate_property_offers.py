from dateutil.relativedelta import relativedelta
from odoo import fields, models, tools, http, api
from odoo.exceptions import ValidationError


class RealEstatePropertyOffers(models.Model):
    _name = 'estate.property.offers'
    _description = "This is Real Estate Property Offer Description"
    _order = 'price desc'
    _rec_name = ''

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
    property_type_id = fields.Many2one(related='property_ids.property_type_id', string="Property Type", store=True)

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
            record.property_ids.status = "offer_accepted"
            record.property_ids.selling_price = record.price
            record.property_ids.buyer_id = record.partner_id

    def property_offer_status_refuse(self):
        for record in self:
            record.status = "refused"

    @api.onchange('price')
    def _check_offered_price(self):
        for record in self:
            if record.price < 0:
                raise ValidationError("Offered price must be a positive value !")

    @api.model
    def create(self, vals):
        existing_offers = self.search([('property_ids', '=', vals['property_ids'])])
        if existing_offers and vals['price'] <= max(existing_offers.mapped('price')):
            raise ValidationError("Offered price can't be equal or lower than an existing offer!")
        return super(RealEstatePropertyOffers, self).create(vals)
