from odoo import fields, models, api, _
from odoo.exceptions import Warning, UserError, ValidationError 

CALC_TYPE = [
    ('0', 'Saldos Insolutos'),
    ('1', 'Solo Interes'),
    ('2', 'Saldos Morosos'),
    ('3', 'Saldos Puntuales'),
]

class ExtenssProductCreditType(models.Model):
    _name = 'extenss.product.credit_type'
    _order = 'name'
    _description = 'Credit Type'

    name = fields.Char(string='Credit Type',  translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)

class ExtenssProductCalculationBase(models.Model):
    _name = 'extenss.product.calculation_base'
    _orde = 'name'
    _description = 'Calculation Base'
    
    name = fields.Char(string='Calculation Base',  translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)
class ExtenssProductBaseInterestRate(models.Model):
    _name = 'extenss.product.base_interest_rate'
    _orde = 'name'
    _description = 'Base Interest Rate'
    
    name = fields.Char(string='Base Interest Rate',  translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)

class ExtenssProductInterestRate(models.Model):
    _name = 'extenss.product.interest_rate'
    _description = 'multiples registros interest rate'

    @api.constrains('initial_term', 'final_term', 'cat')   
    def _check_intrat(self):
        for intrat in self: 
            if intrat.initial_term <= 0:
                raise ValidationError(_('The Internal Term must be greater than 0'))
            if final_term  <= 0:
                raise ValidationError(_('The Final Term at must be greater than 0'))
            if cat  <= 0:
                raise ValidationError(_('The Cat at must be greater than 0'))

    interest_rate_id = fields.Many2one('product.template')
    initial_term = fields.Integer('Initial item',  translate=True)
    final_term = fields.Integer('Final item',  translate=True)
    interest_rate_2 = fields.Float('Rate',  translate=True)
    cat = fields.Float('Cat',  translate=True)
    frequencies_ir = fields.Many2one('extenss.product.frequencies', string="Frequencies")
class ExtenssFrequencies(models.Model):
    _name = "extenss.product.frequencies"
    _description = "Frequencies"

    name = fields.Char('Frequency')
    sequence = fields.Integer('sequence', help="Sequence for the handle.")

class Product(models.Model):
    _inherit = 'product.template'

    @api.constrains('min_age', 'max_age', 'min_amount', 'max_amount')   
    def _check_fields(self):
        for product in self:
            if product.min_age <=0:
                raise ValidationError(_('The Min. Age must be greater than 0'))
            if product.max_age <=0:
                raise ValidationError(_('The Max. Age must be greater than 0'))
            if product.min_age >= product.max_age:
                raise ValidationError(_('The Min. Age must be less than The Max. Age'))
            if product.min_amount <= 0:
                raise ValidationError(_('The Min. Amount must be greater than 0'))
            if product.max_amount <= 0:
                raise ValidationError(_('The Max. Amount must be greater than 0'))
            if product.min_amount >= product.max_amount:
                raise ValidationError(_('The Min. Amount must be less than The Max. Amount'))

    credit_type = fields.Many2one('extenss.product.credit_type')
    calculation_base = fields.Many2one('extenss.product.calculation_base')
    base_interest_rate = fields.Many2one('extenss.product.base_interest_rate')
    point_base_interest_rate = fields.Float('Points of Base Interest Rate', translate=True)
    include_taxes = fields.Boolean('Include Taxes', default=False,  translate=True)
    min_age = fields.Integer('Min. Age', translate=True)
    max_age = fields.Integer('Max. Age',  translate=True)
    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    min_amount = fields.Monetary('Min. Amount',  currency_field='company_currency', tracking=True)
    max_amount = fields.Monetary('Max. Amount',  currency_field='company_currency', tracking=True)
    apply_company = fields.Boolean('Apply Compnay', default=False,  translate=True)
    apply_person = fields.Boolean('Apply Person', default=False,  translate=True)
    endorsement = fields.Boolean('Requires Endorsement', default=False,  translate=True)
    obligated_solidary = fields.Boolean('Requires Obligated solidary', default=False,  translate=True)
    guarantee = fields.Boolean('Requires Warranty', default=False,  translate=True)
    socioeconomic_study = fields.Boolean('Socio-economic study', default=False,  translate=True)
    sic_consult = fields.Boolean('SIC Query', default=False,  translate=True)
    beneficiaries = fields.Boolean('Beneficiaries', default=False,  translate=True)
    patrimonial_relationship = fields.Boolean('Patrimonial Declaration', default=False,  translate=True)
    financial_situation = fields.Boolean('Business information', default=False,  translate=True)
    calculation_type = fields.Selection(CALC_TYPE, string='Calculation Type', index=True, default=CALC_TYPE[0][0])
    interest_rate_ids = fields.One2many(
        'extenss.product.interest_rate',
        'interest_rate_id',
        string='Interest Rate',)
    frequencies = fields.Many2many('extenss.product.frequencies', string="Frequencies")


class ExtenssProductInteresRateExtra(models.Model):
    _inherit ='product.template.attribute.value'
    
    @api.constrains('interest_rate_extra', 'cat_extra')   
    def _check_intcatextra(self):
        for intrat in self: 
            if intrat.interest_rate_extra <= 0:
                raise ValidationError(_('The Interest Rate must be greater than 0'))
            if intrat.cat_extra <= 0:
                raise ValidationError(_('The Cat must be greater than 0'))

    interest_rate_extra = fields.Float('Rate',  translate=True)
    cat_extra = fields.Float('Cat',  translate=True)