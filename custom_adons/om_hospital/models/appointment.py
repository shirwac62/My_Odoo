import random
from datetime import datetime
from dateutil import relativedelta

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'patient_id'
    _order = 'id desc'

    patient_id = fields.Many2one('hospital.patient', string='Patient', ondelete='restrict')
    gender = fields.Selection(related='patient_id.gender')
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    ref = fields.Char(string='Reference', related='patient_id.ref')
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string='Priority')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], default="draft", string='state', required=True)
    doctor_id = fields.Many2one('res.users', string='Doctor', tracking=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.line', 'appointment_id', string='Pharmacy Line')
    hide_sales_price = fields.Boolean(string='Hide Sales Price')
    operation_id = fields.Many2one('hospital.operation', string='Operation')
    progress = fields.Integer(string='Progress', compute='_compute_progress')

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    float_total = fields.Float(string='Total Float')
    monetary_total = fields.Monetary(string='Total Monetary')

    assignment_total = fields.Float(string='Total')
    refund = fields.Integer(string='Refund')

    def action_send_mail(self):
        template = self.env.ref('om_hospital.appointment_mail_template')
        for rec in self:
            if rec.patient_id.email:
                email_values = {'subject': 'The Test one'}
                template.send_mail(rec.id, force_send=True)

    def action_share_whatsapp(self):
        if not self.patient_id.phone:
            raise ValidationError(_('Missing Phone Number In This Patient Record'))
        message = 'Hi %s' % self.patient_id.name
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone, message)
        self.message_post(body=message, subject='WhatsApp Message')
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url
        }

    def action_notification(self):
        action = self.env.ref('om_hospital.action_hospital_patient')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': '%s',
                'links': [{
                    'label': self.patient_id.name,
                    'url': f'#action{action.id}&id={self.patient_id.id}&model=hospital.patient'
                }],
                'type': 'success',
                'sticky': False,
                'next': {
                    'type': 'ir.actions.act_window',
                    'res_model': 'hospital.patient',
                    'res_id': self.patient_id.id,
                    'views': [(False, 'form')]
                }
            }
        }

    def set_line_number(self):
        sl_no = 0
        for line in self.pharmacy_line_ids:
            sl_no += 1
            line.sl_no = sl_no
        return

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        res = super(HospitalAppointment, self).create(vals)
        res.set_line_number()
        return res

    def write(self, vals):
        res = super(HospitalAppointment, self).write(vals)
        self.set_line_number()
        return res

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(_('You Can only Delete The appointment With Draft status'))
        return super(HospitalAppointment, self).unlink()

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    # return {
    #     'effect': {
    #         'fadeout': 'slow',
    #         'message': 'click successful',
    #         'type': 'rainbow_man'
    #     }
    # }
    def object_button(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': 'https://www.odoo.com'
        }

    # def action_first(self):
    #     for rec in self:
    #         rec.state = 'one'
    #
    # def action_second(self):
    #     for rec in self:
    #         rec.state = 'two'
    #
    # def action_third(self):
    #     for rec in self:
    #         rec.state = 'three'
    #
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = random.randrange(0, 25)
            elif rec.state == 'in_consultation':
                progress = random.randrange(25, 99)
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.line"
    _description = "Appointment Pharmacy Line"

    sl_no = fields.Integer(string='SNO')
    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(related='product_id.list_price', digits='Product Price')
    qty = fields.Integer(string='Quantity', default=1)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    company_currency_id = fields.Many2one('res.currency', related='appointment_id.currency_id')
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_price_subtotal',
                                     currency_field='company_currency_id')

    @api.depends('price_unit', 'qty')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty
