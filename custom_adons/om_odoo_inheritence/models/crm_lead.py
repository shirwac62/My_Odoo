from odoo import fields, models, api


class Lead(models.Model):
    _inherit = 'crm.lead'

    company_type = fields.Selection(string='Company Type',
                                    selection=[('person', 'Individual'), ('company', 'Company')],
                                    compute='_compute_company_type', inverse='_write_company_type', default='person')

    is_company = fields.Boolean(string='Is a Company', default=False,
                                help="Check if the contact is a company, otherwise it is a person")
    # user_id = fields.Many2one(
    #     'res.users', string='Agent', default=lambda self: self.env.user,
    #     domain="['&', ('share', '=', False), ('company_ids', 'in', user_company_ids)]",
    #     check_company=True, index=True, tracking=True)

    commercial_reg = fields.Binary(string='Commercial Registration', attachment=False, required=True)
    business_license = fields.Binary(string='Business License', attachment=False, required=True)
    passport = fields.Binary(string='Passport', attachment=False, required=True)
    article_of_association = fields.Binary(string='Article of Association', attachment=False, required=True)
    mou = fields.Binary(string='MOU', attachment=False, required=True)
    minutes = fields.Binary(string='Minutes', attachment=False, required=True)
    resolution_latter = fields.Binary(string='Resolution Latter', attachment=False, required=True)

    @api.depends('is_company')
    def _compute_company_type(self):
        for partner in self:
            partner.company_type = 'company' if partner.is_company else 'person'

# class CustomerInfo(models.Model):
#     _inherit = 'crm.lead'
#
#     commercial_reg = fields.Binary(string='Commercial Registration', attachment=False, required=True)
#     business_license = fields.Binary(string='Business License', attachment=False, required=True)
#     passport = fields.Binary(string='Passport', attachment=False, required=True)
#     article_of_association = fields.Binary(string='Article of Association', attachment=False, required=True)
#     mou = fields.Binary(string='MOU', attachment=False, required=True)
#     minutes = fields.Binary(string='Minutes', attachment=False, required=True)
#     resolution_latter = fields.Binary(string='Resolution Latter', attachment=False, required=True)


    def _write_company_type(self):
        for partner in self:
            partner.is_company = partner.company_type == 'company'
