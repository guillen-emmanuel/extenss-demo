from odoo import fields, models, exceptions, api, _
from odoo.exceptions import Warning, UserError, ValidationError

class ExtenssRequestDestination(models.Model):
    _name =  'extenss.request.destination'
    _order = 'name'
    _description = 'Destination loan'

    name = fields.Char(string='Destination loan', required=True, translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)

class ExtenssRequestSalesChannelId(models.Model):
    _name = 'extenss.request.sales_channel_id'
    _order = 'name'
    _description ='Sales channel'

    name = fields.Char(string='Sales channel', required=True, translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)

class ExtenssRequestCategoryAct(models.Model):
    _name = 'extenss.request.category_act'
    _order = 'name'
    _description = 'Category'

    name = fields.Char(strig='Category', required=True, translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)

class ExtenssRequestCategoryPas(models.Model):
    _name = 'extenss.request.category_pas'
    _order = 'name'
    _description = 'Category'

    name = fields.Char(strig='Category', required=True, translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)

class ExtenssRequestHipoteca(models.Model):
    _name = 'extenss.request.hipoteca'
    _order = 'name'
    _description = 'Tipo de hipoteca'

    name = fields.Char(string='Tipo de hipoteca', required=True, translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)

class ExtenssRequestTipoIngreso(models.Model):
    _name = 'extenss.request.tipo_ingreso'
    _order = 'name'
    _description = 'Tipo de ingreso'

    name = fields.Char(string='Tipo de ingreso', required=True, translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)

class ExtenssRequestTipoGasto(models.Model):
    _name = 'extenss.request.tipo_gasto'
    _order = 'name'
    _description = 'Tipo de gasto'

    name = fields.Char(string='Tipo de gasto', required=True, translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)

class ExtenssRequestFrecuencia(models.Model):
    _name = 'extenss.request.frecuencia'
    _order = 'name'
    _description = 'Frecuencia'

    name = fields.Char(string='Frecuencia', required=True, translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)

class ExtenssRequestBase(models.Model):
    _name = 'extenss.request.base'
    _order = 'name'
    _description = 'Base'

    name = fields.Char(string='Base', required=True, translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)

