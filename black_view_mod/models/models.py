# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.workorder'
    #_description = 'test_module.test_module'

    package_id = fields.Many2one(related='move_id.move_line_ids.package_id', readonly=False)
    location_id = fields.Many2one(related='move_id.move_line_ids.location_id', readonly=False)

class MrpBom(models.Model):
    _inherit = "mrp.bom"

    mrp_bom_line_extra_ids = fields.One2many("mrp.bom.line", "bom_id")

class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    product_extra_id = fields.Many2one("product.product", string="Componentes extras")
    check = fields.Boolean(related='product_extra_id.check_bool')

    #@api.depends('product_extra_id')
    #def _enviar_bool(self):
     #  for r in self:
      #     if r.product_extra_id:
       #        r.product_extra_id.check_bool = True

class ProductProduct(models.Model):
    _inherit = "product.product"

    check_bool = fields.Boolean(default=False, readonly=False, required=False)