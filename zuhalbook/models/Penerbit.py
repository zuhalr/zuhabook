from odoo import api, fields, models


class Penerbit(models.Model):
    _name = 'zuhalbook.penerbit'
    _description = 'New Description'

    name = fields.Char(string='Nama Penerbit')
    alamat = fields.Char(string='Alamat')
    no_telp = fields.Char(string='No. Telepon')
    buku_ids = fields.One2many(comodel_name='zuhalbook.buku',inverse_name='penerbit_id', string='Buku')