class Lead(models.Model):
    _inherit = "crm.lead"

    @api.constrains('owners_phone')
    def _check_prin_phone(self):
        for reg in self:
            if not reg.owners_phone == False:
                digits1 = [int(x) for x in reg.owners_phone if x.isdigit()]
                if len(digits1) != 10:
                    raise ValidationError(_('The principal phone must be a 10 digits'))
    
    @api.constrains('months_residence')
    def _check_years(self):
        for reg_years in self:
            if reg_years.months_residence > 999:
                raise ValidationError(_('The Years residence must be a 3 digits'))

    def open_docs_count(self):
        #domain = [('folder_id', '=', self.ids)],('partner_id', '=', self.partner_id.id),
        if self.env['documents.document'].search_count([('lead_id', '=', self.id)]) <= 0:
            self.crear_documentos()
        ##domain = [('partner_id', '=', self.partner_id.id)]
        #domain = [('partner_id', '=', [self.partner_id.id]),('lead_id', '=', True),('lead_id', 'in', [self.id])]
        domain = [('lead_id', 'in', [self.id])]
        return {
            'name': _('Documents'),
            'view_type': 'kanban',
            'domain': domain,
            'res_model': 'documents.document',
            'type': 'ir.actions.act_window',
            #'views': [(False, 'list'), (False, 'form')],
            'view_mode': 'kanban,tree,form',
            'context': "{'default_folder_id': %s}" % self.ids
        }
    
    def get_document_count(self):
        ##count = self.env['documents.document'].search_count([('partner_id', '=', self.partner_id.id)])
        count = self.env['documents.document'].search_count([('lead_id', '=', self.id)])
        #count = self.env['documents.document'].search_count([('partner_id', '=', [self.partner_id.id]),('lead_id', '=', True),('lead_id', 'in', [self.id])])
        self.document_count = count

    def crear_documentos(self):
        if not self.product_id:
            return
        for reg in self.product_id.catalogo_docs:
            docs_product = reg.name
            if self.product_id.flag_activo == True:
                document = self.env['documents.document'].create({
                    'name': docs_product,##'Docs automatico',
                    'type': 'empty',
                    'folder_id': 1,
                    'owner_id': self.env.user.id,
                    'partner_id': self.partner_id.id if self.partner_id else False,
                    'res_id': 0,
                    'res_model': 'documents.document',
                    'lead_id': self.id
                })
            else:
                return

    destination_id = fields.Many2one('extenss.request.destination', string='Destination loan')
    name = fields.Char(string='Request number', required=True, copy=False, readonly=True, index=True, translate=True, default=lambda self: _('New'))
    sales_channel_id = fields.Many2one('extenss.request.sales_channel_id')
    create_date = fields.Date(string='Create date', readonly=True, translate=True)
    closed_date = fields.Date(string='Closed date', readonly=True, translate=True)
    product_id = fields.Many2one('product.product', string='Product', translate=True)
    user_id = fields.Many2one('res.users')
    #partner_type = fields.Char('Partner type', readonly=True, default=lambda self: self.env.company.company_type)
    #self.env["res.partner"]
    #team_id = fields.Char(string='Office')
    #planned_revenue = fields.Char(string='Request amount', translate=True)
    #description = fields.Text(string='Comments', translate=True)
    document_count = fields.Integer("Documentos", compute='get_document_count')

    partner_id = fields.Many2one('res.partner', string='Customer')
    #Resident Profile
    housing_type_rp = fields.Selection([('rented', 'Rented'),('own','Own')], string='Housing type', translate=True)
    owners_name = fields.Many2one('res.partner', string='Owners name', translate=True)
    owners_phone = fields.Char(string='Owners phone', translate=True)
    montly_rent = fields.Monetary(string='Montly rent', currency_field='company_currency', tracking=True, translate=True)
    months_residence = fields.Integer(string='Months in Residence', translate=True)
    residency_profile = fields.Char(string='Residency profile', translate=True)

    rent = fields.Monetary(string='Rent', currency_field='company_currency', translate=True)
    first_mortage = fields.Monetary(string='First mortage', currency_field='company_currency', tracking=True, translate=True)
    another_finantiation = fields.Monetary(string='Another finantiation', currency_field='company_currency', tracking=True, translate=True)
    risk_insurance = fields.Monetary(string='Risk insurance', currency_field='company_currency', tracking=True, translate=True)
    real_state_taxes = fields.Monetary(string='Real state taxes', currency_field='company_currency', tracking=True, translate=True)
    mortage_insurance = fields.Monetary(string='Mortage insurance', currency_field='company_currency', tracking=True, translate=True)
    debts_cowners = fields.Monetary(string='Debts co-owners', currency_field='company_currency', tracking=True, translate=True)
    other = fields.Monetary(string='Other', currency_field='company_currency', tracking=True, translate=True)
    total_resident = fields.Monetary(string='Total', compute='_compute_total_resident', store=True, currency_field='company_currency')

    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)

    # sale_amount_total = fields.Monetary(compute='_compute_sale_data', string="Sum of Orders", help="Untaxed Total of Confirmed Orders", currency_field='company_currency')
    #lead_ids = fields.One2many('documents.document', 'lead_id', string='Crm lead id')

    # @api.depends('order_ids.state','order_ids.product_id')
    # def _compute_sale_data(self):
    #     for order in self.order_ids:
    #         if order.state in ('sale'):
    #             #self.product_id = self.order_ids.product_id
    #             self.write({'product_id': order.product_id})

    @api.depends('rent','first_mortage','another_finantiation','risk_insurance','real_state_taxes','mortage_insurance','debts_cowners','other')
    def _compute_total_resident(self):
        for reg in self:
            reg.total_resident = reg.rent + reg.first_mortage + reg.another_finantiation + reg.risk_insurance + reg.real_state_taxes + reg.mortage_insurance + reg.debts_cowners + reg.other

    # @api.onchange('partner_id')
    # def change_partner_id(self):
    #     if not self.partner_id:
    #         return
    #     #self.partner_name = self.partner_id.name
    #     for reg in self:
    #         data = {
    #                 'partner_id': reg.partner_id.name,
    #         }
    #         for reg in reg.fin_sit_ids:
    #             fin_sit_ids = [(1, reg.id, data)]
    #             self.fin_sit_ids = fin_sit_ids

    @api.model
    def create(self, reg):
        if reg:
            if reg.get('name', _('New')) == _('New'):
                reg['name'] = self.env['ir.sequence'].next_by_code('crm.lead') or _('New')
            result = super(Lead, self).create(reg)
            return result

    fin_sit_ids = fields.One2many('extenss.crm.lead.financial_sit', 'financial_id', string=' ')
    #asset_ids = fields.One2many('extenss.crm.lead.financial_sit', 'asset_id', string=' ')
    fin_pos_ids = fields.One2many('extenss.crm.lead.financial_pos', 'financial_pos_id', string=' ')
    fin_pas_ids = fields.One2many('extenss.crm.lead.financial_pos', 'financial_pas_id', string=' ')
    #patrimonial_ids = fields.One2many('extenss.crm.lead.patrimonial', 'patrimonial_id', string=' ')
    owner_ids = fields.One2many('extenss.crm.lead.ownership', 'ownership_id', string=' ')
    #liabilites_ids = fields.One2many('extenss.crm.lead.liabilities', 'liabilities_id', string=' ')
    #income_ids = fields.One2many('extenss.crm.lead.income_statement', 'income_id', string=' ')
    surce_ids = fields.One2many('extenss.crm.lead.source_income', 'surce_id', string=' ')

