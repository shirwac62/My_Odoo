from datetime import date

from odoo.exceptions import ValidationError
from odoo import api, models, fields, _


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"

    name = fields.Char(string='Name', tracking=True)
    ref = fields.Char(string='Reference')
    date_of_birth = fields.Date(string='Date Of  Birth')
    age = fields.Integer(string='Age', compute='_compute_age', tracking=True, store=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True)
    active = fields.Boolean(string="Active", default=True)
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string='Tags')
    # appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointment')
    parent = fields.Char(string='Parent')
    martial_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string='Martial Status',
                                      tracking=True)
    partner_name = fields.Char(string='Partner Name')

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("You Can not Delete A patient with Appointments !"))

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth > fields.date.today():
                raise ValidationError(_('The Entered date Is not Acceptable '))

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        print('vals =========', vals)
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    def name_get(self):
        patient_list = []
        for record in self:
            name = record.name + '--' + record.ref
            patient_list.append((record.id, name))

        return patient_list

    def action_test(self):
        print('Click')
        return

    # @api.onchange('gender')
    # def onchange_age(self):
    #     if self.gender == 'male':
    #         self.age = 0
