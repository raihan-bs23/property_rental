from dateutil.relativedelta import relativedelta
from odoo import fields, models, tools, http, api
from odoo.exceptions import ValidationError

class InheritedModel(models.Model):
    _inherit = 'res.users'




