# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class WizardTaskCalendar(models.TransientModel):
    _name = 'project.task.calendar'

    project_ids = fields.Many2many('project.project', string='Projects', help='If empty, all projects will be included')
    date_from = fields.Date(
        string='Start Date',
        default=lambda self: fields.Date.context_today(self).replace(month=1, day=1),
        required=True)
    date_to = fields.Date(
        string='End Date',
        default=lambda self: fields.Date.context_today(self).replace(month=12, day=31),
        required=True)

    def generate_report(self):
        if self.date_from.year != self.date_to.year:
            raise UserError(_('The start and end dates should be in the same year.'))
        data = {}
        if not self.project_ids:
            self.project_ids = self.env['project.project'].search([])
        data['date_from'] = self.date_from
        data['date_to'] = self.date_to
        data['project_ids'] = self.project_ids.ids
        report_reference = self.env.ref('pwc_tasks.action_report_task_calendar_xlsx').report_action(self, data=data)
        report_reference.update({'close_on_report_download': True})
        return report_reference
