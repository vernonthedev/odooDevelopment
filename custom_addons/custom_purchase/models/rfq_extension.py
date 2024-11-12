# models/rfq_extension.py
from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vendor_ids = fields.Many2many(
        'res.partner', string="Vendors", domain="[('supplier_rank', '>', 0)]",
        help="Vendors who will receive this RFQ."
    )

    bid_ids = fields.One2many('purchase.bid', 'rfq_id', string="Bids")
    winning_bid_id = fields.Many2one('purchase.bid', string="Winning Bid")

    def action_select_winning_bid(self, bid_id):
        """Select a winning bid and create a Purchase Order."""
        bid = self.env['purchase.bid'].browse(bid_id)
        self.winning_bid_id = bid
        # Create the Purchase Order logic if needed



class PurchaseBid(models.Model):
    _name = 'purchase.bid'
    _description = 'Purchase Bid'

    name = fields.Char("Bid Reference", required=True)
    rfq_id = fields.Many2one('purchase.order', string="RFQ", required=True)
    vendor_id = fields.Many2one('res.partner', string="Vendor", required=True)
    bid_date = fields.Date("Bid Date", default=fields.Date.today)
    total_amount = fields.Float("Total Amount")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected')
    ], string="Status", default='draft')

    def action_select_as_winner(self):
        self.state = 'selected'
        self.rfq_id.action_select_winning_bid(self.id)
