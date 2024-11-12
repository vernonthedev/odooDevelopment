from odoo import models, fields


class NationalIDApplication(models.Model):
    _name = 'national.id.application'
    _description = 'National ID Application'

    applicant_name = fields.Char(string="Applicant Name", required=True)
    applicant_dob = fields.Date(string="Date of Birth", required=True)
    applicant_email = fields.Char(string="Email Address", required=True)
    applicant_phone = fields.Char(string="Phone Number", required=True)
    applicant_address = fields.Text(string="Address", required=True)
    picture_attachment = fields.Binary(string="Picture", attachment=True)
    lc_reference_letter = fields.Binary(string="LC Reference Letter", attachment=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='draft', string='Status')

    # track the stages
    approval_stage = fields.Selection([
        ('stage_1', 'Stage 1'),
        ('stage_2', 'Stage 2'),
        ('final_approval', 'Final Approval'),
    ], default='stage_1', string='Approval Stage')

    # Tracking approvers
    approvers = fields.One2many('res.users', 'application_id', string='Approvers')
