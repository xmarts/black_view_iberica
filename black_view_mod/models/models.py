# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.workorder'
    #_description = 'test_module.test_module'

    package_id = fields.Many2one(related='move_id.move_line_ids.package_id', readonly=False)
    location_id = fields.Many2one(related='move_id.move_line_ids.location_id', readonly=False)
    #value = fields.Integer()
    #value2 = fields.Float(compute="_value_pc", store=True)
    #description = fields.Text()

    #@api.depends('value')
    #def _value_pc(self):
    # for record in self:
    #     record.value2 = float(record.value) / 100
