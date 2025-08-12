from odoo import models,fields,api
from odoo.exceptions import ValidationError,UserError
from odoo.tools.float_utils import float_compare,float_is_zero

class Property(models.Model):
    _name ="real.estate.property"
    _log_access = False
    _order = "id desc"
    name = fields.Char(required=1,string="Name")
    description =fields.Text(required=1)
    postcode =fields.Char(required=1)
    date_availability= fields.Date(default=fields.Date.today(),copy=False)
    expected_price=fields.Float(copy=False)
    selling_price=fields.Float(copy=False)
    bedrooms=fields.Integer(default=2)
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
    property_type=fields.Many2one("estate.property.type",string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer",copy=False)
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    tag_ids= fields.Many2many("estate.property.tag",string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    status=fields.Selection([('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('sold', 'Sold'),
        ('offer_accepted', 'Offer Accepted'),
        ('cancelled','Cancelled')
    ],
    string="Status",
    default='new'
)
    total_area=fields.Float(compute="_compute_total_area")
    best_price=fields.Float(compute="_compute_best_offer",string="Best offer")
    owner_id = fields.Many2one('res.partner', string="Owner",copy=False)
    details_ids=fields.One2many("estate.property.detail", "property_id", string="Details type")
  
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
         # Compute the total area by adding living and garden areas
         for rec in self:
               rec.total_area=rec.living_area+rec.garden_area
              
        


    @api.depends("offer_ids")
    def _compute_best_offer(self):
         # Compute the highest offer price from all related offers
         for rec in self:
              rec.best_price=max(rec.offer_ids.mapped("price") or [0])
         
              
      
    @api.constrains("expected_price")
    def check_expected_price_above0(self):
        # Ensures expected price is positive
        for record in self:
              if record.expected_price<=0 :
                  raise ValidationError("Enter a valid expected_price")
              
    @api.constrains("living_area")
    def check_living_area_above0(self):
        # Ensures living area is positive
        for record in self:
             if record.living_area<=0 :
                    raise ValidationError("Enter a valid living area value")
             
    @api.constrains("bedrooms")
    def check_bedrooms_availability(self):
        # Ensures bedrooms count is positive
        for record in self:
             if record.bedrooms<=0 :
                    raise ValidationError("Enter a valid bedrooms value(must be greater than 0)")
                   
    @api.onchange("garden")
    # Sets default garden area and orientation when garden field changes
    def check_garden_availability(self):
        for rec in self :
               if self.garden:
                    self.garden_area=10
                    self.garden_orientation="north"
               else:
                    self.garden_area=0
                    self.garden_orientation=""
             
      
        
    def cancel_property(self):
        # Cancel the property if not already sold or canceled
        for rec in self:
               if rec.status=="sold":
                    raise UserError("A sold property cannot be cancelled")
               elif rec.status=="canceled":
                    raise UserError("Already canceled property")
               else:
                    rec.status="canceled"
               

    def sold_property(self):
     for property in self:
        if not property.buyer_id:
            raise UserError(f"Property '{property.name}' has no buyer assigned.")
        if property.status != "offer_accepted":
            raise UserError(f"Property '{property.name}' must have status 'offer accepted' before selling.")
        
        property.status = "sold"
     
    
    @api.constrains("expected_price","selling_price")
    def _prevent_expected_price_edit_after_offer(self):
         # Ensures selling price is at least 90% of expected price (if selling price not zero)
         if not float_is_zero(self.selling_price,precision_digits=2):
              min_selling_price=self.expected_price*0.9
              if float_compare(self.selling_price,min_selling_price,precision_digits=2)==-1:
                   raise UserError("Selling price must be at least 90% of the expected price.")
              
    @api.ondelete(at_uninstall=False)
    def _prevent_deletion(self):
        # Prevent deletion unless property is 'new' or 'cancelled'.
        for record in self:
            if record.status not in ['new', 'cancelled']:
                raise UserError(f"You cannot delete a property in state '{record.status}'. Only 'New' or 'Cancelled' properties are allowed.")
            
    def print_property_report(self):
        return self.env.ref('real_estate.action_property_report').report_action(self)
    
    @api.constrains("buyer_id","owner_id")
    def check_owner_buyer_validity(self):
         if self.buyer_id:
              if self.owner_id.name==self.buyer_id.name:
                   raise ValidationError("Buyer should be different from the owner")

