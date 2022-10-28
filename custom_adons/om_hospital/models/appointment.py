from odoo import api, models, fields


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    gender = fields.Selection(related='patient_id.gender')
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    ref = fields.Char(string='Reference')
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string='Priority')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], default="draft", string='Status', required=True)
    doctor_id = fields.Many2one('res.users', string='Doctor', tracking=True)

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def object_button(self):
        print("Button Clicked")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'click successful',
                'type': 'rainbow_man'
            }
        }

    def action_cancel(self):
        for rec in self:
            rec.status = 'cancel'

    def action_in_consultation(self):
        for rec in self:
            rec.status = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.status = 'done'
