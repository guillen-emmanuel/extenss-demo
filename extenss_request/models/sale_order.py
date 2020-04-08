from odoo import fields, models
from odoo.exceptions import Warning

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


    amount = fields.Monetary('Request Amount', currency_field='company_currency', tracking=True)
    date_start = fields.Date('Start Date')
    date_first_payment = fields.Date('First Payment Date')
    frequency_id = fields.Many2one('extenss.request.frequency') 
    term = fields.Integer('Term', default=0)
    interest_rate_value = fields.Float('Interest Rate', (2,6))
    amortization_ids = fields.One2many(
        'extenss.request.amortization', 
        'amortization_id', 
        string='Amortization Table',)

    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)

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
    

