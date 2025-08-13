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
    salesman_id = fields.Many2one(
        'res.users',
        string="Salesman",
        domain=lambda self: self._get_salesman_domain()
    )

    def _get_salesman_domain(self):
        # Only include users who are linked to at least one property
        salesman_ids = self.env['real.estate.property'].search([]).mapped('salesperson_id').ids
        return [('id', 'in', salesman_ids)]

    def action_export_excel(self):
        return self.env.ref('real_estate.report_estate_xlsx').report_action(self.estate_ids)

    def print_report(self):
        domain = []
        criteria = {}

        if self.estate_ids:
            # Case 1: Specific estates selected
            domain.append(('id', 'in', self.estate_ids.ids))
            criteria['estate_names'] = ', '.join(self.estate_ids.mapped('name'))

        elif self.from_date and self.to_date and self.salesman_id:
            # Case 2: Salesman + date range
            domain.append(('salesperson_id', '=', self.salesman_id.id))
            domain.append(('date_availability', '>=', self.from_date))
            domain.append(('date_availability', '<=', self.to_date))
            criteria['salesman'] = self.salesman_id.name
            criteria['date_range'] = f"{self.from_date} to {self.to_date}"

        elif self.from_date and self.to_date:
            # Case 3: Date range only
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
