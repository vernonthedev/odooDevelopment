from odoo import models, fields, api, _


class VendorBid(models.Model):
    _name = 'vendor.bid'
    _description = 'Vendor Bid'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Bid Reference', required=True, copy=False,readonly=True, default=lambda self: _('New'))
    rfq_id = fields.Many2one('purchase.order', string='RFQ')
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True)
    bid_date = fields.Date('Bid Date', default=fields.Date.context_today)
    bid_lines = fields.One2many('vendor.bid.line', 'bid_id', string='Bid Lines')
    total_amount = fields.Float('Total Amount', compute='_compute_total')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent to Vendor'),
        ('received', 'Bid Received'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)

    @api.depends('bid_lines.subtotal')
    def _compute_total(self):
        for bid in self:
            bid.total_amount = sum(line.subtotal for line in bid.bid_lines)