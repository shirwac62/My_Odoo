from datetime import datetime
from dateutil import relativedelta

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['date'] = datetime.today()
        res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one('hospital.appointment', 'Appointment',
                                     domain=[('state', '=', 'draft'), ('priority', 'in', ('0', '1', False))])
    reason = fields.Text(string="Reason")
    date = fields.Date(string='Cancellation Date')

    def action_cancel(self):
        cancel_day = self.env['ir.config_parameter'].get_param('om_hospital.cancel_day')
        allow_date = self.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_day))

        if self.appointment_id.booking_date == fields.date.today():
            raise ValidationError(_("Sorry Cancellation is not allowed on the same day of booking data !"))
        # self.appointment_id.state = 'cancel'


        query = """select name from hospital_patient"""
        self.env.cr.execute(query)
        patients = self.env.cr.fetchall()
        print('patients=======> ', patients)



        # day1 = self.appointment_id.appointment_time - datetime.datetime.now()


        # datem = datetime.datetime.strptime(str(day1), "%d %H:%M:%S.%f")
        # print(datem.hour)  # 11

        # print('day1:  ', day1.seconds)
        #
        # div_hours = (day1.days * 24) + (day1.seconds / 3600)
        # print('div_hours=========> ', div_hours)
        #
        # amount = self.appointment_id.assignment_total
        # print('amount   :', amount)
        # # percentage1 = amount/75 * self.appointment_id.assignment_total
        # percentage1 = 75 / 100 * amount
        # print('percentage1 :', percentage1)
        # print('Type Of day 1 :', type(day1))
        # percentage2 = 50 / 100 * amount
        # percentage3 = 25 / 100 * amount

        # if div_hours == 72:
        #     self.appointment_id.refund = percentage3
        # elif div_hours == 48:
        #     self.appointment_id.refund = percentage2
        # elif div_hours == 24:
        #     self.appointment_id.refund = percentage1
        # else:
        #     self.appointment_id.refund = 0
        # return

        # if allow_date < datetime.date.today():
        #     raise ValidationError(_("Sorry Cancellation is not allowed For this Booking!"))
        # self.appointment_id.state = 'cancel'

        # return {
        #     'type': 'ir.actions.client',
        #     'view_mode': 'form',
        #     'res_model': 'cancel.appointment.wizard',
        #     'target': 'new',
        #     'res_id': self.id,
        # }

        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }
    # if self.appointment_id.booking_date == fields.date.today():
    #     raise ValidationError(_("Sorry Cancellation is not allowed on the same day of booking data !"))
    # self.appointment_id.state = 'cancel'
    # return
