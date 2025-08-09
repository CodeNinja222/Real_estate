from odoo import models,Command,fields

class EstateProperty(models.Model):
    _inherit = "real.estate.property"

    def sold_property(self):
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)

        for property in self:
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': property.buyer_id.id,
                'journal_id': journal.id,
                'invoice_date': fields.Date.context_today(self),
                'invoice_line_ids': [
                    Command.create({
                        'name': f'Commission (6%) for {property.name}',
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ],
            }

            invoice = self.env['account.move'].create(invoice_vals)
            invoice.action_post() 

        return super().sold_property()
