from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vendor_ids = fields.Many2many('res.partner', string='Vendors',domain=[('supplier_rank', '>', 0)])
    purchase_request_id = fields.Many2one('purchase.request',
    purchase_request_id = fields.Many2one('purchase.request',string='Purchase Request')
    bid_ids = fields.One2many('vendor.bid', 'rfq_id', string='Vendor Bids')
    winning_bid_id = fields.Many2one('vendor.bid', string='Winning Bid')
    state = fields.Selection(selection_add=[
        ('bid_selection', 'Bid Selection'),
    ])

    def action_send_to_vendors(self):
        for vendor in self.vendor_ids:
            self.env['vendor.bid'].create({
                'rfq_id': self.id,
                'vendor_id': vendor.id,
                'state': 'sent'
            })

    def action_select_winning_bid(self):
        if self.winning_bid_id:
            self.partner_id = self.winning_bid_id.vendor_id
            self.state = 'purchase'