from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class Peminjaman(models.Model):
    _name = 'zuhalbook.peminjaman'
    _description = 'peminjaman'

    name = fields.Char(string='No. Nota')
    konsumen_id = fields.Many2one(comodel_name='zuhalbook.konsumen',
                                        string='Konsumen')

    tgl_peminjaman = fields.Datetime(
        string='Tanggal Peminjaman',
        default=fields.Datetime.now())
    
    tgl_pengembalian = fields.Datetime(
        string='Tanggal Pengembalian')
    total_bayar = fields.Integer(
        string='Total Pembayaran',
        compute='_compute_totalbayar')
    total_keuntungan = fields.Integer(
        string='Total Keuntungan',
        compute='_compute_totalbayar')    
    detailpeminjaman_ids = fields.One2many(
        comodel_name='zuhalbook.detailpeminjaman',
        inverse_name='peminjaman_id',
        string='Detail peminjaman')
    state = fields.Selection([
        ('draft', 'Draft'),('confirm', 'Confirm'),('done', 'Done'),('cancelled', 'Cancelled')
    ], string='Status', required=True, readonly=True, default="draft")

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_confirm(self):
        self.write({'state': 'confirm'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancelled(self):
        self.write({'state': 'cancelled'})    

    @api.depends('detailpeminjaman_ids')
    def _compute_totalbayar(self):
        for line in self:
            result = sum(self.env['zuhalbook.detailpeminjaman'].search(
                [('peminjaman_id', '=', line.id)]).mapped('subtotal'))
            line.total_bayar = result
            line.total_keuntungan = result


    @api.ondelete(at_uninstall=False)
    def __ondelete_peminjaman(self):
        if self.filtered(lambda line: line.state != 'draft'):
            raise ValidationError("Tidak dapat menghapus jika bukan status draft")
        if self.detailpeminjaman_ids:
            peminjaman = []
            for line in self:
                peminjaman = self.env['zuhalbook.detailpeminjaman'].search(
                    [('peminjaman_id', '=', line.id)])
                print(peminjaman)

            for ob in peminjaman:
                print(ob.buku_id.name + ' ' + str(ob.qty))
                ob.buku_id.stok += ob.qty

    def write(self,vals):
        for rec in self:
            a = self.env['zuhalbook.detailpeminjaman'].search([('peminjaman_id','=',rec.id)])
            print(a)
            for data in a:
                data.buku_id.stok += data.qty

        # default write atau edit (proses update dari data yg dimasukkan) 
        record = super(Peminjaman,self).write(vals)
        for rec in self:
            b = self.env['zuhalbook.detailpeminjaman'].search([('peminjaman_id','=',rec.id)])

            for databaru in b:
                if databaru in a:
                    databaru.buku_id.stok -= databaru.qty
            else:
                pass
        # default write juga (harus ada return)
        return record        

    # constrains pada sql (menjadikan sebuah atribut pada tabel menjadi khusus ch : unique)
    _sql_constrains = [
        ('no_nota_unik','unique(name)','Nomor Nota Tidak Boleh Sama!!!!!')
    ]

class DetailPeminjaman(models.Model):
    _name = 'zuhalbook.detailpeminjaman'
    _description = 'Detail'

    name = fields.Char(string='Nama')
    peminjaman_id = fields.Many2one(
        comodel_name='zuhalbook.peminjaman',
        string='Detail peminjaman')
    buku_id = fields.Many2one(
        comodel_name='zuhalbook.buku',
        string='List buku')
    harga_satuan = fields.Integer(
        string='Harga Satuan',
        onchange='_onchange_buku_id')
    qty = fields.Integer(string='Quantity')
    subtotal = fields.Integer(compute='_compute_subtotal', string='Subtotal')

    @api.depends('harga_satuan', 'qty')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.qty * line.harga_satuan

    @api.onchange('buku_id')
    def _onchange_buku_id(self):
        if self.buku_id.harga_sewa:
            self.harga_satuan = self.buku_id.harga_sewa


    @api.model
    def create(self, vals):
        # default create 
        record = super(DetailPeminjaman, self).create(vals)
        if record.qty:
            # Mendapatkan data berdasarkan ID pada buku_id
            self.env['zuhalbook.buku'].search(
                [('id', '=', record.buku_id.id)]
            ).write({'stok': record.buku_id.stok - record.qty})
        # default create juga (harus ada return)
        return record

    # constrains pada python 
    @api.constrains('qty')
    def check_quantity(self):
        for rec in self:
            if rec.qty < 1:
                raise ValidationError("Mau Belanja {} Berapa Banyak Sih...".format(rec.buku_id.name))
            elif rec.buku_id.stok == 0:
                raise ValidationError("Stok {} Habis, Silahkan Pilih buku yang Lain Yaaa...".format(rec.buku_id.name))    
            elif rec.qty > rec.buku_id.stok:
                raise ValidationError("Stok {} Tidak Mencukupi, Hanya Ada {}".format(rec.buku_id.name,rec.buku_id.stok))
