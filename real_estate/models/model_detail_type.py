from odoo import models,fields
from odoo.exceptions import ValidationError

class DetailsType(models.Model):
    _name ="estate.property.detail.type"
    _log_access = False
    _description = "Real Estate Property detail name"
    name=fields.Char(required=True)
    _sql_constraints=[("type_constraint","unique(name)","the detail type is already founded")]

   
   

    
                   
                  
       
           
       
  
  













