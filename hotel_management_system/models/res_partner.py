from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    reservation_ids = fields.Many2one("hotel.reservation")
    reservation_history_ids = fields.One2many(
        comodel_name='hotel.reservation',
        inverse_name='client_name',
        string='Reservation History',
    )
