from odoo import fields, models, api, _, exceptions
from odoo.exceptions import Warning, UserError, ValidationError
import re

class Partner(models.Model):
    _inherit = "res.partner"

    @api.constrains('email')
    def _check_email(self):
        for reg in self:
            if reg.email:
                reg.email.replace(" ","")
                if not re.match(r"[^@]+@[^@]+\.[^@]+", reg.email):
                    raise ValidationError(_('Please enter valid email address'))

    @api.constrains('phone')
    def _check_phone(self):
        for reg in self:
            if reg.phone:
                digits = [int(x) for x in reg.phone if x.isdigit()]
                if len(digits) != 10:
                    raise ValidationError(_('The phone must be a 10 digits'))

    @api.constrains('mobile')
    def _check_mobile(self):
        for reg in self:
            if reg.mobile:
                digits = [int(x) for x in reg.mobile if x.isdigit()]
                if len(digits) != 10:
                    raise ValidationError(_('The mobile must be a 10 digits'))

    
    gender = fields.Selection([('male', 'Male'),('female','Female')], string='Gender', default='', required=True, help="Select one option")
    birth_date = fields.Date(string='Birth Date', required=True, translate=True)
    identification_type = fields.Many2one('extenss.customer.identification_type', required=True)
    identification = fields.Char(string='Indentification', required=True, translate=True)
    country_birth = fields.Many2one('res.country', string='Country of birth', required=True, translate=True)
    state_birth = fields.Many2one('res.country.state', string='State of birth', translate=True)
    marital_status = fields.Many2one('extenss.customer.marital_status')
    occupation = fields.Char(string='Occupation', translate=True)
    function = fields.Char(string='Job title', traslate=True)
    #job_title = fields.Many2one('extenss.customer.job_title')
    politically_person = fields.Boolean(string='Politically exposed person', default=True, traslate=True)
    housing_type = fields.Many2one('extenss.customer.housing_type')
    years_residence = fields.Integer(string='Years of residence', traslate=True)
    level_study = fields.Many2one('extenss.customer.level_study')
    dependent_number = fields.Integer(string='Dependent number', traslate=True)
    ssn = fields.Char(string='SSN', traslate=True)

    bankref_ids = fields.One2many('extenss.customer.bank_ref', 'bank_ref_id', string=' ')
    persref_ids = fields.One2many('extenss.customer.personal_ref', 'personal_ref_id', string=' ')
    add_identifi_ids = fields.One2many('extenss.customer.add_identifications', 'add_ident_id', string=' ')
    work_inf_ids = fields.One2many('extenss.customer.work_info', 'work_inf_id', string=' ')
    #product_type_ids = fields.One2many('extenss.customer.product_type', 'product_type_id', string='Product type')

class ExtenssCustomerIdentificationType(models.Model):
    _name = 'extenss.customer.identification_type'
    _order = 'name'
    _description = 'Identification type'

    name = fields.Char(string='Identification type', traslate=True)
    shortcut = fields.Char(string='Abbreviation', traslate=True)

class ExtenssCustomerJobTitle(models.Model):
    _name = 'extenss.customer.job_title'
    _order = 'name'
    _description = 'Job title'

    name = fields.Char(string='Job title', traslate=True)
    shortcut = fields.Char(string='Abbreviation', traslate=True)

class ExtenssCustomerMaritalStatus(models.Model):
    _name = 'extenss.customer.marital_status'
    _order = 'name'
    _description = 'Marital status'

    name = fields.Char(string='Marital status', traslate=True)
    shortcut = fields.Char(string='Abbreviation', traslate=True)

class ExtendsCustomerHousingType(models.Model):
    _name = 'extenss.customer.housing_type'
    _order = 'name'
    _descrption = 'Housing type'

    name = fields.Char(string='Housing type', traslate=True)
    shorcut = fields.Char(string='Abbreviation', traslate=True)

class ExtenssCustomerTypeRefBank(models.Model):
    _name = 'extenss.customer.type_refbank'
    _order = 'name'
    _description = 'Type of reference'

    name = fields.Char(string='Type of reference', traslate=True)
    shorcut = fields.Char(string='Abbreviation', traslate=True)

class ExtenssCustomerLevelStudy(models.Model):
    _name = 'extenss.customer.level_study'
    _order = 'name'
    _description = 'Level study'

    name = fields.Char(string='Level study', traslate=True)
    shorcut = fields.Char(string='Abbreviation', traslate=True)

# class ExtenssCustomerTypeIdentAI(models.Model):
#     _name = 'extenss.customer.type_ident_ai'
#     _order = 'name'
#     _description = 'Type of Identification'

#     name = fields.Char(string='Type of Identification', traslate=True)
#     shorcut = fields.Char(string='Abbreviation', traslate=True)

class ExtenssCustomerProductType(models.Model):
    _name = 'extenss.customer.product_type'
    _order = 'name'
    _description = 'Product type'

    name = fields.Char(string='Product type', traslate=True)
    shortcut = fields.Char(string='Abbreviation', traslate=True)

    ###--Bank References
