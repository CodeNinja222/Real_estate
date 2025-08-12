from odoo import models
import logging

_logger = logging.getLogger(__name__)

class EstateReport(models.AbstractModel):
    _name = 'report.real_estate.report_property_document'
    _description = 'Estate Property Report'

    def _get_report_values(self, docids, data=None):
        _logger.info(f"Report _get_report_values called with docids: {docids}")
        _logger.info(f"Report _get_report_values called with data: {data}")
        if not docids:
            docids = data.get('context', {}).get('active_ids', [])
        estates = self.env['real.estate.property'].browse(docids)
        criteria = data.get('criteria', {}) if data else {}

        _logger.info(f"Number of estates found: {len(estates)}")
        for estate in estates:
            _logger.info(f"Estate: {estate.id} - {estate.name}")

        return {
            'doc_ids': docids,
            'doc_model': 'real.estate.property',
            'docs': estates,
            'data': data or {},
            'criteria': criteria,
        }
