import logging
from odoo import api, fields, models, _
from odoo.exceptions import Warning, UserError, ValidationError

_logger = logging.getLogger(__name__)

class ExtenssRequestFrequency(models.Model):
    _name = 'extenss.request.frequency'
    _order = 'name'
    _description = 'Frequency'

    name = fields.Char(string='Frequency', required=True, translate=True)
    days = fields.Char(string='Days', required=True)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_quotation_calculate(self):
        for quotation in self:
            if not quotation.date_start:
                raise Warning('Please provide a Start Date for %s' % quotation.name)
            if not quotation.date_first_payment:
                raise Warning('Please provide a First Payment Date for %s' % quotation.name)
            if not quotation.frequency_id:
                raise Warning('Please provide a Frequency for %s' % quotation.name)
            if quotation.amount <= 0:
                raise ValidationError(_('The Internal Term must be greater than 0'))
        order_lines = [(5, 0, 0)]


        #data = self._compute_line_data_for_template_change(line)
        data = {
            'display_type': 0,
            'name': 'Cuota',
            'state': 'draft',
            'price_unit': 350,
            'discount': 0,
            'product_uom_qty': 1,
            'product_id': 23,
            #'product_uom': 1,
            #'customer_lead': 1,
        }
        #if self.pricelist_id:
        #    data.update(self.env['sale.order.line']._get_purchase_price(self.pricelist_id, line.product_id, line.product_uom_id, fields.Date.context_today(self)))

        order_lines.append((0, 0, data))

        self.order_line = order_lines

        return True

    min_age = fields.Integer('Min. Age', translate=True, readonly=True)
    max_age = fields.Integer('Max. Age',  translate=True, readonly=True)
    min_amount = fields.Monetary('Min. Amount',  currency_field='company_currency', tracking=True, readonly=True)
    max_amount = fields.Monetary('Max. Amount',  currency_field='company_currency', tracking=True, readonly=True)
    amount = fields.Monetary('Request Amount', currency_field='company_currency', tracking=True, required=True)
    payment_amount = fields.Monetary('Payment Amount', currency_field='company_currency', tracking=True, required=True)
    tax_amount = fields.Monetary('Tax Amount', currency_field='company_currency', tracking=True, required=True)
    total_payment = fields.Monetary('Total Payment', currency_field='company_currency', tracking=True, required=True)
    total_commision = fields.Monetary('Total Commision', currency_field='company_currency', tracking=True, required=True)
    rents_deposit = fields.Integer('Rents in Deposit', required=True, readonly=True, default=0)
    total_deposit = fields.Monetary('Request Amount', currency_field='company_currency', tracking=True, required=True)
    guarantee_percentage = fields.Integer('Guarantee Percentage', required=True, readonly=True, default=0)
    total_guarantee = fields.Monetary('Total Guarantee Deposit', currency_field='company_currency', tracking=True, required=True)
    total_initial_payments = fields.Monetary('Total Initial Payments', currency_field='company_currency', tracking=True, required=True)
    date_start = fields.Date('Start Date')
    date_first_payment = fields.Date('First Payment Date')
    frequency_id = fields.Many2one('extenss.request.frequency') 
    term = fields.Integer('Term', required=True, readonly=True, default=0)
    calculation_base = fields.Text('Calculation Base', required=True, readonly=True )
    interest_rate_value = fields.Float('Interest Rate', (2,6))
    current_interest_rate_value = fields.Float('Interest Rate', (2,6))
    credit_type = fields.Text('Credit Type', required=True, readonly=True )
    base_interest_rate = fields.Text('Base Interest Rate', required=True, readonly=True )
    point_base_interest_rate = fields.Text('P. Base Int. Rate', required=True, readonly=True )
    tax_id = fields.Float('Tax Rate', (2,6))
    amortization_ids = fields.One2many(
        'extenss.request.amortization', 
        'amortization_id', 
        string='Amortization Table',)

    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    product_id = fields.Many2one('product.product', 'Product Name', required=True)
    
    product_custom_attribute_value_ids = fields.One2many('product.attribute.custom.value', 'sale_order_line_id', string="Custom Values")
    order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    #partner_id = fields.Many2one(
    #    'res.partner', string='Customer', readonly=True,
    #    states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
    #    required=True, change_default=True, index=True, tracking=1,
    #    domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    # M2M holding the values of product.attribute with create_variant field set to 'no_variant'
    # It allows keeping track of the extra_price associated to those attribute values and add them to the SO line description
    product_no_variant_attribute_value_ids = fields.Many2many('product.template.attribute.value', string="Extra Values", ondelete='restrict')

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
        
        _logger.debug('product Cat Extra: %f', product.cat_extra)
        _logger.debug('product Interest Extra: %f', product.interest_rate_extra)
        _logger.debug('product Taxes: %s', self.product_id.taxes_id.amount)
        #_logger.debug('product Frequencys: %s', product.frequencies_extra)
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

    amortization_id = fields.Many2one('sale.order')
    date_start = fields.Date('Start Date')
    date_end = fields.Date('End Date')
    initial_balance = fields.Monetary('Initial Balance',currency_field='company_currency', tracking=True)

    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    

