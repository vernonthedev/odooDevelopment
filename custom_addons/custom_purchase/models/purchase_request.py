from odoo import models, fields, api, _

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'

    name = fields.Char('Request Reference', required=True, readonly=True, default=lambda self: _('New'))
    requesting_employee = fields.Many2one('hr.employee', string='Requesting Employee', required=True)
    department_id = fields.Many2one('hr.department', string='Department')
    request_date = fields.Date('Request Date', default=fields.Date.context_today)
    required_date = fields.Date('Required Date')
    product_lines = fields.One2many('purchase.request.line', 'request_id', string='Products')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rfq_created', 'RFQ Created'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)

    def action_submit_request(self):
        """Submit the purchase request."""
        self.state = 'submitted'

    def action_approve_request(self):
        """Approve the purchase request."""
        self.state = 'approved'

    def action_create_rfq(self):
        """Create RFQ from this purchase request."""
        rfq_vals = {
            'origin': self.name,
            # Additional fields and logic as needed
        }
        rfq = self.env['purchase.order'].create(rfq_vals)


class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'

    request_id = fields.Many2one('purchase.request', string='Purchase Request', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    description = fields.Text('Description')
    quantity = fields.Float('Quantity', required=True, default=1)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
