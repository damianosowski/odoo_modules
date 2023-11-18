# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from datetime import date, datetime
import calendar

YEAR_LENGTH = 366


class ReportTaskCalendar(models.AbstractModel):
    _name = 'report.pwc_tasks.task_calendar'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, tasks):

        row = 0
        column = 0

        # template start
        report = workbook.add_worksheet()

        # formats
        bold_format = workbook.add_format({'bold': True})
        months_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
        })
        deadline_format = workbook.add_format()
        deadline_format.set_bg_color('red')

        weekend_format = workbook.add_format()
        weekend_format.set_bg_color('gray')

        # report data
        project_ids = self.env['project.project'].browse(data['project_ids'])
        tasks = project_ids.mapped('tasks')
        date_from = datetime.strptime(data['date_from'], '%Y-%m-%d')
        date_to = datetime.strptime(data['date_to'], '%Y-%m-%d')
        year = date_from.year

        # report start
        report.merge_range(row, row, column, column + YEAR_LENGTH,
                           'Task calendar: from {} to {} '.format(data['date_from'], data['date_to']), bold_format)

        # months and days
        days_columns = {}  # dict for task deadline
        day_column = column + 1
        for month_number in range(date_from.month, date_to.month+1):
            month_first_column = day_column
            days_columns[month_number] = []  # dict for task deadline, empty list pof each month
            for day_number in calendar.Calendar().itermonthdays(year, month_number):
                if (day_number == 0 or
                        month_number == date_from.month and day_number < date_from.day or
                        month_number == date_to.month and day_number > date_to.day):
                    continue
                report.write(row + 2, day_column, day_number)
                days_columns[month_number].append({day_number: day_column})  # dict for task deadline, pair {day: column} added

                if date(year, month_number, day_number).weekday() in [5, 6]:
                    report.set_column(day_column, day_column, cell_format=weekend_format)
                    for row_task in range(row + 3, row + 3 + len(tasks)):
                        report.write(row_task, day_column, None, weekend_format)

                day_column += 1
            report.merge_range(row + 1, month_first_column, row + 1, day_column - 1, calendar.month_name[month_number],
                               months_format)

        # tasks
        task_row = row + 3
        for task in tasks:
            report.write(task_row, column, task.name)
            deadline = task.date_deadline
            if deadline and deadline.year == year:
                deadline_days_columns = days_columns.get(deadline.month)  # --> list of dicts {day: column} for deadline month
                if deadline_days_columns:
                    deadline_column = [column.get(deadline.day) for column in deadline_days_columns
                                       if deadline.day in column]
                    if deadline_column:
                        report.write(task_row, deadline_column[0], '!', deadline_format)
            task_row += 1

        # column width
        report.set_column(column, column, 20)
        report.set_column(column + 1, column + YEAR_LENGTH, 2)
