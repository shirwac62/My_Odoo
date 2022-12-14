from odoo import fields, models, api


class Lead(models.Model):
    _inherit = 'crm.lead'

    company_type = fields.Selection(string='Company Type',
                                    selection=[('person', 'Individual'), ('company', 'Company')],
                                    compute='_compute_company_type', inverse='_write_company_type', default='person')

    is_company = fields.Boolean(string='Is a Company', default=False,
                                help="Check if the contact is a company, otherwise it is a person")

    @api.depends('is_company')
    def _compute_company_type(self):
        for partner in self:
            partner.company_type = 'company' if partner.is_company else 'person'


class CustomerInfo(models.Model):
    _inherit = 'crm.lead'

    commercial_reg = fields.Binary(string='Commercial Registration', attachment=False)
    business_license = fields.Binary(string='Business License', attachment=False)
    passport = fields.Binary(string='Passport', attachment=False)
    article_of_association = fields.Binary(string='Article of Association', attachment=False)
    mou = fields.Binary(string='MOU', attachment=False)
    minutes = fields.Binary(string='Minutes', attachment=False)
    resolution_latter = fields.Binary(string='Resolution Latter', attachment=False)


    def _write_company_type(self):
        for partner in self:
            partner.is_company = partner.company_type == 'company'
