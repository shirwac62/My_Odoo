import datetime

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['date'] = datetime.date.today()
        res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one('hospital.appointment', 'Appointment',
                                     domain=[('state', '=', 'draft'), ('priority', 'in', ('0', '1', False))])
    reason = fields.Text(string="Reason")
    date = fields.Date(string='Cancellation Date')

    def action_cancel(self):
        if self.appointment_id.booking_date == fields.date.today():
            raise ValidationError(_("Sorry Cancellation is not allowed on the same day of booking data !"))
        self.appointment_id.state = 'cancel'
        return
