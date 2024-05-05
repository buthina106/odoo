from odoo import models, fields,api

class HmsPatientLog(models.Model):
    _name = 'hms.patient.log'

    description = fields.Text(string='Description')
    patient_id = fields.Many2one('hms.patient', string='Patient')