# class SaleOrder(models.Model):
#     _inherit = 'sale.order'

#     opportunity_id = fields.Many2one(
#         'crm.lead', string='Opportunity', check_company=True,
#         domain="[('type', '=', 'opportunity'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")

class ExtenssDocuments(models.Model):
    _inherit = "documents.document"

    lead_id = fields.Char(string="Lead Id")

class ExtenssCrmLeadFinancialSit(models.Model):
    _name = "extenss.crm.lead.financial_sit"
    _description = "Financial situation"

    financial_id = fields.Many2one('crm.lead')#modelo padre
    date_fin_sit = fields.Date(string='Date', required=True, translate=True)
    #partner_name = fields.Char(string='Company', translate=True)
    partner_id = fields.Many2one('res.partner', string='Customer')#, default=lambda self: self.env.user.partner_id.id)#default=10)#default=lambda self: self.env.partner_id)#
    #partner_name = fields.Char(related='partner_id.name', string='Company', translate=True)
    base = fields.Many2one('extenss.request.base', string='Base', translate=True)
    frequency = fields.Many2one('extenss.request.frecuencia', string='Frequency', translate=True)
    description = fields.Char(string='Description', translate=True)
    #Assets
    efectivo = fields.Monetary(string='Cash', currency_field='company_currency', tracking=True, translate=True)
    cuentas_cobrar = fields.Monetary(string='Accounts receivable', currency_field='company_currency', tracking=True, translate=True)
    inventario = fields.Monetary(string='Inventory', currency_field='company_currency', tracking=True, translate=True)
    activo_adicional1_tipo = fields.Char(string='Activo adicional 1 Tipo', translate=True)
    activo_adicional1_importe = fields.Monetary(string='Activo adicional 1 Importe', currency_field='company_currency', tracking=True, translate=True)
    activo_adicional2_tipo = fields.Char(string='Activo adicional 2 Tipo', translate=True)
    activo_adicional2_importe = fields.Monetary(string='Activo adicional 2 Importe', currency_field='company_currency', tracking=True, translate=True)
    activo_otras_cuentas = fields.Monetary(string='Activo de otras cuentas', currency_field='company_currency', tracking=True, translate=True)
    total_activo_circulante = fields.Monetary(string='Total activo circunlante', currency_field='company_currency', compute='_compute_total_circulante', store=True, tracking=True, translate=True)

    activos_fijos = fields.Monetary(string='Activos fijos', currency_field='company_currency', tracking=True, translate=True)
    depreciacion = fields.Monetary(string='Depreciación', currency_field='company_currency', tracking=True, translate=True)
    activos_intangibles = fields.Monetary(string='Activos intangibles', currency_field='company_currency', tracking=True, translate=True)
    total_activos_fijos = fields.Monetary(string='Total activos fijos', currency_field='company_currency', compute='_compute_total_af', store=True, tracking=True, translate=True)

    otros_activos = fields.Monetary(string='Otros activos', currency_field='company_currency', tracking=True, translate=True)
    otro_activo_adicional = fields.Char(string='Otro activo adicional, tipo de activo', translate=True)
    otro_activo_importe = fields.Monetary(string='Otro activo adicional, importe de activo', currency_field='company_currency', tracking=True, translate=True)
    total_otros_activos = fields.Monetary(string='Total otros activos', currency_field='company_currency', compute='_compute_total_oa', store=True, tracking=True, translate=True)

    activos_totales = fields.Monetary(string='Activos totales', currency_field='company_currency', compute='_compute_total_activos', store=True, tracking=True, translate=True)
    verifica_importes = fields.Boolean(string='Verifica importes', compute='_compute_flag_vi', store=True, default=False, readonly=True, translate=True)#(Activo=Pasivo+Capital)
    #Liabilities
    proveedores	= fields.Monetary(string='Provedores', currency_field='company_currency', tracking=True, translate=True)
    pasivo_tipo = fields.Char(string='Pasivo tipo', translate=True)
    pasivo_importe = fields.Monetary(string='Pasivo importe', currency_field='company_currency', tracking=True, translate=True)
    parte_corto_plazo = fields.Monetary(string='Parte a corto plazo de deuda a largo plazo', currency_field='company_currency', tracking=True, translate=True)
    otro_pasivo_circulante = fields.Monetary(string='Otro pasivo circulante', currency_field='company_currency', tracking=True, translate=True)
    pasivo_total_circulante = fields.Monetary(string='Pasivo total circulante', currency_field='company_currency', compute='_compute_pasivo_tc', store=True, tracking=True, translate=True)

    deuda_largo_plazo = fields.Monetary(string='Deuda a largo plazo', currency_field='company_currency', tracking=True, translate=True)
    deuda_adicional_actual_tipo	= fields.Char(string='Deuda adicional actual tipo', translate=True)
    deuda_adicional_actual_importe = fields.Monetary(string='Deuda adicional actual importe', currency_field='company_currency', tracking=True, translate=True)
    otro_pasivo_no_circulante = fields.Monetary(string='Otro pasivo no circulante', currency_field='company_currency', tracking=True, translate=True)
    pasivo_total_no_circulante	= fields.Monetary(string='Pasivo total no circulante', currency_field='company_currency', compute='_compute_pasivo_tnc', store=True, tracking=True, translate=True)

    capital	= fields.Monetary(string='Capital', currency_field='company_currency', tracking=True, translate=True)
    capital_desembolso = fields.Monetary(string='Capital desembolso', currency_field='company_currency', tracking=True, translate=True)
    utilidades_perdidas_acumuladas = fields.Monetary(string='Utilidades (pérdidas) acumuladas', currency_field='company_currency', tracking=True, translate=True)
    utilidad_ejercicio = fields.Monetary(string='Utilidad del ejercicio', currency_field='company_currency', tracking=True, translate=True)
    total_capital_contable = fields.Monetary(string='Total capital contable', currency_field='company_currency', compute='_compute_total_cc', store=True, tracking=True, translate=True)
    
    pasivo_total_capital_contable = fields.Monetary(string='Pasivo total y Capital contable', currency_field='company_currency', compute='_compute_pasivo_tcc', store=True, tracking=True, translate=True)

    #Income Statement
    ventas_netas = fields.Monetary(string='Ventas netas', currency_field='company_currency', tracking=True, translate=True)

    costo_ventas = fields.Monetary(string='Costo de ventas', currency_field='company_currency', tracking=True, translate=True)
    ganancia_bruta = fields.Monetary(string='Ganancia bruta', currency_field='company_currency', compute='_compute_ganancia_bruta', store=True, tracking=True, translate=True)

    otros_ingresos_is = fields.Monetary(string='Otros ingresos', currency_field='company_currency', tracking=True, translate=True)
    ingresos_adicionales_tipo = fields.Char(string='Ingresos operativos adicionales, tipo de ingresos', translate=True)
    ingresos_adicionales_importe = fields.Monetary(string='Ingresos operativos adicionales, importe de ingresos', currency_field='company_currency', tracking=True, translate=True)
    gastos_ope_ad_1_tipo= fields.Char(string='Gastos operativos adicionales 1, tipo de gastos', translate=True)
    gastos_ope_ad_1_importe = fields.Monetary(string='Gastos operativos adicionales 1, importe de gastos', currency_field='company_currency', tracking=True, translate=True)
    gastos_ope_ad_2_tipo = fields.Char(string='Gastos operativos adicionales 2, tipo de gastos', translate=True)
    gastos_ope_ad_2_importe = fields.Monetary(string='Gastos operativos adicionales 2, importe de gastos', currency_field='company_currency', tracking=True, translate=True)
    beneficios_ope_totales = fields.Monetary(string='Beneficios operativos totales', currency_field='company_currency', compute='_compute_beneficios', store=True, tracking=True, translate=True)

    interes = fields.Monetary(string='Interes', currency_field='company_currency', tracking=True, translate=True)
    otros_gastos = fields.Monetary(string='Otros gastos', currency_field='company_currency', tracking=True, translate=True)
    depreciación = fields.Monetary(string='Depreciación', currency_field='company_currency', tracking=True, translate=True)
    impuestos = fields.Monetary(string='Impuestos', currency_field='company_currency', tracking=True, translate=True)
    utilidad_neta = fields.Monetary(string='Utilidad neta', currency_field='company_currency', tracking=True, translate=True)

    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)

    @api.depends('ventas_netas','costo_ventas')
    def _compute_ganancia_bruta(self):
        for reg in self:
            reg.ganancia_bruta = reg.ventas_netas - reg.costo_ventas

    @api.depends('otros_ingresos_is','ingresos_adicionales_importe','gastos_ope_ad_1_importe','gastos_ope_ad_2_importe')
    def _compute_beneficios(self):
        for reg in self:
            reg.beneficios_ope_totales = reg.otros_ingresos_is + reg.ingresos_adicionales_importe - reg.gastos_ope_ad_1_importe - reg.gastos_ope_ad_2_importe

    @api.depends('proveedores','pasivo_importe','parte_corto_plazo','otro_pasivo_circulante')
    def _compute_pasivo_tc(self):
        for reg in self:
            reg.pasivo_total_circulante = reg.proveedores + reg.pasivo_importe + reg.parte_corto_plazo + reg.otro_pasivo_circulante

    @api.depends('deuda_largo_plazo','deuda_adicional_actual_importe','otro_pasivo_no_circulante')
    def _compute_pasivo_tnc(self):
        for reg in self:
            reg.pasivo_total_no_circulante = reg.deuda_largo_plazo + reg.deuda_adicional_actual_importe + reg.otro_pasivo_no_circulante

    @api.depends('capital','capital_desembolso','utilidades_perdidas_acumuladas','utilidad_ejercicio')
    def _compute_total_cc(self):
        for reg in self:
            reg.total_capital_contable = reg.capital + reg.capital_desembolso + reg.utilidades_perdidas_acumuladas + reg.utilidad_ejercicio

    @api.depends('pasivo_total_circulante','pasivo_total_no_circulante','total_capital_contable')
    def _compute_pasivo_tcc(self):
        for reg in self:
            reg.pasivo_total_capital_contable = reg.pasivo_total_circulante + reg.pasivo_total_no_circulante + reg.total_capital_contable

    @api.depends('efectivo','cuentas_cobrar','inventario','activo_adicional1_importe','activo_adicional2_importe','activo_otras_cuentas')
    def _compute_total_circulante(self):
        for reg in self:
            reg.total_activo_circulante = reg.efectivo + reg.cuentas_cobrar + reg.inventario + reg.activo_adicional1_importe + reg.activo_adicional2_importe + reg.activo_otras_cuentas

    @api.depends('activos_fijos','depreciacion','activos_intangibles')
    def _compute_total_af(self):
        for reg in self:
            reg.total_activos_fijos = reg.activos_fijos + reg.depreciacion + reg.activos_intangibles
    
    @api.depends('otros_activos','otro_activo_importe')
    def _compute_total_oa(self):
        for reg in self:
            reg.total_otros_activos = reg.otros_activos + reg.otro_activo_importe

    @api.depends('total_activo_circulante','total_activos_fijos','total_otros_activos')
    def _compute_total_activos(self):
        for reg in self:
            reg.activos_totales = reg.total_activo_circulante + reg.total_activos_fijos + reg.total_otros_activos
    
    @api.depends('activos_totales','pasivo_total_capital_contable')
    def _compute_flag_vi(self):
        for reg in self:
            if reg.activos_totales == reg.pasivo_total_capital_contable:
                reg.verifica_importes = True
            if reg.activos_totales != reg.pasivo_total_capital_contable:
                reg.verifica_importes = False

