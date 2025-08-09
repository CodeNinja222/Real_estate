from odoo import models,fields,api
from odoo.exceptions import UserError,ValidationError

class Offer(models.Model):
    _name ="estate.property.offer"
    _log_access = False
    _description = "Real Estate Property offer"
    _order = "price desc"
    price = fields.Float()
    status = fields.Selection([
        ("accepted","Accepted"),("refused","Refused")
    ],default="")
    validity_days=fields.Integer(default=7,string="Validity(days)")
    deadline=fields.Date(required=True)
    partner_id=fields.Many2one("res.partner",required=True)
    property_id=fields.Many2one("real.estate.property",required=True)
    property_type_id = fields.Many2one(related='property_id.property_type',store=True,readonly=True)


    def accepted_offer(self):
        # Accepts the offer if no other accepted offer exists for the property; updates property buyer and price.
        already_accepted = self.env['estate.property.offer'].search_count([
        ('property_id', '=', self.property_id.id),
        ('status', '=', 'accepted'),
        ('id','!=',self.id)
    ])

        if already_accepted:
            raise UserError("This property already has an accepted offer.")
            
        else :
            self.status="accepted"
            self.property_id.buyer_id=self.partner_id
            self.property_id.selling_price=self.price
            self.property_id.status="offer_accepted"
        
    def refuse_offer(self):
        # Refuses the offer if it has not already been accepted or refused.
        if self.status=="accepted":
             raise UserError("This offer  already been accepted")
           
        elif self.status=="refused":
             raise UserError("This offer  already been refused")
        else:
            self.status="refused"
             
             
    @api.constrains("price")
    def check_price_is_positive(self):
        # Validates that the offer price is strictly positive.
        if(self.price<=0):
            raise ValidationError("Offer price must be strictly positive")
        

    @api.model
    def create(self, vals):
        # Ensure offer price is not lower than existing offers and update property state on first offer
        property_id = vals.get('property_id')
        price = vals.get('price')
        property_obj = self.env['real.estate.property'].browse(property_id)

        
        existing_max = max(property_obj.offer_ids.mapped('price') or [0])

        if price < existing_max:
            raise ValidationError("Cannot create offer: Offer is lower than an existing offer.")
            

        if property_obj.status == 'new':
            property_obj.status = 'offer_received'

        return super().create(vals)


    
    
