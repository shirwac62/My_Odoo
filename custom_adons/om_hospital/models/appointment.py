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
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.line', 'appointment_id', string='Pharmacy Line')
    hide_sales_price = fields.Boolean(string='Hide Sales Price')

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


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.line"
    _description = "Appointment Pharmacy Line"

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(related='product_id.list_price')
    qty = fields.Integer(string='Quantity', default=1)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
