from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        comodel_name='real.estate.property',
        inverse_name='salesperson_id',  
        string='Available Properties',
        domain=[('status', 'in', ['new', 'cancelled', 'offer_received'])]
    )
