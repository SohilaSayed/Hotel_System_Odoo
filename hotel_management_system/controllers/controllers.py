# -*- coding: utf-8 -*-
# from odoo import http


# class HotelManagementSystem(http.Controller):
#     @http.route('/hotel_management_system/hotel_management_system', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hotel_management_system/hotel_management_system/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hotel_management_system.listing', {
#             'root': '/hotel_management_system/hotel_management_system',
#             'objects': http.request.env['hotel_management_system.hotel_management_system'].search([]),
#         })

#     @http.route('/hotel_management_system/hotel_management_system/objects/<model("hotel_management_system.hotel_management_system"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hotel_management_system.object', {
#             'object': obj
#         })