class ExtenssCrmLeadFinancialPos(models.Model):
    _name = "extenss.crm.lead.financial_pos"
    _description = "Financial position"

    financial_pos_id = fields.Many2one('crm.lead')#modelo padre
    category_act = fields.Many2one('extenss.request.category_act', string='Category', translate=True)
    value_act = fields.Monetary(string='Value', currency_field='company_currency', tracking=True, translate=True)
    description_act = fields.Char(string='Description', translate=True)
    institution_act = fields.Many2one('res.bank', string='Institution', translate=True)#catalogo de bancos
    account_number_act = fields.Char(string='Account number', translate=True)
    verify_act = fields.Boolean(string='Verify', transalate=True)
    #total_activos_act = fields.Monetary(string='Total activos', currency_field='company_currency', compute='_compute_total_act', store=True, tracking=True, translate=True)

    financial_pas_id = fields.Many2one('crm.lead')#modelo padre
    category_pas = fields.Many2one('extenss.request.category_pas', string='Category', translate=True)
    value_pas = fields.Monetary(string='Value', currency_field='company_currency', tracking=True, translate=True)
    pago_mensual_pas = fields.Monetary(string='Pago mensual', currency_field='company_currency', tracking=True, translate=True)
    description_pas = fields.Char(string='Description', translate=True)
    institution_pas = fields.Many2one('res.bank', string='Institution', translate=True)#catalogo de bancos
    account_number_pas = fields.Char(string='Account number', translate=True)
    tipo_hipoteca = fields.Many2one('extenss.request.hipoteca', string='Tipo de hipoteca', translate=True)
    #total_pasivos = fields.Monetary(string='Total pasivos', currency_field='company_currency', compute='_compute_pasivos', store=True, tracking=True, translate=True)

    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)

