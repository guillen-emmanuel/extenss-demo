from odoo import api, fields, models
from odoo.exceptions import Warning

class Partner(models.Model):
    _inherit = "res.partner"

    def valfields(self):
        if self.years_residence.isdigit() == False:
            raise Warning('Please enter only numbers' % self.years_residence)        
        if self.dependent_number.isdigit()== False:
            raise Warning('Plaase enter only numbers' % self.dependent_number)
        if self.ssn.isdgit() == False:
            raise Warning('Plase enter only nmbers' % self.ssn)

    gender = fields.Selection([('male', 'Male'),('female','Female')], string='Gender', default='', required=True, help="Select one option")
    birth_date = fields.Date(string='Birth Date', required=True, translate=True)
    identification_type = fields.Many2one('extenss.customer.identification_type', required=True)
    identification = fields.Char(string='Indentification', required=True, translate=True)
    country_birth = fields.Many2one('res.country', string='Country of birth', required=True, translate=True)
    state_birth = fields.Many2one('res.country.state', string='State of birth', translate=True)
    marital_status = fields.Many2one('extenss.customer.marital_status')
    occupation = fields.Char(string='Occupation', translate=True)
    job_title = fields.Many2one('extenss.customer.job_title')
    politically_person = fields.Boolean(string='Politically exposed person', default=True, traslate=True)
    housing_type = fields.Many2one('extenss.customer.housing_type')
    years_residence = fields.Integer(string='Years of residence', traslate=True)
    level_study = fields.Many2one('extenss.customer.level_study')
    dependent_number = fields.Integer(string='Dependent number', traslate=True)
    ssn = fields.Char(string='SSN', traslate=True)

    bankref_ids = fields.One2many('extenss.customer.bank_ref', 'bank_ref_id', string='Bank references')
    persref_ids = fields.One2many('extenss.customer.personal_ref', 'personal_ref_id', string='Personal references')
    add_identifi_ids = fields.One2many('extenss.customer.add_identifications', 'add_ident_id', string='Aditional identifications')
    work_inf_ids = fields.One2many('extenss.customer.work_info', 'work_inf_id', string='Work information')

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
    #_order = 'name'
    _description = 'Type of reference'

    name = fields.Char(string='Type of reference', traslate=True)
    shorcut = fields.Char(string='Abbreviation', traslate=True)

class ExtenssCustomerLevelStudy(models.Model):
    _name = 'extenss.customer.level_study'
    _order = 'name'
    _description = 'Level study'

    name = fields.Char(string='Level study', traslate=True)
    shorcut = fields.Char(string='Abbreviation', traslate=True)

class ExtenssCustomerTypeIdentAI(models.Model):
    _name = 'extenss.customer.type_ident_ai'
    _order = 'name'
    _description = 'Type of Identification'

    name = fields.Char(string='Type of Identification', traslate=True)
    shorcut = fields.Char(string='Abbreviation', traslate=True)


    ###--Bank References
    class ExtenssCustomerBankReferences(models.Model):
        _name = "extenss.customer.bank_ref"
        _description = "Bank References Lines"
        
        #def valfields(self):
            #if validate_email(self.email_bank_ref) == False:
                #raise Warning('Please enter only numbers' % self.email_bank_ref)

         #  if len(self.banking_reference.isdigit()) == 18:
        bank_ref_id = fields.Many2one('res.partner')#modelo padre
        product_type = fields.Char(string='Product type', required=True, traslate=True)
        institution = fields.Many2one('res.partner.bank')#modelo padre
        #institution = fields.Char(string='Institution', required=True, traslate=True)
        banking_reference = fields.Char(string='Banking reference', traslate=True)
        number_account = fields.Char(string='Number account', traslate=True)
        comments_bank_ref = fields.Char(string='Comments', traslate=True)
        type_reference_bankref = fields.Many2one('extenss.customer.type_refbank', string='Type of reference')
        reference_name_bank_ref = fields.Char(string='Reference name', traslate=True)
        phone_bank_ref = fields.Char(string='Phone', traslate=True)
        cell_phone_bank_ref = fields.Char(string='Cell phone', traslate=True)
        email_bank_ref = fields.Char(string='Email', traslate=True)

    ###--Personal References
    class ExtenssCustomerPersonalReferences(models.Model):
        _name = "extenss.customer.personal_ref"
        _description = "Personal references"

        personal_ref_id = fields.Many2one('res.partner')#modelo padre
        type_reference_personal_ref = fields.Char(string='Type reference', required=True,traslate=True)
        reference_name_personal_ref = fields.Char(string='Reference name', required=True, traslate=True)
        phone_personal_ref = fields.Char(string='Phone', traslate=True)
        cell_phone_personal_res = fields.Char(string='Cell phone', traslate=True)
        email_personal_ref = fields.Char(string='Email', traslate=True)

    ###--Aditional identifications
    class ExtenssCustomerAditionalIdentifications(models.Model):
        _name = "extenss.customer.add_identifications"
        _description = "Aditional identifications"

        add_ident_id = fields.Many2one('res.partner')#modelo padre
        type_of_indentification = fields.Many2one('extenss.customer.type_ident_ai', string='Type of identification', required=True,)
        identification_ai = fields.Char(string='Indentification', required=True, translate=True)

    ###--Work information
    class ExtenssCustomerWorkInfo(models.Model):
        _name = "extenss.customer.work_info"
        _description = "Work information"

        work_inf_id = fields.Many2one('res.partner')#modelo padre
        company = fields.Char(string='Company', traslate=True, required=True)
        position = fields.Char(string='Position', traslate=True, required=True)
        start_date = fields.Date(string='Star date', traslate=True, required=True)
        close_date = fields.Date(string='Close date', traslate=True, )
        email = fields.Char(string='Email', traslate=True)
        principal_phone = fields.Char(string='Principal phone', traslate=True)
        optional_phone = fields.Char(string='Optional phone', traslate=True)

    ###-Request
    #class ExtenssCustomerRequest(models.Model):
        #_name = "extenss.customer.request"
        #_description = "Request"

        #id_request = fields.Char(string='Id request')
        #product = fields.Char(string='Product', traslate=True)
        #requested_amount = fields.Monetary('Requested amount', currency_field='company_currency', tracking=True)
        #date_req = fields.Date(string='Date', traslate=True)
        #start_date_req = fields.Date(string='Star date', traslate=True)
        #close_date_req = fields.Date(string='Close date', traslate=True)
        #company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
        #company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)

