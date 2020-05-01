import logging
from odoo import api, fields, models, _
from odoo.exceptions import Warning, UserError, ValidationError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

COMMISION_TYPE = [
    ('0', 'Porcentaje'),
    ('1', 'Monto'),
]

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.constrains('date_start', 'date_first_payment', 'amount', 'credit_type','rents_deposit','purchase_option','residual_porcentage')   
    def _check_intrat(self):
        for quotation in self:
            if not quotation.product_id:
                raise Warning('Please provide a Product for %s' % quotation.name)
            if datetime.now().date() > quotation.date_start:
                raise Warning('Star Date must be greater or equal than Today for %s' % quotation.name)
            if quotation.date_first_payment < quotation.date_start:
                raise Warning('Date First Payment must be greater or equal than Date Start for %s' % quotation.name)
            if not quotation.amount:
                raise Warning('Please provide a Request Amount for %s' % quotation.name)
            if quotation.amount < quotation.min_amount or quotation.amount > quotation.max_amount:
                raise Warning('The Request Amount must be older than Min Amount and less than Max Amount %s' % quotation.name)
            if quotation.credit_type == 'Arrendamiento Financiero' or quotation.credit_type == 'Arrendamiento Puro':
                if quotation.credit_type == 'Arrendamiento Financiero':
                    if not quotation.guarantee_percentage:
                        raise Warning('Please provide a Guarantee Porcentage for %s' % quotation.name)
                if not quotation.purchase_option:
                    raise Warning('Please provide a Purchase Option Porcentage for %s' % quotation.name)
                if quotation.credit_type == 'Arrendamiento Puro':
                    if not quotation.residual_porcentage:
                        raise Warning('Please provide a Residual Porcentage for %s' % quotation.name)

    def action_quotation_calculate(self):
        for quotation in self:
            if not quotation.product_id:
                raise Warning('Please provide a Product for %s' % quotation.name)
            if not quotation.date_start:
                raise Warning('Please provide a Start Date for %s' % quotation.name)
            if not quotation.date_first_payment:
                raise Warning('Please provide a First Payment Date for %s' % quotation.name)
            if quotation.date_first_payment < quotation.date_start:
                raise Warning('Date First Payment must be greater or equal than Date Start for %s' % quotation.name)
            if not quotation.amount:
                raise Warning('Please provide a Request Amount for %s' % quotation.name)
            if quotation.amount < quotation.min_amount or quotation.amount > quotation.max_amount:
                raise Warning('The Request Amount must be older than Min Amount and less than Max Amount %s' % quotation.name)
            if quotation.credit_type == 'Arrendamiento Financiero' or quotation.credit_type == 'Arrendamiento Puro':
                if quotation.credit_type == 'Arrendamiento Financiero':
                    if not quotation.guarantee_percentage:
                        raise Warning('Please provide a Guarantee Porcentage for %s' % quotation.name)
                if not quotation.rents_deposit:
                    raise Warning('Please provide a Rents in deposit for %s' % quotation.name)
                if not quotation.purchase_option:
                    raise Warning('Please provide a Purchase Option for %s' % quotation.name)
                if quotation.credit_type == 'Arrendamiento Puro':
                    if not quotation.residual_porcentage:
                        raise Warning('Please provide a Residual Porcentage for %s' % quotation.name)
            di=quotation.date_start
            df=quotation.date_start
            dpp=quotation.date_first_payment
            diff=dpp- df
            if quotation.calculation_base=='360/360':
                if quotation.include_taxes:
                    dr=(quotation.interest_rate_value / 360 )
                else:
                    dr=(quotation.interest_rate_value / 360 * (1+(quotation.tax_id/100)))
                if quotation.frequency_id.id == 3:
                    dm=30
                    rate=dr/100*30
                if quotation.frequency_id.id == 2:
                    dm=15
                    rate=dr/100*15
                if quotation.frequency_id.id == 1:
                    dm=7
                    rate=dr/100*7
            if quotation.calculation_base=='365/365':
                if quotation.include_taxes:
                    dr=(quotation.interest_rate_value / 365)
                else:
                    dr=(quotation.interest_rate_value / 365 * (1+(quotation.tax_id/100)))
                if quotation.frequency_id.id == 3:
                    dm=calendar.monthrange(di.year,di.month)[1]
                    rate=dr/100*30.5
                if quotation.frequency_id.id == 2:
                    dm=15
                    rate=dr/100*15.25
                if quotation.frequency_id.id == 1:
                    dm=7
                    rate=dr/100*7
                
            if quotation.calculation_base=='360/365':
                if quotation.include_taxes:
                    dr=(quotation.interest_rate_value / 360 )
                else:
                    dr=(quotation.interest_rate_value / 360 * (1+(quotation.tax_id/100)))
                if quotation.frequency_id.id == 3:
                    dm=calendar.monthrange(di.year,di.month)[1]
                    rate=dr/100*30.5
                if quotation.frequency_id.id == 2:
                    dm=15
                    rate=dr/100*15.25
                if quotation.frequency_id.id == 1:
                    dm=7
                    rate=dr/100*7
            amortization_ids = [(5, 0, 0)]
            #amortization_ids.append((0, 0))
            quotation.amortization_ids = amortization_ids
            if quotation.credit_type == 'Arrendamiento Financiero' or quotation.credit_type == 'Arrendamiento Puro':
                quotation.amount_si=quotation.amount/(1+(quotation.tax_id/100))
                ra=quotation.amount_si
                quotation.purchase_option2=quotation.purchase_option/100*ra
                if quotation.credit_type == 'Arrendamiento Puro':
                    quotation.residual_value=ra*quotation.residual_porcentage/100
                if quotation.credit_type == 'Arrendamiento Financiero':
                    quotation.iva=ra*quotation.guarantee_percentage/100
                    quotation.total_guarantee=quotation.iva
                quotation.iva_purchase=quotation.purchase_option2*(quotation.tax_id/100)
                quotation.total_purchase=quotation.purchase_option2+quotation.iva_purchase
                quotation.total_commision=0
                for com in quotation.commision_ids:
                    quotation.total_commision=quotation.total_commision+(com.value_commision)
                if quotation.credit_type == 'Arrendamiento Financiero':
                    pay=((ra*(rate)*pow((1+(rate)),quotation.term))-(0*(rate)))/(pow(1+(rate),quotation.term)-1)
                if quotation.credit_type == 'Arrendamiento Puro':
                    pay=((ra*(rate)*pow((1+(rate)),quotation.term))-(quotation.residual_value*(rate)))/(pow(1+(rate),quotation.term)-1)
            else:
                ra=quotation.amount
                pay=quotation.amount/((1-(1/pow((1+(rate)),quotation.term)))/(rate))
            pay=round(pay,2)
            quotation.tax_amount=pay*(1+(quotation.tax_id/100))
            quotation.payment_amount=pay
            quotation.total_payment=pay+quotation.tax_amount
            for i in range(quotation.term):
                if quotation.frequency_id.id == 3:
                    df = df + relativedelta(months=1)
                if quotation.frequency_id.id == 2:
                    if i%2 == 0:
                        dfq=df
                        df = df + relativedelta(days=15)
                    else:
                         df = dfq + relativedelta(months=1)
                if quotation.frequency_id.id == 1:
                    df = df + relativedelta(days=7)
                if quotation.calculation_base=='365/365' or quotation.calculation_base=='360/365':
                    if quotation.frequency_id.id == 3:
                        dm=calendar.monthrange(df.year,df.month)[1]
                    if quotation.frequency_id.id == 2:
                        if i%2 == 0:
                            dm=15
                        else:
                            dm=(calendar.monthrange(df.year,df.month)[1]-15)
                if i == 0 :
                    dmt=dm
                    dm=diff.days
                    df= di + relativedelta(days=dm)
                else:
                    if quotation.calculation_base =='360/360':
                        dm=dmt
                ici=round(((ra*dr*dm)/100),2)
                if i == (quotation.term-1):
                    if quotation.credit_type == 'Arrendamiento Puro':
                        pay=round(pay,2)
                    else:    
                        pay=round(ra+ici,2)
                else:
                    pay=round(pay,2)
                capital=pay-ici
                interest=round(ici/(1+(quotation.tax_id/100)),2)
                ivainterest=round(ici*(quotation.tax_id/100),2)
                ivacapital=capital*(quotation.tax_id/100)
                fb=ra-capital
                totalrent=0
                ivarent=0
                if quotation.credit_type == 'Arrendamiento Financiero': 
                    totalrent=pay+ivainterest+ivacapital
                if quotation.credit_type == 'Arrendamiento Puro':
                    ivarent=pay*(quotation.tax_id/100)
                    totalrent=pay+ivarent
                amortization_ids = [(4, 0, 0)]
                #data = self._compute_line_data_for_template_change(line)
                data = {
                    'id': '1',
                    'no_payment': (i+1),
                    'date_start': di,
                    'date_end': df,
                    'initial_balance': ra,
                    'daily_rate': dr,
                    'day_interest': dm,
                    'payment': pay,
                    'capital': capital,
                    'interest_iva': ici,
                    'interest': interest,
                    'iva_interest': ivainterest,
                    'iva_capital': ivacapital,
                    'iva_rent': ivarent,
                    'total_rent': totalrent,
                    'final_balance': fb,
                }
                #if self.pricelist_id:
                #    data.update(self.env['sale.order.line']._get_purchase_price(self.pricelist_id, line.product_id, line.product_uom_id, fields.Date.context_today(self)))

                amortization_ids.append((0, 0, data))

                self.amortization_ids = amortization_ids
                
                ra=fb
                di=df 
                if quotation.credit_type == 'Arrendamiento Financiero' or quotation.credit_type == 'Arrendamiento Puro':
                    if i == 0 :   
                        quotation.total_deposit=totalrent*quotation.rents_deposit
                        quotation.total_initial_payments=quotation.total_deposit+quotation.total_commision+quotation.total_guarantee
            
                di=df
                if quotation.credit_type == 'Arrendamiento Financiero' or quotation.credit_type == 'Arrendamiento Puro':
                    if i == 0 :   
                        quotation.total_deposit=totalrent*quotation.rents_deposit
                        quotation.total_initial_payments=quotation.total_deposit+quotation.total_commision+quotation.total_guarantee


    def action_confirm(self):
        self.ensure_one()
        self.opportunity_id.product_id = self.product_id.product_tmpl_id.id
        #self.amount = self.opportunity_id.planned_revenue
        #self.opportunity_id.product_id = self.product_id.id
        res = super(SaleOrder, self).action_confirm()
        return res
        

    @api.depends('partner_id')
    def _compute_amount(self):
        monto = self.env['crm.lead'].search([('id', '=', self.opportunity_id.id)])
        for reg in monto:
            self.amount = monto.planned_revenue
            self.amount_untaxed = monto.planned_revenue

    include_taxes = fields.Boolean('Include Taxes', default=False,  translate=True)
    min_age = fields.Integer('Min. Age')
    max_age = fields.Integer('Max. Age')
    min_amount = fields.Monetary('Min. Amount',  currency_field='company_currency', tracking=True)
    max_amount = fields.Monetary('Max. Amount',  currency_field='company_currency', tracking=True)
    amount = fields.Monetary('Request Amount', currency_field='company_currency', compute = '_compute_amount', store=True, tracking=True)
    amount_si = fields.Monetary('Amount s/iva', currency_field='company_currency', tracking=True)
    payment_amount = fields.Monetary('Payment Amount', currency_field='company_currency', tracking=True)
    tax_amount = fields.Monetary('Tax Amount', currency_field='company_currency', tracking=True)
    total_payment = fields.Monetary('Total Payment', currency_field='company_currency', tracking=True)
    total_commision = fields.Monetary('Total Commision', currency_field='company_currency', tracking=True)
    rents_deposit = fields.Integer('Rents in Deposit', default=0)
    total_deposit = fields.Monetary('Rent Deposit Amount', currency_field='company_currency', tracking=True)
    guarantee_percentage =  fields.Float('Guarantee Percentage', (2,6))
    total_guarantee = fields.Monetary('Total Guarantee Deposit', currency_field='company_currency', tracking=True)
    total_initial_payments = fields.Monetary('Total Initial Payments', currency_field='company_currency', tracking=True)
    date_start = fields.Date('Start Date')
    date_first_payment = fields.Date('First Payment Date')
    frequency_id = fields.Many2one('extenss.product.frequencies') 
    term = fields.Integer('Term', required=True,  default=0)
    calculation_base = fields.Char('Calculation Base')
    interest_rate_value = fields.Float('Interest Rate', (2,6))
    cat = fields.Float('CAT', (2,6))
    current_interest_rate_value = fields.Float('Current Interest Rate', (2,6))
    credit_type = fields.Char('Credit Type')
    base_interest_rate = fields.Char('Base Interest Rate')
    point_base_interest_rate = fields.Char('P. Base Int. Rate')
    tax_id = fields.Float('Tax Rate', (2,6))
    amortization_ids = fields.One2many(
        'extenss.request.amortization', 
        'sale_order_id', 
        string='Amortization Table',)
    
    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    product_id = fields.Many2one('product.product', 'Product Name', required=True)
    
    product_custom_attribute_value_ids = fields.One2many('product.attribute.custom.value', 'sale_order_line_id', string="Custom Values")
    order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    product_no_variant_attribute_value_ids = fields.Many2many('product.template.attribute.value', string="Extra Values", ondelete='restrict')
    hide = fields.Boolean(string="Hide")
    hidepo = fields.Boolean(string="Hide")
    hidevr = fields.Boolean(string="Hide")
    iva = fields.Monetary('IVA',  currency_field='company_currency', tracking=True)
    purchase_option = fields.Float('Purchase Option Porcentage', (2,6))
    purchase_option2 = fields.Monetary('Purchase Option Value', currency_field='company_currency', tracking=True)
    iva_purchase = fields.Monetary('IVA Purchase',  currency_field='company_currency', tracking=True)
    total_purchase =  fields.Monetary('Total Purchase', currency_field='company_currency', tracking=True)
    residual_porcentage = fields.Float('Residual %', (2,6))
    residual_value = fields.Monetary('Residual Value', currency_field='company_currency', tracking=True)
    commision_ids = fields.One2many(
        'extenss.request.commision', 
        'sale_order_id', 
        string='Commision',)

    @api.depends('partner_id')
    def _compute_amount(self):
        monto = self.env['crm.lead'].search([('id', '=', self.opportunity_id.id)])
        for reg in monto:
            self.amount = monto.planned_revenue
            self.amount_untaxed = monto.planned_revenue

    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids
        _logger.debug('Valid Values: %s', valid_values)
       # remove the is_custom values that don't belong to this template
        for pacv in self.product_custom_attribute_value_ids:
            if pacv.custom_product_template_attribute_value_id not in valid_values:
                self.product_custom_attribute_value_ids -= pacv
        # remove the no_variant attributes that don't belong to this template
        for ptav in self.product_no_variant_attribute_value_ids:
            if ptav._origin not in valid_values:
                self.product_no_variant_attribute_value_ids -= ptav
                _logger.debug('No Variant Attribute value ids: ')
        vals = {}

        product = self.product_id.with_context(
            #lang=get_lang(self.env, self.order_id.partner_id.lang).code,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )
        self.term = product.term_extra
        self.credit_type = self.product_id.credit_type.name
        self.calculation_base = self.product_id.calculation_base.name
        self.base_interest_rate = self.product_id.base_interest_rate.name
        self.point_base_interest_rate=self.product_id.point_base_interest_rate
        self.tax_id=self.product_id.taxes_id.amount
        self.min_age=self.product_id.min_age
        self.max_age=self.product_id.max_age
        self.min_amount=self.product_id.min_amount
        self.max_amount=self.product_id.max_amount
        self.frequency_id=product.frequency_extra
        self.interest_rate_value=product.interest_rate_extra
        self.cat=product.cat_extra
        self.include_taxes=self.product_id.include_taxes
        if self.credit_type == 'Credito Simple':
            self.hide = True
        else:
            self.hide = False
        if self.credit_type == 'Arrendamiento Puro' or self.credit_type == 'Credito Simple':
            self.hidepo = True
        else:
            self.hidepo = False
        if self.credit_type == 'Arrendamiento Financiero' or self.credit_type == 'Credito Simple':
            self.hidevr = True
        else:
            self.hidevr = False
        _logger.debug('product Cat Extra: %f', product.cat_extra)
        _logger.debug('product Interest Extra: %f', product.interest_rate_extra)
        _logger.debug('product Taxes: %s', self.product_id.taxes_id.amount)
        _logger.debug('product Frequencys: %s', product.frequency_extra)
        #vals.update(name=self.get_sale_order_line_multiline_description_sale(product))
       
        #self._compute_tax_id()
        self.update(vals)

        title = False
        message = False
        result = {}
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s") % product.name
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.product_id = False

        return result

    #@api.onchange('product_id')
    #def _onchange_product_id(self):
    #    if not self.product_id:
    #        return
    # To compute the dicount a so line is created in cache
    #    self.frequency = self.product_id.lst_price
    #    res = {
    #        'price_unit': self.price_unit,
            #'tax_ids': [(6, 0, self.tax_id.ids)],
    #    }
    #    return res

    #taxes_id = fields.Many2many('account.tax', 'product_taxes_rel', 'prod_id', 'tax_id', help="Default taxes used when selling the product.", string='Customer Taxes',
    #    domain=[('type_tax_use', '=', 'sale')], default=lambda self: self.env.company.account_sale_tax_id)

class SaleOrderAmortization(models.Model):
    _name = "extenss.request.amortization"
    _description = "Extenss Amortization Table Lines"

    sale_order_id = fields.Many2one('sale.order')
    no_payment = fields.Integer('No.')
    date_start = fields.Date('Start Date')
    date_end = fields.Date('End Date')
    initial_balance = fields.Monetary('Initial Balance',currency_field='company_currency', tracking=True)
    daily_rate = fields.Float('Daily Rate', (2,6))
    day_interest = fields.Integer('Days of Interest')
    payment = fields.Monetary('Payment',currency_field='company_currency', tracking=True)
    capital = fields.Monetary('Capital',currency_field='company_currency', tracking=True)
    interest_iva = fields.Float('Interest c/IVA', (2,2))
    interest = fields.Monetary('Interest', currency_field='company_currency', tracking=True)
    iva_interest = fields.Monetary('IVA Interest',currency_field='company_currency', tracking=True)
    iva_capital = fields.Monetary('IVA Capital',currency_field='company_currency', tracking=True)
    iva_rent = fields.Monetary('IVA Rent',currency_field='company_currency', tracking=True)
    total_rent = fields.Monetary('Total Rent',currency_field='company_currency', tracking=True)
    final_balance = fields.Monetary('Final Balance',currency_field='company_currency', tracking=True)
    

    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)

class SaleOrderCommision(models.Model):
    _name = "extenss.request.commision"
    _description = "Extenss Commision"
    

    @api.depends('type_commision','commision')
    def _compute_total_commision(self):
        for reg in self:
            if reg.type_commision == '1':
                reg.value_commision = reg.commision
            else:
                reg.value_commision=reg.sale_order_id.amount*reg.commision/100
                #reg.value_commision = reg.commision_id.amount*commision/100
    
    sale_order_id = fields.Many2one('sale.order')
    detali_commision = fields.Char('Detail Commision')
    type_commision = fields.Selection(COMMISION_TYPE, string='Type Commision', index=True)
    commision = fields.Monetary('Commision',currency_field='company_currency', tracking=True)
    value_commision = fields.Monetary('Commision Value',currency_field='company_currency', tracking=True,compute='_compute_total_commision')

    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)

    @api.constrains('commision')   
    def _check_intrat(self):
        for com in self:
            if not com.detali_commision:
                raise Warning('Please provide a Detail Commision ')
            if not com.type_commision:
                raise Warning('Please provide a Type Commision ')
            if not com.commision:
                raise Warning('Please provide a Commision ')


        

