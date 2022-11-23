from datetime import date

from odoo.exceptions import ValidationError
from odoo import api, models, fields, _
from dateutil import relativedelta


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"

    name = fields.Char(string='Name', tracking=True)
    ref = fields.Char(string='Reference')
    date_of_birth = fields.Date(string='Date Of  Birth')
    age = fields.Integer(string='Age', compute='_compute_age', inverse='_inverse_compute_age',
                         search='_search_age', tracking=True, store=True)
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

    medicine_id = fields.One2many('medicine', 'patient_id_medicine', string='Medicine')
    is_birthday = fields.Boolean(string='Birthday ?', compute='_compute_is_birthday')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    website = fields.Char(string='Website')
    hole_total = fields.Float(string='Total', compute='_hole_total')

    def action_compute_bill(self):
        return

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        print('..............', self)
        appointment_group = self.env['hospital.appointment'].read_group(domain=[],
                                                                        fields=['patient_id'], groupby=['patient_id'])
        for appointment in appointment_group:
            patient_id = appointment.get('patient_id')
            if patient_id:
                patient_rec = self.browse(patient_id[0])
                patient_rec.appointment_count = appointment['patient_id_count']
                self -= patient_rec
        self.appointment_count = 0

    #
    # @api.depends('appointment_ids')
    # def _compute_appointment_count(self):
    #     for rec in self:
    #         rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

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

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

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

    def _search_age(self, operation, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday

    @api.depends('medicine_id')
    def _hole_total(self):
        for rec in self:
            total_discount = 0
            total_amount = 0
            if rec.medicine_id:
                for medicine in rec.medicine_id:
                    total_amount += medicine.total_amount
                    total_discount += medicine.discount
                    all_total_discount = (total_amount * total_discount) / 100
                    rec.hole_total = total_amount - all_total_discount
            else:
                rec.hole_total = total_amount

    def action_view_appointments(self):
        return {
            'name': _('Appointments'),
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            # 'context': {'default_patient_id': self.ids},
            'context': {'default_patient_id': self.id},
            'domain': [('patient_id', '=', self.ids)],
            'target': 'current',
            'type': 'ir.actions.act_window',
            # 'view_id': self.env.ref('base.view_translation_dialog_tree').id,
            # 'flags': {'search_view': True, 'action_buttons': True},
        }


class Medicine(models.Model):
    _name = "medicine"
    _description = "Medicine"

    medicine_name = fields.Char(string="Name")
    amount = fields.Float(string='Amount')
    quantity = fields.Float(string="Quantity")
    total_amount = fields.Float(string='Total Amount', compute='calculate_total_amount')
    discount = fields.Float(string='Discount %')
    # amount_total = fields.Integer(string='Total', store=True, compute='_amount_all')
    patient_id_medicine = fields.Many2one('hospital.patient', string='Patient')

    @api.depends('amount', 'quantity')
    def calculate_total_amount(self):
        for rec in self:
            rec.total_amount = rec.amount * rec.quantity

    # @api.depends('amount', 'quantity', 'discount')
    # def _calculate_amount(self):
    #     for rec in self:
    #         if rec.quantity > 0:
    #             total = rec.amount * rec.quantity
    #             total_discount = (total * rec.discount) / 100
    #             rec.total_amount = total - total_discount
    #         else:
    #             rec.total_amount = 1

    # total_discount = (total_amount * discount) / 100

    # (amount * qty) - (amount * discount / 100)
    # @api.depends('total_amount')
    # def _amount_all(self):
    #     for rec in self:
    #         rec.amount_total += rec.total_amount