class ExtenssCustomerBankReferences(models.Model):
    _name = "extenss.customer.bank_ref"
    _description = "Bank References Lines"

    @api.constrains('number_account', 'banking_reference')
    def _check_bankref_none(self):
        for reg_number in self:
            if reg_number.number_account == False and reg_number.banking_reference == False:
                raise ValidationError(_('Enter a value for Banking reference o Number account'))
            else:
                digits = [int(x) for x in reg_number.banking_reference if x.isdigit()]
                if len(digits) != 18:
                    raise ValidationError(_('The bankin reference must be a 18 digits'))

    bank_ref_id = fields.Many2one('res.partner')#modelo padre
    #product_type = fields.Char(string='Product type', required=True, traslate=True)
    product_type = fields.Many2one('extenss.customer.product_type', required=True, traslate=True)
    institution = fields.Many2one('res.bank', required=True)#modelo padre
    banking_reference = fields.Char(string='Banking reference', size=18, traslate=True)
    number_account = fields.Char(string='Number account', traslate=True)
    comments_bank_ref = fields.Char(string='Comments', traslate=True)

    ###--Personal References
class ExtenssCustomerPersonalReferences(models.Model):
    _name = "extenss.customer.personal_ref"
    _description = "Personal references"

    @api.constrains('email_personal_ref', 'phone_personal_ref', 'cell_phone_personal_res')
    def _check_fields_none(self):
        for reg_pr in self:
            if reg_pr.email_personal_ref == False and reg_pr.phone_personal_ref == False and reg_pr.cell_phone_personal_res == False:
                raise ValidationError(_('Enter a value in any of the fields Phone, Cell phone or Email'))
    
    @api.constrains('phone_personal_ref')
    def _check_phone_personal(self):
        for reg in self:
            digits = [int(x) for x in reg.phone_personal_ref if x.isdigit()]
            if len(digits) != 10:
                raise ValidationError(_('The phone must be a 10 digits'))

    @api.constrains('cell_phone_personal_res')
    def _check_cell_phone_res(self):
        for reg_cell in self:
            if not reg_cell.cell_phone_personal_res == False:
                digits1 = [int(x) for x in reg_cell.cell_phone_personal_res if x.isdigit()]
                if len(digits1) != 10:
                    raise ValidationError(_('The cell phone must be a 10 digits'))

    @api.constrains('email_personal_ref')
    def _check_email_personal_ref(self):
        for reg_ref in self:
            if not reg_ref.email_personal_ref == False:
                reg_ref.email_personal_ref.replace(" ","")
                if not re.match(r"[^@]+@[^@]+\.[^@]+", reg_ref.email_personal_ref):
                    raise ValidationError(_('Please enter valid email address'))

    personal_ref_id = fields.Many2one('res.partner')#modelo padre
    type_reference_personal_ref = fields.Many2one('extenss.customer.type_refbank', string='Type reference', required=True,traslate=True)
    #type_reference_personal_ref = fields.Char(string='Type reference', required=True,traslate=True)
    reference_name_personal_ref = fields.Char(string='Reference name', required=True, traslate=True)
    phone_personal_ref = fields.Char(string='Phone', traslate=True)
    cell_phone_personal_res = fields.Char(string='Cell phone', traslate=True)
    email_personal_ref = fields.Char(string='Email', traslate=True)

    ###--Aditional identifications
    class ExtenssCustomerAditionalIdentifications(models.Model):
        _name = "extenss.customer.add_identifications"
        _description = "Aditional identifications"

        add_ident_id = fields.Many2one('res.partner')#modelo padre
        type_of_indentification = fields.Many2one('extenss.customer.identification_type', string='Type of identification', required=True,)
        identification_ai = fields.Char(string='Indentification', required=True, translate=True)

    ###--Work information
class ExtenssCustomerWorkInfo(models.Model):
    _name = "extenss.customer.work_info"
    _description = "Work information"

    @api.constrains('email_wi')
    def _check_email_wi(self):
        for reg_wi in self:
            if not reg_wi.email_wi == False:
                reg_wi.email_wi.replace(" ","")
                if not re.match(r"[^@]+@[^@]+\.[^@]+", reg_wi.email_wi):
                    raise ValidationError(_('Please enter valid email address'))

    @api.constrains('principal_phone')
    def _check_prin_phone(self):
        for reg_ph_wi in self:
            if not reg_ph_wi.principal_phone == False:
                digits1 = [int(x) for x in reg_ph_wi.principal_phone if x.isdigit()]
                if len(digits1) != 10:
                    raise ValidationError(_('The principal phone must be a 10 digits'))

    @api.constrains('optional_phone')
    def _check_opt_phone(self):
        for reg_opt in self:
            if not reg_opt.optional_phone == False:
                digits1 = [int(x) for x in reg_opt.optional_phone if x.isdigit()]
                if len(digits1) != 10:
                    raise ValidationError(_('The optional phone must be a 10 digits'))

    work_inf_id = fields.Many2one('res.partner')#modelo padre
    company = fields.Char(string='Company', traslate=True, required=True)
    position = fields.Char(string='Position', traslate=True, required=True)
    start_date = fields.Date(string='Star date', traslate=True, required=True)
    close_date = fields.Date(string='Close date', traslate=True)
    email_wi = fields.Char(string='Email', traslate=True)
    principal_phone = fields.Char(string='Principal phone', traslate=True)
    optional_phone = fields.Char(string='Optional phone', traslate=True)
