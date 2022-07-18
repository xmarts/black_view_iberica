# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from logging import logThreads
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PaqueteFuente(models.Model):
    _name = 'paquete.fuente.order'
    _description = 'Paquete fuente'

    name = fields.Integer()
    paquete_fuente = fields.Integer()
    producto = fields.Many2one('product.product')
    quantity = fields.Integer()
    lot= fields.Integer()
    company = fields.Many2one('res.company')