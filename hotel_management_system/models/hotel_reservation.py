from datetime import datetime

from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class HotelReservation(models.Model):
    _name = 'hotel.reservation'
    _inherit = 'mail.thread'
    _rec_name = 'checkin_date'
    room_ids = fields.Many2many("hotel.room", 'room_reservation_relation', 'reservation_id', 'room_id',
                                 string="Room Name")
    client_name = fields.Many2one('res.partner', string="Client Name", required=True)
    phone_number = fields.Char(related="client_name.phone")
    reservation_date = fields.Date("Reservation Date")
    checkin_date = fields.Date("Check In Date")
    checkout_date = fields.Datetime("Check Out Date", required=True)
    attachment_ids = fields.One2many('ir.attachment', 'res_id', string="Attachments",domain=[('res_model', '=', 'hotel.reservation')])
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('cancel', 'Cancel'),
        ]
        ,default="draft"
    )
    employee_name = fields.Many2one('hr.employee',string="Employee")

    @api.onchange('client_name')
    def _onchange_client_name(self):
        self.reservation_date = False
        self.checkin_date = False

    def change_state(self, new_state):
        for hotel in self:
            if hotel.state == "draft" or hotel.state == "confirmed":
                hotel.state = new_state

    def make_confirmed(self):
        if self.checkin_date >= self.reservation_date:
            for room in self.room_ids:
                if room.room_state == 'reserved':
                    raise models.ValidationError(
                        'Error! This room is already reserved')
                else:
                    self.change_state('confirmed')
                    room.room_state = "reserved"
                    self.state = "confirmed"
        else:
            raise models.ValidationError(
                'Error! check in date before reservation date')

    def make_draft(self):
        self.change_state('draft')
        self.room_ids.room_state = "unoccupied"
        self.state = "draft"

    def cancel_reservation(self):
        if self.checkout_date >= fields.Datetime.now():
            for room in self.room_ids:
                if room.room_state == 'occupied':
                    raise models.ValidationError(
                        'Error! You cannot cancel as one of the rooms is checked in')
                else:
                    self.change_state('cancel')
                    self.room_ids.room_state = "unoccupied"
                    self.state = "cancel"
        else:
            raise models.ValidationError(
                'Cannot cancel reservation after checkout time.')
