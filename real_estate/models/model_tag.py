from odoo import models,fields


class Tag(models.Model):
    _name ="estate.property.tag"
    _log_access = False
    _description = "Real Estate Property Tag"
    _order = "name"
    name = fields.Char(required=True)
    color = fields.Integer(string="Color")
    _sql_constraints=[("tag_constraint","unique(name)","The name of tag must be unique")]
                   
                  
       
           
       
  
  













