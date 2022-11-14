from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")
    sequence = fields.Integer(string='Sequence')

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)", self.name)
        default['sequence'] = 10
        return super(PatientTag, self).copy(default)

    @api.constrains('name')
    def _check_name_unique(self):
        name_counts = self.search_count([('name', '=', self.name), ('id', '!=', self.id)])
        if name_counts > 0:
            raise ValidationError("Name already exists!")

    # _sql_constraints = [
    #     ('unique_tag_name', 'unique (name, active)', 'Name Must Be Unique.'),
    #     ('check_sequence', 'check (sequence > 0)', 'Sequence Must Be Greater than Zero Or Positive Number'),
    # ]
