from odoo import models,fields

class PartnerXlsx(models.AbstractModel):
    _name = 'report.zuhalbook.report_penjualan_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    tgl_lap = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, penjualan):
        sheet = workbook.add_worksheet('Daftar penjualan')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, 'Tanggal Laporan : '+ str(self.tgl_lap))
        sheet.write(2, 0, 'No Nota',bold)
        sheet.write(2, 1, 'Nama Pembeli',bold)
        sheet.write(2, 2, 'Tanggal Transaksi',bold)
        sheet.write(2, 3, 'Total Pembayaran',bold)
        sheet.write(2, 4, 'Produk yang Dibeli',bold)
        row = 3
        col = 0 
        for obj in penjualan:
            sheet.write(row, col, obj.name)
            sheet.write(row, col+1, obj.konsumen_id)
            sheet.write(row, col+2, str(obj.tgl_penjualan))
            sheet.write(row, col+3, obj.total_bayar)
            for buku in obj.detailpenjualan_ids:
                sheet.write(row, col+4, buku.buku_id.name)
                row += 1
            row += 1 