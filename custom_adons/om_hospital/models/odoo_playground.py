from odoo import models, fields


class OdooPlayGround(models.Model):
    _name = "odoo.playground"
    _description = "Odoo PlayGround"

    model_id = fields.Many2one('ir.model', string='Model')
    name = fields.Char(string='Name', tracking=True)
    ref = fields.Char(string='Reference')

    def action_execute(self):
        # Create ORM Method
        # print(self.env['hospital.patient'].create({'name': 'ORM Methods'}))

        # Browse ORM Method
        # print(self.env['hospital.patient'].browse(1).email)

        # Write ORM Method
        # print(self.env['hospital.patient'].browse(36).write({'name': 'Updated Name'}))

        # Unlink ORM Method
        # print(self.env['hospital.patient'].browse(36).unlink())

        # Search ORM Method
        # print(self.env['hospital.patient'].search([('gender', '=', 'male')], order='id desc'))

        # Search Count ORM Method
        # print(self.env['hospital.patient'].search([('gender', '=', 'male')], order='id desc', count=True))

        # Get Metadata ORM Method
        # print(self.env['patient.tag'].browse(34).get_metadata()[0].get('xmlid'))

        # Fields Get ORM Method
        print(self.env['hospital.patient'].fields_get(['name', 'gender'], ['type', 'string']))
