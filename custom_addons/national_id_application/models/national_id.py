from odoo import models, fields, api

class NationalIDApplication(models.Model):
    _name = 'national.id.application'
    _description = 'National ID Application'

    # Fields for the applicant's details
    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
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
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string="Status", default='draft')
