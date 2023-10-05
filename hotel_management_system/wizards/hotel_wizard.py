from odoo import fields, models


class HotelWizard(models.TransientModel):
    _name = 'reservation.report'

    reservation_from = fields.Date("Reservation Date From", required=True)
    reservation_to = fields.Date("Reservation Date To", required=True)
    client = fields.Many2one('res.partner', string="Client")
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('cancled', 'Cancled')])

    def print_report(self):
        domain = [('reservation_date', '>', self.reservation_from),
                  ('reservation_date', '<', self.reservation_to)
                  ]
        if self.client.id:
            domain.append(('client_name', '=', self.client.id))
        if self.state:
            domain.append(('state', '=', self.state))
        reservations = self.env['hotel.reservation'].search(domain)
        return reservations
