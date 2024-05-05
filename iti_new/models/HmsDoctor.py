from odoo import models, fields

class HmsDoctor(models.Model):
    _name = 'hms.doctor'
    _rec_name = "first_name"
    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    image = fields.Binary(string='Image')
