from odoo import models,fields,api


class Type(models.Model):
    _name ="estate.property.type"
    _log_access = False
    _description = "Real Estate Property Type"
    _order = "sequence,name"
    name = fields.Char(required=True)
    sequence = fields.Integer(string="Sequence")
    property_ids=fields.One2many("real.estate.property","property_type")
    offer_ids = fields.One2many('estate.property.offer','property_type_id',string="Offers")
    _sql_constraints=[("type_constraint","unique(name)","the type name must be unique")]
    offer_count = fields.Integer(string="Offer Count",compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
                   
                  
       
           
       
  
  













