from odoo import fields, models, tools


class HotelStatistics(models.Model):
    _name = 'hotel.reservation.statistic'
    _auto = False
    res_id = fields.Many2one('hotel.reservation', string="Reservation")
    partner_id = fields.Many2one('res.partner', string="Partner")
    number_of_reserved_rooms = fields.Integer()
    number_of_beds = fields.Integer()

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'hotel_reservation_statistic')
        query = """
             CREATE OR REPLACE VIEW hotel_reservation_statistic AS (
                 SELECT   row_number() OVER () as id,
                         hotel_reservation.id AS res_id , 
                         hotel_reservation.client_name AS partner_id ,
                         SUM(hotel_room.number_of_beds) AS number_of_beds,
                         COUNT(hotel_reservation.id) AS  number_of_reserved_rooms
                 FROM 
                    hotel_reservation 
                    INNER JOIN room_reservation_relation ON (hotel_reservation.id = room_reservation_relation.reservation_id)
                    INNER JOIN hotel_room ON (hotel_room.id = room_reservation_relation.room_id)
                 GROUP BY hotel_reservation.id , hotel_reservation.client_name
             );
             """
        self._cr.execute(query)