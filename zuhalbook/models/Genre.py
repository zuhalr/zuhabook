from odoo import api, fields, models

class Genre(models.Model):
    _name = 'zuhalbook.genre'
    _description ='New Description'
       
    name = fields.Char( string='Nama Genre')

    kode_genre = fields.Char( string='Kode Genre')
       
    kode_rak = fields.Char(string='Kode Rak')
    buku_id = fields.Many2many(comodel_name='zuhalbook.buku',
                                string='Daftar Buku')

    jml_item = fields.Char(compute='_compute_jml_item', string='Jml Item')
    
		# Perubahannya di sini
    @api.depends('buku_id')
    def _compute_jml_item(self):
        for record in self:
            a = self.env['zuhalbook.buku'].search([('genre_id', '=', record.id)]).mapped('name')
            b = len(a)
            record.jml_item = b
     
