from odoo import api,fields, models, _

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment Information'

    sl_no = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True,
                        index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('sl_no', _('New')) == _('New'):
            vals['sl_no'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        res = super(HospitalAppointment, self).create(vals)
        return res

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    appointment_date = fields.Date(string='Appointment Date')
    booking_date = fields.Date(string='Booking Date')
    age = fields.Integer(string='Age')