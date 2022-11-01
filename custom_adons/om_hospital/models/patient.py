from datetime import date

from odoo import api, models, fields


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"

    name = fields.Char(string='Name', tracking=True)
    ref = fields.Char(string='Reference')
    date_of_birth = fields.Date(string='Date Of  Birth')
    age = fields.Integer(string='Age', compute='_compute_age', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True)
    active = fields.Boolean(string="Active", default=True)
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', 'Tags')

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    # @api.onchange('gender')
    # def onchange_age(self):
    #     if self.gender == 'male':
    #         self.age = 0
