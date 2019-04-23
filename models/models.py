# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import timedelta

class Curso(models.Model):
    _name = 'rnet.curso'

    name = fields.Char(string="Nombre del curso", required=True, size =50)
    descripcion=fields.Text(string="Descripción")
    responsable_id = fields.Many2one('res.users', ondelete='set null', string="Responsable", index=True)
    sesion_ids = fields.One2many('rnet.sesion','curso_id', string="Sesiones")

    _sql_constraints = [
        ('verificar_nombre_descripcion',
        'CHECK(name !=descripcion)',
        "El nombre de un curso no debe ser su descripción"),

        ('nombre_unico',
        'UNIQUE(name)',
        "El nombre del curso debe ser único"),
    ]

class Sesion(models.Model):
    _name = 'rnet.sesion'

    name=fields.Char(string="Nombre", required=True, default = '/')
    inicio = fields.Datetime(default=lambda self:fields.Datetime.now())
    duracion = fields.Float(string="Duración", digits=(6,2), help = "Duración en dias")
    asientos = fields.Integer(String="Asientos")
    instructor_id = fields.Many2one('res.partner', string="Instructor",
    domain=[('instructor', '=', True)])
    curso_id = fields.Many2one('rnet.curso', ondelete='cascade', string="Curso", required=True)
    asistente_ids = fields.Many2many('res.partner', 'partner_sesion_rel', 'sesion_id', 'partner_id', string="Asistentes")
    asientosReservados = fields.Float(string="Asientos Reservados", compute='_asientosReservados')
    fin = fields.Datetime(string="Fin", store=True, compute='_getFin', inverse= '_setFin' )
    state = fields.Selection([
        ('borrador', "Borrador"),
        ('confirmada', "Confirmada"),
        ('realizada', "Realizada"),
        ('cancelada', "Cancelada"),
    ], string = "Estado", copy = False, default='borrador')

#funciones para los estados
    @api.multi
    def action_borrador(self):
        for i in self:
            i.state = 'borrador'

    @api.multi
    def action_confirmar(self):
        for i in self:
            i.state = 'confirmada'

    @api.multi
    def action_realizar(self):
        for i in self:
            i.state = 'realizada'

    @api.multi
    def action_cancelar(self):
        for i in self:
            i.state = 'cancelada'


#Defunimos una funcion
    @api.depends('asientos', 'asistente_ids')
    def _asientosReservados(self):
        for record in self:
            if not record.asientos:
                record.asientosReservados  = 0.0
            else:
                record.asientosReservados = 100 * len(record.asistente_ids) / record.asientos

    @api.onchange('asientos', 'asistente_ids')
    def _verify_valid_seats(self):
        self.ensure_one()
        if self.asientos<0:
            self.asientos= 0
            return{
                'warning':{
                    'title': "Número de Asientos incorrecto",
                    'message': "El número de asientos no debe ser negativo",
                },
            }
        if self.asientos < len(self.asistente_ids):
            return{
                'warning':{
                    'title': "Hay demasiados asientos reservados",
                    'message': "El número de asientos reservados es mayor que los"\
                    " asientos disponibles. Incremente el número de asiontos o"\
                    " reasigne a los reservantes",
                },
            }
    @api.depends('inicio', 'duracion')
    def _getFin(self):
        for record in self:
            if not (record.inicio and record.duracion):
                record.fin = record.inicio
                continue
            inicio = fields.Datetime.from_string(record.inicio)
            duracion = timedelta(days=(record.duracion - 1))
            record.fin = inicio + duracion
    def _setFin(self):
        for record in self:
            if not (record.inicio and record.fin):
                continue
            inicio = fields.Datetime.from_string(record.inicio)
            fin = fields.Datetime.from_string(record.fin)
            record.duracion = (fin - inicio).days + 1

    @api.constrains('instructor_id', 'asistente_ids')
    def _check_instructor_not_in_attendees(self):
        for record in self:
            if record.instructor_id and record.instructor_id in record.asistente_ids:
                raise exceptions.ValidationError("El instructor de la sesión no puede estar entre"\
                " los reservantes")
