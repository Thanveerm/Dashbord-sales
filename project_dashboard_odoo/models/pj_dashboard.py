# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

import calendar
import random
from datetime import datetime

from collections import defaultdict
from dateutil.relativedelta import relativedelta

from odoo import models, api


class PosDashboard(models.Model):
    """

    The ProjectDashboard class provides the data to the js when the dashboard is loaded.
        Methods:
            get_tiles_data(self):
                when the page is loaded get the data from different models and transfer to the js file.
                return a dictionary variable.
            get_top_timesheet_employees(model_ids):
               getting data for the timesheet graph.
            get_hours_data(self):
                getting data for the hours table.
            get_task_data(self):
                getting data to project task table
            get_project_task_count(self):
                getting data to project task table
            get_color_code(self):
                getting dynamic color code for the graph
            get_income_this_month(self):
                getting data to profitable graph after month filter apply
            get_income_last_year(self):
                getting data to profitable graph after last year filter apply
            get_income_this_year(self):
                getting data to profitable graph after current year filter apply
            get_details(self):
                getting data for the profatable table

    """
    _inherit = 'project.project'



    @api.model
    def get_task_data(self):
        """

        Summery:
            when the page is loaded get the data from different models and transfer to the js file.
            return a dictionary variable.
        return:
            type:It is a dictionary variable. This dictionary contain data that affecting project task table.

        """
        self._cr.execute('''select project_task.name as task_name,pro.name as project_name from project_task
          Inner join project_project as pro on project_task.project_id = pro.id ORDER BY project_name ASC''')
        data = self._cr.fetchall()
        project_name = []
        for rec in data:
            b = list(rec)
            project_name.append(b)
        return {
            'project': project_name
        }

