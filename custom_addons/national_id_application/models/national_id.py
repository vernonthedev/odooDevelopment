from odoo import models, fields, api
from odoo.exceptions import UserError

class NationalIDApplication(models.Model):
    _name = 'national.id.application'
    # add logging
    _inherit = ['mail.thread']
    _description = 'National ID Application'

    # Fields for the applicant's details
    first_name = fields.Char(string="First Name", required=True, tracking=True)
    last_name = fields.Char(string="Last Name", required=True,tracking=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone Number")
    gender = fields.Selection([('male', 'Male'), ('female','Female')])
    fathers_name = fields.Char(string="Father's Name")
    mothers_name = fields.Char(string="Mother's Name")
    address = fields.Text(string="Address")
    date_of_birth = fields.Date(string="Date of Birth")
    picture = fields.Binary(string="Picture")
    lc_reference_letter = fields.Binary(string="LC Reference Letter")

    # Fields to track the status of the application
    # and only track whether it was approved or rejected or still a draft
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string="Status", default='draft', tracking=True, track_visibility='onchange')

    def approve_application(self):
        for record in self:
            if record.state != 'pending':
                raise UserError(_("Application must be in 'Pending Approval' state to be approved."))
            record.state = 'approved'
            record.message_post(body=_("Application approved by %s.") % self.env.user.name, subtype='mail.mt_comment')

    def reject_application(self):
        for record in self:
            if record.state != 'pending':
                raise UserError(_("Application must be in 'Pending Approval' state to be rejected."))
            record.state = 'rejected'
            record.message_post(body=_("Application rejected by %s.") % self.env.user.name, subtype='mail.mt_comment')
    # automatically post a message when the state changes
    def write(self, vals):
        changes = []
        for field in vals:
            old_value = getattr(self, field)  # Current value
            new_value = vals.get(field)  # New value

            if old_value != new_value:
                changes.append(f"Field '{field}' changed from '{old_value}' to '{new_value}'")

        # If changes are made, post them to the chatter
        if changes:
            change_details = "\n".join(changes)
            self.message_post(
                body=f"Changes made by {self.env.user.name}:\n{change_details}",
                subtype_id=self.env.ref('mail.mt_comment').id
            )

        return super(NationalIDApplication, self).write(vals)
