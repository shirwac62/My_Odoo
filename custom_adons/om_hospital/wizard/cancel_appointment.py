import datetime
from odoo import fields, models, api


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['date'] = datetime.date.today()
        return res

    appointment_id = fields.Many2one('hospital.appointment', 'Appointment')
    reason = fields.Text(string="Reason")
    date = fields.Date(string='Cancellation Date')

    def action_cancel(self):
        return
