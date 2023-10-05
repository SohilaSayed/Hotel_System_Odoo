from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class hotel_room_facility(models.Model):
    _name = 'hotel.room.facility'
    name = fields.Char("Type")


class hotel_room(models.Model):
    _name = 'hotel.room'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    room_number = fields.Integer("Room Number")
    floor_number = fields.Integer("floor number")
    number_of_beds = fields.Integer("number of beds", default=1)
    additional_notes = fields.Text("Notes", groups="hotel_management_system.group_hotel_receptionist")
    num_of_reserved_rooms = fields.Integer(compute='_compute_reserved_rooms_count')
    active = fields.Boolean(default=True)
    name = fields.Char(string="Room Name", compute='_compute_room')

    def _compute_reserved_rooms_count(self):
        reserved = self.env['hotel.room']
        for room in self:
            room.num_of_reserved_rooms = reserved.search_count(
                [('room_state', '=', 'reserved')]
            )

    room_state = fields.Selection(
        [
            ('unoccupied', 'Unoccupied'),
            ('occupied', 'Occupied'),
            ('reserved', 'Reserved'),
            ('under_maintenance', 'Under maintenance'),
        ]
        ,default="unoccupied"
    )
    room_type = fields.Selection(
        [
            ('regular', 'regular'),
            ('deluxe', 'deluxe'),
            ('suite', 'suite'),
        ]
        ,default="regular"
    )
    room_view = fields.Selection(
        [
            ('garden_view', 'garden view'),
            ('pool_view', 'pool view'),
        ]
        ,default="garden_view"
    )
    _sql_constraints = [
        ('room_number_uniq', 'UNIQUE(room_number)', 'Room Number must be unique')
    ]
    tags = fields.Many2many('hotel.room.facility', string="Room Tags")
    reservation = fields.Many2many('hotel.reservation')
    checkin_date = fields.Date(related='reservation.checkin_date')

    @api.depends("floor_number", "room_number")
    def _compute_room(self):
        for record in self:
            record.name = str(record.floor_number) + "/" + str(record.room_number)

    def change_state(self, new_state):
        for hotel in self:
            if hotel.room_state == "reserved":
                hotel.room_state = new_state
            if hotel.room_state == "occupied":
                hotel.room_state = new_state

    def view_history(self):
        confirm_count = 0
        cancel_count = 0
        records = self.env['hotel.reservation'].search(
            [('room_ids.room_number', '=', self.room_number)])
        for record in records:
            if record.state == 'confirmed':
                confirm_count += 1
            elif record.state == 'cancel':
                cancel_count += 1
        return {
            'name': f'History --> Room Number: {self.room_number} Confirmed:{confirm_count} / Canceled:{cancel_count}',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.reservation',
            'view_mode': 'tree',
            'view_type': 'tree',
            'domain': [('room_ids.room_number', '=', self.room_number)],
            'target': 'new'
        }

    def make_occupied(self):
        checkin_list = []
        records = self.env['hotel.reservation'].search([('room_ids', '=', self.name)])
        for record in records:
            if record.state == "confirmed":
                checkin_list.append(record.checkin_date)

        for hotel in checkin_list:
            if hotel == fields.Date.today():
                self.change_state('occupied')
        # else:
        #    msg = _('Error! You cannot check in  as the checkin date is on %s') % hotel
        #   raise UserError(msg)

    def make_unoccupied(self):
        self.change_state('unoccupied')
