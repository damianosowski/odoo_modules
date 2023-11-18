# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from itertools import cycle


class StockCmr(models.AbstractModel):
    _name = 'report.pwc_tasks.task_pivot_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, tasks):

        row = 0
        column = 0

        # template start
        report = workbook.add_worksheet()

        # formats
        bold_format = workbook.add_format({'bold': True})

        task_format_1 = workbook.add_format()
        task_format_1.set_text_wrap()
        task_format_1.set_bg_color('yellow')
        task_format_2 = workbook.add_format()
        task_format_2.set_text_wrap()
        task_format_2.set_bg_color('blue')
        task_format_3 = workbook.add_format()
        task_format_3.set_text_wrap()
        task_format_3.set_bg_color('green')
        task_format_4 = workbook.add_format()
        task_format_4.set_text_wrap()
        task_format_4.set_bg_color('magenta')

        task_formats = cycle([task_format_1, task_format_2, task_format_3, task_format_4])

        project_format = workbook.add_format()
        project_format.set_bg_color('gray')

        # report data
        task_names = sorted(list(set(tasks.mapped('name'))))
        project_ids = tasks.mapped('project_id').sorted(key=lambda r: r.id)

        report.set_column(column, column + 2 * len(task_names), 10)
        report.set_row(row + 1, 30)
        report.write(row, column, None, project_format)
        report.write(row + 1, column, None, project_format)

        task_name_column = column + 1
        name_columns_dict = {}
        for task_name in task_names:
            cell_format = next(task_formats)
            report.write(row, task_name_column, task_name, cell_format)
            report.write(row, task_name_column + 1, None, cell_format)
            report.write(row + 1, task_name_column, 'Deadline', cell_format)
            report.write(row + 1, task_name_column + 1, 'Last stage update', cell_format)
            name_columns_dict[task_name] = task_name_column
            task_name_column += 2

        project_row = row + 2
        for project in project_ids:
            report.write(project_row, column, project.name, project_format)
            for task in project.tasks:
                task_column = name_columns_dict.get(task.name)
                if task_column:
                    report.write(project_row, task_column,
                                 task.date_deadline.strftime('%d.%m.%Y') if task.date_deadline else None,
                                 bold_format)
                    report.write(project_row, task_column + 1,
                                 task.date_last_stage_update.strftime('%d.%m.%Y') if task.date_last_stage_update else None,
                                 bold_format)
            project_row += 1
