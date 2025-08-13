from odoo.addons.report_xlsx.report.report_abstract_xlsx import ReportXlsxAbstract

class EstateXlsxReport(ReportXlsxAbstract):
    _name = 'report.real_estate.report_estate_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Estate XLSX Report'

    def generate_xlsx_report(self, workbook, data, estates):
        bold = workbook.add_format({'bold': True})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D9E1F2', 'border': 1})
        table_header_format = workbook.add_format({'bold': True, 'bg_color': '#B4C6E7', 'border': 1})
        cell_format = workbook.add_format({'border': 1})
        cell_num_format = workbook.add_format({'border': 1, 'align': 'right'})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'border': 1, 'align': 'center'})

        for estate in estates:
            sheet_name = estate.name[:31] if estate.name else 'Estate'
            sheet = workbook.add_worksheet(sheet_name)

            # Set column widths for better readability
            sheet.set_column('A:A', 20)
            sheet.set_column('B:B', 25)
            sheet.set_column('C:C', 25)
            sheet.set_column('D:D', 20)
            sheet.set_column('E:E', 20)

            row = 0

            # --- Property Info ---
            sheet.merge_range(row, 0, row, 4, "Property Report", header_format)
            row += 2

            sheet.write(row, 0, 'Name', bold)
            sheet.write(row, 1, estate.name or '', cell_format)
            row += 1

            sheet.write(row, 0, 'Price', bold)
            sheet.write(row, 1, estate.selling_price or 0, cell_num_format)
            row += 1

            sheet.write(row, 0, 'Status', bold)
            sheet.write(row, 1, estate.status or '', cell_format)
            row += 1

            sheet.write(row, 0, 'Buyer', bold)
            sheet.write(row, 1, estate.buyer_id.name or '', cell_format)
            row += 1

            sheet.write(row, 0, 'Owner', bold)
            sheet.write(row, 1, estate.owner_id.name or '', cell_format)
            row += 2

            # --- Property Details Table ---
            if estate.details_ids:
                sheet.merge_range(row, 0, row, 4, 'Property Details', header_format)
                row += 1

                sheet.write(row, 0, 'Detail', table_header_format)
                sheet.write(row, 1, 'Count', table_header_format)
                sheet.write(row, 2, 'Remark', table_header_format)
                row += 1

                for detail in estate.details_ids:
                    sheet.write(row, 0, detail.detail_id.name or '', cell_format)
                    sheet.write(row, 1, detail.count or 0, cell_num_format)
                    sheet.write(row, 2, detail.remark or '', cell_format)
                    row += 1
                row += 1

            # --- Offers Table ---
            if estate.offer_ids:
                sheet.merge_range(row, 0, row, 4, 'Offers', header_format)
                row += 1

                sheet.write(row, 0, 'Price', table_header_format)
                sheet.write(row, 1, 'Partner', table_header_format)
                sheet.write(row, 2, 'Deadline', table_header_format)
                sheet.write(row, 3, 'Validity Days', table_header_format)
                sheet.write(row, 4, 'Status', table_header_format)
                row += 1

                for offer in estate.offer_ids:
                    sheet.write(row, 0, offer.price or 0, cell_num_format)
                    sheet.write(row, 1, offer.partner_id.name or '', cell_format)
                    if offer.deadline:
                        sheet.write_datetime(row, 2, offer.deadline, date_format)
                    else:
                        sheet.write(row, 2, '', cell_format)
                    sheet.write(row, 3, offer.validity_days or 0, cell_num_format)
                    sheet.write(row, 4, offer.status or '', cell_format)
                    row += 1
