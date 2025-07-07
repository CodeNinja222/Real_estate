from odoo import models,fields,api
from odoo.exceptions import ValidationError
from datetime import date
class Property(models.Model):
    _name ="real.estate.property"
    _log_access = False
    name = fields.Char(required=1)
    description =fields.Text(required=1)
    postcode =fields.Char(required=1)
    date_availability= fields.Date(default=date.today())
    expected_price=fields.Float(required=1)
    selling_price=fields.Float()
    bedrooms=fields.Integer()
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    garden_orientation=fields.Selection([
        ("north","North"),
        ("south","South"),
        ("east","East"),
        ("west","West")
    ],default="north")
    bedrooms=fields.Integer()
    @api.constrains("expected_price","living_area","bedrooms")
    def check_expected_price_above0(self):
        for record in self:
              if record.expected_price<=0 :
                  raise ValidationError("Enter a valid expected_price")
              if record.living_area<=0 :
                    raise ValidationError("Enter a valid living area value")
              if record.bedrooms<=0 :
                    raise ValidationError("Enter a valid bedrooms value(must be greater than 0)")
                   
    @api.constrains("garden","garden_area")
    def check_garden_availability(self):
        for record in self:
              if not record.garden and record.garden_area>0:
                  raise ValidationError("The garden area must be 0 if no garden choosen for this property")
              elif record.garden and  record.garden_area<=0:
                    raise ValidationError("The garden area must be greater than 0 when you choose garden option for this property")
                   
                  
       
           
       
  
  













