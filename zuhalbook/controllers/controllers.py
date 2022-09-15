# -*- coding: utf-8 -*-
# from odoo import http


# class Zuhalbook(http.Controller):
#     @http.route('/zuhalbook/zuhalbook', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zuhalbook/zuhalbook/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('zuhalbook.listing', {
#             'root': '/zuhalbook/zuhalbook',
#             'objects': http.request.env['zuhalbook.zuhalbook'].search([]),
#         })

#     @http.route('/zuhalbook/zuhalbook/objects/<model("zuhalbook.zuhalbook"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zuhalbook.object', {
#             'object': obj
#         })
