from odoo import models,fields

class PartnerXlsx(models.AbstractModel):
    _name = 'report.zuhalbook.report_buku_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    tgl_lap = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, buku):
        sheet = workbook.add_worksheet('Daftar Buku')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, 'Tanggal Laporan : '+ str(self.tgl_lap))
        sheet.write(2, 0, 'Judul Buku',bold)
        sheet.write(2, 1, 'Harga Jual',bold)
        sheet.write(2, 2, 'Harga Beli',bold)
        sheet.write(2, 3, 'Genre',bold)
        sheet.write(2, 4, 'Author',bold)
        sheet.write(2, 5, 'penerbit',bold)
        sheet.write(2, 6, 'Stok',bold)
        row = 3
        col = 0 
        for obj in buku:
            sheet.write(row, col, obj.name)
            sheet.write(row, col+1, obj.harga_jual)
            sheet.write(row, col+2, obj.harga_beli)
            sheet.write(row, col+3, obj.daftar)
            sheet.write(row, col+4, obj.daftar)
            sheet.write(row, col+5, obj.penerbit_id)
            sheet.write(row, col+6, obj.stok)
            # for barang in obj.barang_id:
            #     sheet.write(row, col+3, barang.name)
            #     row += 1
            row += 1 