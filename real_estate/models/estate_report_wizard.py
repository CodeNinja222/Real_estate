from odoo import models, fields, api

class EstateReportWizard(models.TransientModel):
    _name = 'estate.report.wizard'
    _description = 'Estate Report Wizard'

    estate_ids = fields.Many2many('real.estate.property', string='Estates')

    def print_report(self):
       
        return self.env.ref('real_estate.action_property_report').report_action(self.estate_ids, config=False)

