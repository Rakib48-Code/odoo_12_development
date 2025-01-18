from odoo import api, fields, models, _
from odoo.exceptions import  ValidationError

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient Information'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', track_visibility=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender')
    ref = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                      index=True, default=lambda self: _('New'))
    age_group = fields.Selection(
        [
            ('minor', 'Minor'),
            ('major', 'Major'),
        ], string='Age Group', compute='age_group_set')
    note = fields.Text(string='Description')

    image = fields.Binary(string='Image')
    sl_no = fields.Char(string='Patient ID', required=True, copy=False, readonly=True,
                        index=True, default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft')

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Patient Created'
        # Assign a sequence to 'sl_no' if it is 'New' or not provided
        if vals.get('sl_no', _('New')) == _('New'):
            vals['sl_no'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        if vals.get('ref', _('New')) == _('New'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('patient.ref') or _('New')
        # Call the original create method
        return super(HospitalPatient, self).create(vals)

    # for smart button and this is type object
    @api.multi
    def open_patient_appointment(self):
        return  {
            'name': _('Appointments'),
            'domain': [],
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    @api.onchange('age')
    def age_group_set(self):
        for rec in self:
            if rec.age:
                if rec.age < 18:
                    rec.age_group = 'minor'
                else:
                    rec.age_group = 'major'

    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age <= 0:  # Check if the age is less than or equal to 0
                raise ValidationError(_('The age must be greater than 0.'))

    # for button actions
    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'