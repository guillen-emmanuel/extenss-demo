from odoo import fields, models

class ExtenssRequestDestination(models.Model):
    _name =  'extenss.request.destination'

    _order = 'name'
    _description = 'Loan Destination'

    name = fields.Char(string='Loan Destination', required=True, translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)

class Lead(models.Model):
    _inherit = "crm.lead"
    destination_id = fields.Many2one('extenss.request.destination')
