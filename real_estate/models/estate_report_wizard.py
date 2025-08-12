from odoo import models, fields
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class EstateReportWizard(models.TransientModel):
    _name = 'estate.report.wizard'
    _description = 'Estate Report Wizard'

    estate_ids = fields.Many2many('real.estate.property', string='Estates')
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")

    def action_export_excel(self):
        return self.env.ref('real_estate.report_estate_xlsx').report_action(self.estate_ids)

    def print_report(self):
        domain = []
        criteria = {}

        if self.estate_ids:
            domain.append(('id', 'in', self.estate_ids.ids))
            criteria['estate_names'] = ', '.join(self.estate_ids.mapped('name'))
        elif self.from_date and self.to_date:
            domain.append(('date_availability', '>=', self.from_date))
            domain.append(('date_availability', '<=', self.to_date))
            criteria['date_range'] = f"{self.from_date} to {self.to_date}"

        estates = self.env['real.estate.property'].search(domain)

        if not estates:
            raise UserError("No estates found for the given criteria.")

        _logger.info(f"Estates found: {estates.ids}")
        _logger.info(f"Criteria: {criteria}")

        data = {
            'criteria': criteria,
        }

        return self.env.ref('real_estate.action_property_report').report_action(estates, data=data)
