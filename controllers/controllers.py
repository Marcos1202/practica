# -*- coding: utf-8 -*-
from odoo import http

# class Practica(http.Controller):
#     @http.route('/practica/practica/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/practica/practica/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('practica.listing', {
#             'root': '/practica/practica',
#             'objects': http.request.env['practica.practica'].search([]),
#         })

#     @http.route('/practica/practica/objects/<model("practica.practica"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('practica.object', {
#             'object': obj
#         })