# -*- coding: utf-8 -*-

from multiprocessing import context
from odoo import models, fields, api
from odoo.tools import float_compare, float_round, float_is_zero

class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.workorder'
    #_description = 'test_module.test_module'

    package_id = fields.Many2one(related='move_id.move_line_ids.package_id',readonly=False)
    location_id = fields.Many2one(related='move_id.move_line_ids.location_id', readonly=False)

    @api.onchange('lot_id')
    def _update_component_quantity_lot(self):
        self.ensure_one()
        for wo in self:
            if wo.lot_id:
                wo.qty_done = wo.move_line_ids.qty_done
                if wo.qty_done <= 0.0000:
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

   
    