# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.workorder'
    #_description = 'test_module.test_module'

    paquete_fuente = fields.Many2one('stock.production.lot')
    #value = fields.Integer()
    #value2 = fields.Float(compute="_value_pc", store=True)
    #description = fields.Text()

    #@api.depends('value')
    #def _value_pc(self):
    # for record in self:
    #     record.value2 = float(record.value) / 100
