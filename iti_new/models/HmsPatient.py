from odoo import models, fields,api
from datetime import date
from odoo.exceptions import ValidationError

class HmsPatient(models.Model):
    _name = 'hms.patient'
    _rec_name="first_name"
    _description = 'HMS Patient'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birthdate = fields.Date(string='Birthdate')
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ], string='Blood Type')
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary(string='Image')
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age',compute='_compute_age',store=True)
    email = fields.Char(string='Email', required=True)
    department_id = fields.Many2one(comodel_name="hms.department", string="Department")
    department_capacity = fields.Integer(string="Department Capacity", related="department_id.capacity")
    doctor_ids = fields.Many2many(comodel_name="hms.doctor")
    customer_id = fields.Many2one('res.partner', string='Related Customer', ondelete='restrict')

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], string="State", default='undetermined')
    log_history_ids = fields.One2many('hms.patient.log', 'patient_id', string='Log History')
    
    @api.depends('birthdate')
    def _compute_age(self):
        for rec in self:
            if rec.birthdate:
                today = date.today()
                rec.age = today.year - rec.birthdate.year - (
                (today.month, today.day) < (rec.birthdate.month, rec.birthdate.day))
            else:
                rec.age = 0


    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                "warning": {
                    "title": "Warning",
                    "message": "PCR is checked by default for patients with age less than 30",
                }
            }

    @api.onchange('history')
    def _onchange_history(self):
        if self.history:
            vals = {
                'description': 'History changed to %s' % (self.history),
                'patient_id': self.id
            }
            self.env['hms.patient.log'].create(vals)


    @api.constrains('email')
    def _check_valid_email(self):
        for record in self:
            if record.email:
                email_parts = record.email.split('@')
                if len(email_parts) != 2 or '.' not in email_parts[1] or email_parts[1].find('.') < 1:
                    raise ValidationError("Please enter a valid email address.")
                existing_patient = self.search([('email', '=', record.email), ('id', '!=', record.id)])
                if existing_patient:
                    raise ValidationError("Email address must be unique.")

    def change_state(self):
        if self.state == "undetermined":
            self.state = "good"
        elif self.state == "good":
            self.state = "fair"
        elif self.state == "fair":
            self.state = "serious"
        else:
            self.state = "undetermined"

