from odoo import api, fields, models

class Buku(models.Model):
    _name = 'zuhalbook.buku'
    _description ='New Description'

    name = fields.Char(string='Nama Buku')
    harga_beli = fields.Integer(string='Harga Modal',required=True)
    harga_jual = fields.Integer(string='Harga Jual',required=True)
    harga_sewa = fields.Integer(string='Harga Sewa',required=True)
    keuntungan = fields.Integer(compute='_compute_keuntungan',string='Keuntungan',required=True)
    genre_id = fields.Many2many(comodel_name='zuhalbook.genre',
                                        string='Genre',
                                        ondelete='cascade')
    
    author_id = fields.Many2many(comodel_name='zuhalbook.author',
                                        string='Author',
                                        ondelete='cascade')

    penerbit_id = fields.Many2one(comodel_name='zuhalbook.penerbit',
                                        string='Penerbit')

    # supplier_id = fields.Many2many(comodel_name='zuhalbook.supplier', string='Supplier')
    stok = fields.Integer(string='Stok')
    daftar = fields.Char(compute='_compute_jml_item', string='Genre')
    
    @api.depends('harga_jual','harga_beli')
    def _compute_keuntungan(self):
        for record in self:
            record.keuntungan = record.harga_jual - record.harga_beli

    @api.depends('genre_id')
    def _compute_jml_item(self):
        for record in self:
            a = self.env['zuhalbook.genre'].search([('buku_id', '=', record.id)]).mapped('name')
            b = len(a)
            record.daftar = a