class ExtenssCrmLeadSourceIncome(models.Model):
    _name = "extenss.crm.lead.source_income"
    _description = "Source of income"

    surce_id = fields.Many2one('crm.lead')
    tipo_ingreso = fields.Many2one('extenss.request.tipo_ingreso', string='Tipo de ingreso', translate=True)
    importe_ing= fields.Monetary(string='Importe', currency_field='company_currency', tracking=True, translate=True)
    persona_ing	= fields.Many2one('res.partner', string='Persona', translate=True)
    importe_mensual_ing = fields.Monetary(string='Importe mensual', currency_field='company_currency', tracking=True, translate=True)
    frecuencia_ing = fields.Many2one('extenss.request.frecuencia', string='Frecuencia', translate=True)#catalogo
    sujeto_impuestos_ing = fields.Boolean(string='Sujeto a impuestos', translate=True)
    comentarios_ing	= fields.Char(string='Comentarios', translate=True)
    total_ingresos = fields.Monetary(string='Total ingresos', currency_field='company_currency', tracking=True, translate=True)
    
    tipo_gasto = fields.Many2one('extenss.request.tipo_gasto', string='Tipo de gasto', translate=True)
    importe_gas = fields.Monetary(string='Importe', currency_field='company_currency', tracking=True, translate=True)
    persona_gas = fields.Many2one('res.partner', string='Persona', translate=True)
    importe_mensual_gas = fields.Monetary(string='Importe mensual', currency_field='company_currency', tracking=True, translate=True)
    frecuencia_gas = fields.Many2one('extenss.request.frecuencia', string='Frecuencia', translate=True)	
    comentarios_gas = fields.Char(string='Comentarios', translate=True)
    total_gastos = fields.Monetary(string='Total gastos', currency_field='company_currency', tracking=True, translate=True)

    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)

#class ExtenssCrmLeadResidenceProfile(models.Model):
    #_name = "extenss.crm.lead.residence_profile"
    #_description = "Residence Profile"
    #_inherit = "crm.lead"
class ExtenssCrmLeadOwnership(models.Model):
    _name = "extenss.crm.lead.ownership"
    _description = "Ownership"

    ownership_id = fields.Many2one('crm.lead')#modelo padre
    description_own = fields.Char(string='Description', translate=True)
    percentage_properties = fields.Float(string='Percentage in properties', translate=True)
    purchace_price = fields.Monetary(string='Purchace price', currency_field='company_currency', tracking=True, translate=True)
    bookvalue = fields.Monetary(string='Bookvalue', currency_field='company_currency', tracking=True, translate=True)
    market_value = fields.Monetary(string='Market value', currency_field='company_currency', tracking=True, translate=True)
    stock_exchange_value = fields.Monetary(string='Stock exchange value', currency_field='company_currency', tracking=True, translate=True)
    mortages_own = fields.Monetary(string='Mortages', currency_field='company_currency', tracking=True, translate=True)

    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
