#  -*- coding: utf-8 -*-

from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'rnet.wizard'
    _description = "Wizar: Registros de Usuarios a Sesiones"

    def _default_sesiones(self):
        return self.env['rnet.sesion'].browse(self._context.get('active_ids'))


    sesion_ids=fields.Many2many('rnet.sesion',
        string="Sesion", required=True,
        default=_default_sesiones)
    asistente_ids = fields.Many2many('res.partner', string="Asistentes")

    @api.multi
    def suscribir(self):
        for sesion in self.sesion_ids:
            sesion.asistente_ids |= self.asistente_ids
        return {}
