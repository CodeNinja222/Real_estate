from odoo import models,fields,api
from odoo.exceptions import UserError,ValidationError

class Details(models.Model):
    _name ="estate.property.detail"
    _log_access = False
    _description = "Real Estate Property detail"
    detail_id=fields.Many2one("estate.property.detail.type",string="Property detail")
    count=fields.Integer(required=1,default=1)
    remark=fields.Text()
    property_id=fields.Many2one("real.estate.property",required=True)
    @api.constrains("count")
    def check_count_above0(self):
        # Ensures expected price is positive
        for record in self:
              if record.count<=0 :
                  raise ValidationError("Enter a valid count")
   

    
                   
                  
       
           
       
  
  













