from odoo import fields, models, tools

class UserInfo(models.Model):
    _name = "user.info"
    _description = "User Information"

    name = fields.Char('User full Name', required=True, translate=True)
    contact = fields.Integer('contact', required=True)
    email = fields.Char('email', required=True)
    address = fields.Char("Address", required = True)
    joined_date = fields.Date()

