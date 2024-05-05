from odoo import models, fields,api
from odoo.exceptions import ValidationError

class CrmCustomer(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='Related Patient',unique=True)

    vat=fields.Char(required=True)
    email=fields.Char(unique=True)


    @api.constrains('related_patient_id')
    def _check_unique_related_patient(self):
        for customer in self:
            if customer.related_patient_id:
                existing_customer = self.search([
                    ('related_patient_id', '=', customer.related_patient_id.id),
                    ('id', '!=', customer.id)
                ], limit=1)
                if existing_customer:
                    raise ValidationError("Each customer can have only one related patient.")