# -*- coding: utf-8 -*-

#from asyncio.windows_events import NULL
from multiprocessing import context
from odoo import models, fields, api
from odoo.tools import float_compare, float_round, float_is_zero
from odoo.addons.mrp_workorder.models.mrp_workorder import MrpProductionWorkcenterLine as original

class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.workorder'
    #_description = 'test_module.test_module'

    package_id = fields.Many2one('stock.quant.package',readonly=False)
    location_id = fields.Many2one(related='move_id.move_line_ids.location_id', readonly=False)

    def _create_extra_move_lines(self):
        """Create new sml if quantity produced is bigger than the reserved one"""
        vals_list = []
        # apply putaway
        location_dest_id = self.move_id.location_dest_id._get_putaway_strategy(self.product_id)
        quants = self.env['stock.quant']._gather(self.product_id, self.move_id.location_id, lot_id=self.lot_id, strict=False)
        # Search for a sub-locations where the product is available.
        # Loop on the quants to get the locations. If there is not enough
        # quantity into stock, we take the move location. Anyway, no
        # reservation is made, so it is still possible to change it afterwards.
        vals = {
            'move_id': self.move_id.id,
            'product_id': self.move_id.product_id.id,
            'location_dest_id': location_dest_id.id,
            'product_uom_qty': 0,
            'product_uom_id': self.move_id.product_uom.id,
            'lot_id': self.lot_id.id,
            'recibir':self.package_id.id,
            'package_id':self.package_id.id,
            'company_id': self.move_id.company_id.id,
        }
        for quant in quants:
            quantity = quant.quantity - quant.reserved_quantity
            quantity = self.product_id.uom_id._compute_quantity(quantity, self.product_uom_id, rounding_method='HALF-UP')
            rounding = quant.product_uom_id.rounding
            if (float_compare(quant.quantity, 0, precision_rounding=rounding) <= 0 or
                    float_compare(quantity, 0, precision_rounding=self.product_uom_id.rounding) <= 0):
                continue
            vals.update({
                'location_id': quant.location_id.id,
                'qty_done': min(quantity, self.qty_done),
            })

            vals_list.append(vals)
            self.qty_done -= vals['qty_done']
            # If all the qty_done is distributed, we can close the loop
            if float_compare(self.qty_done, 0, precision_rounding=self.product_id.uom_id.rounding) <= 0:
                break

        if float_compare(self.qty_done, 0, precision_rounding=self.product_id.uom_id.rounding) > 0:
            vals.update({
                'location_id': self.move_id.location_id.id,
                'qty_done': self.qty_done,
            })

            vals_list.append(vals)
        return vals_list

    original._create_extra_move_lines = _create_extra_move_lines

    @api.onchange('lot_id')
    def _update_component_quantity_lot(self):
        self.ensure_one()
        for wo in self:
            if wo.lot_id:
                wo.qty_done = wo.move_id.quantity_done
                #wo.component_remaining_qty = wo.move_id.quantity_done
                wo.qty_done = wo.component_remaining_qty
                if wo.qty_done == 0.0000:
                    wo.qty_done = 1
                    if wo.qty_done==1:
                        wo.component_remaining_qty = 2
                        if wo.component_remaining_qty==2:
                            wo._next(continue_production=True)
                            #anadir condicion para llevarlo a 0#
    
    @api.onchange('package_id')
    def _update_component_quantity_lot_pa(self):
        for r in self:
            if r.package_id:
                if r.qty_done <= -1:
                    r.qty_done = 0
                    if r.qty_done==0:
                        r.component_remaining_qty = 0

class recibirdatolineas(models.Model):
    _inherit = "stock.move.line"

    recibir = fields.Integer()

#    @api.onchange('lot_id')
 #   def _update(self):
  #      for r in self:
   #         if r.package_id != r.recibir:
    #            r.package_id = r.recibir

class MrpBom(models.Model):
    _inherit = "mrp.bom"

    mrp_bom_line_extra_ids = fields.One2many("mrp.bom.line", "bom_id")

class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    product_extra_id = fields.Many2one("product.product", string="Componentes extras")
    #check = fields.Boolean(related='product_extra_id.check_bool')

    #@api.depends('product_extra_id')
    #def _enviar_bool(self):
     #  for r in self:
      #     if r.product_extra_id:
       #        r.product_extra_id.check_bool = True ('name', '=', compo_rel)

class MrpWorkorderAdditionalProduct(models.TransientModel):
    _inherit = "mrp_workorder.additional.product"


    test_type = fields.Char(related='test_type_id.technical_name')
    test_type_id = fields.Many2one('quality.point.test_type', 'Test Type', related='workorder_id.test_type_id')
    compo_rel = fields.Many2one(related='workorder_id.production_id.bom_id.mrp_bom_line_extra_ids.product_id', readonly=False, default=lambda self: self.env.context.get('active_id', None))
    #otro = fields.Integer(compute="_buscar")
    product_rel = fields.Many2one(
    'product.product',
    'Product',
    required=True,
    domain="[('company_id', 'in', (company_id, False)), ('type', '!=', 'service')]")


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    active = fields.Boolean(
        string='Activo', 
        default=True
    )
   
    