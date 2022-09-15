from odoo import api, fields, models


class Person(models.Model):
    _name = 'zuhalbook.person'
    _description = 'New Description'

    name = fields.Char(string='Nama')
    alamat = fields.Char(string='Alamat')
    tgl_lahir = fields.Datetime(string='Tanggal Lahir')


class Kasir(models.Model):
    _name = 'zuhalbook.kasir'
    _inherit = 'zuhalbook.person'
    _description = 'New Description'

    id_kasir = fields.Char(string='ID Kasir')


class CleaningService(models.Model):
    _name = 'zuhalbook.cleaningservice'
    _inherit = 'zuhalbook.person'
    _description = 'New Description'

    id_cln = fields.Char(string='ID Cleaning Service')

class Konsumen(models.Model):
    _name = 'zuhalbook.konsumen'
    _inherit = 'zuhalbook.person'
    _description = 'New Description'

    id_konsumen = fields.Char(string='ID Konsumen')
    penjualan_ids = fields.One2many(comodel_name='zuhalbook.penjualan',inverse_name='konsumen_id', string='Pembelian')
    peminjaman_ids = fields.One2many(comodel_name='zuhalbook.peminjaman',inverse_name='konsumen_id', string='Peminjaman')

class Author(models.Model):
    _name = 'zuhalbook.author'
    _inherit = 'zuhalbook.person'
    _description = 'New Description'

    id_author = fields.Char(string='ID Author')
    buku_id = fields.Many2many(comodel_name='zuhalbook.buku',
                                string='Daftar Buku')