from odoo import models, fields, api

class NationalIDApplication(models.Model):
    _name = 'national.id.application'
    # add logging
    _inherit = ['mail.thread']
    _description = 'National ID Application'

    # Fields for the applicant's details
    first_name = fields.Char(string="First Name", required=True, tracking=True)
    last_name = fields.Char(string="Last Name", required=True,tracking=True)
    email = fields.Char(string="Email",tracking=True)
    phone = fields.Char(string="Phone Number",tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female','Female')],tracking=True)
    fathers_name = fields.Char(string="Father's Name",tracking=True)
    mothers_name = fields.Char(string="Mother's Name",tracking=True)
    address = fields.Text(string="Address",tracking=True)
    date_of_birth = fields.Date(string="Date of Birth",tracking=True)
    picture = fields.Binary(string="Picture")
    lc_reference_letter = fields.Binary(string="LC Reference Letter")

    # Fields to track the status of the application
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string="Status", default='draft')

    # To automatically post a message when the state changes
    def write(self, vals):
        # Check if the state is being updated
        if 'state' in vals:
            state_before = self.state
            state_after = vals['state']
            if state_before != state_after:
                self.message_post(
                    body=f"State changed from {state_before} to {state_after}.",
                    subtype_id=self.env.ref('mail.mt_comment').id
                )
        return super(NationalIDApplication, self).write(vals)
