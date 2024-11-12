from odoo import models, fields, api, _


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Request Reference', required=True, copy=False,readonly=True, default=lambda self: _('New'))
    requesting_employee = fields.Many2one('hr.employee', string='Requesting Employee',required=True)
    department_id = fields.Many2one('hr.department', string='Department')
    request_date = fields.Date('Request Date', default=fields.Date.context_today)
    required_date = fields.Date('Required Date')
    product_lines = fields.One2many('purchase.request.line', 'request_id',string='Products')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rfq_created', 'RFQ Created'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request') or _('New')
        return super(PurchaseRequest, self).create(vals)