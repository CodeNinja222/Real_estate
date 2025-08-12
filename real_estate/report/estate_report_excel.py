from odoo.addons.report_xlsx.report.report_abstract_xlsx import ReportXlsxAbstract

class EstateXlsxReport(ReportXlsxAbstract):
    _name = 'report.real_estate.report_estate_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Estate XLSX Report'

    def generate_xlsx_report(self, workbook, data, estates):
        sheet = workbook.add_worksheet('Estates')
        bold = workbook.add_format({'bold': True})

        # Headers
        sheet.write(0, 0, 'Name', bold)
        sheet.write(0, 1, 'Available From', bold)
        sheet.write(0, 2, 'Price', bold)

        row = 1
        for estate in estates:
            sheet.write(row, 0, estate.name or '')
            sheet.write(row, 1, str(estate.date_availability) or '')
            sheet.write(row, 2, estate.expected_price or 0)
            row += 1


