from odoo import models,fields

class PartnerXlsx(models.AbstractModel):
    _name = 'report.zuhalbook.report_genre_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    tgl_lap = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, genre):
        sheet = workbook.add_worksheet('Daftar Genre')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, 'Tanggal Laporan : '+ str(self.tgl_lap))
        sheet.write(2, 0, 'Nama Perusahaan',bold)
        sheet.write(2, 1, 'Alamat',bold)
        sheet.write(2, 2, 'No. Hp',bold)
        sheet.write(2, 3, 'Produk',bold)
        row = 3
        col = 0 
        for obj in genre:
            sheet.write(row, col, obj.name)
            sheet.write(row, col+1, obj.kode_genre)
            sheet.write(row, col+1, obj.kode_rak)
            for barang in obj.buku_id:
                sheet.write(row, col+3, barang.name)
                row += 1
            row += 1 