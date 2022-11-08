from odoo import models, fields


class OdooPlayGround(models.Model):
    _name = "odoo.playground"
    _description = "Odoo PlayGround"

    model_id = fields.Many2one('ir.model',  string='Model')
    name = fields.Char(string='Name', tracking=True)
    ref = fields.Char(string='Reference')
