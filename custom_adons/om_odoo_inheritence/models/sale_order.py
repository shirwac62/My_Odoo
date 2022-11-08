# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user_id = fields.Many2one('res.users', 'Confirmed User')

    def action_confirm(self):
        print('Success..............................')
        self.confirmed_user_id = self.env.user.id

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ref = fields.Char("REF")

    def action_confirm(self):
        print('Success..............................')
        self.ref = self.name
#