# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
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
from datetime import datetime, timedelta
import json
from collections import defaultdict

from odoo import http
from odoo.http import request

# from datetime import datetime
import math


class ProjectFilter(http.Controller):
    """
    The ProjectFilter class provides the filter option to the js.
    When applying the filter return the corresponding data.
        Methods:
            project_filter(self):
                when the page is loaded adding filter options to the selection
                field.
                return a list variable.
            project_filter_apply(self,**kw):
                after applying the filter receiving the values and return the
                filtered data.

    """

    @http.route('/project/filter', auth='public', type='json')
    def project_filter(self):

        """

        Summery:
            transferring data to the selection field that works as a filter
        Returns:
            type:list of lists , it contains the data for the corresponding
            filter.


        """
        current_year = datetime.now().year
        start_year = current_year - 10
        end_year = current_year + 5
        years = list(range(start_year, end_year + 1))
        financial_years = [f"{year}-{year + 1}" for year in years]
        # response_data = {'years': years}
        response_data = {
            'financial_years': financial_years,
        }

        # Log the response before returning
        print(json.dumps(response_data))

        return json.dumps(response_data)

    @http.route('/project/filter-apply/year-wise', auth='public', type='json')
    def project_filter_apply_year_wise(self, **kw):
        data = kw['data']

        # Extract start_date and end_date from the input data
        start_date = data['start_date']
        end_date = data['end_date']

        # Convert start_date and end_date strings to datetime objects
        # start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        # end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        # Initialize a dictionary to store month-wise totals
        # month_totals = defaultdict(float)
        month_totals = defaultdict(lambda: {'subtotal': 0.0, 'total': 0.0})

        # Query sale.order.line records based on start_date and end_date
        sale_order_lines = request.env['sale.order.line'].search(
            [('end_date', '>=', start_date), ('end_date', '<=', end_date)])

        # Iterate through the sale order lines and calculate month-wise totals
        for line in sale_order_lines:
            month = line.end_date.strftime('%B')  # Get the month name
            subtotal = line.forcast  # add forcast amount
            total = line.achieved
            month_totals[month]['subtotal'] += subtotal
            month_totals[month]['total'] += total

        # Convert the defaultdict to a regular dictionary
        month_totals_dict = dict(month_totals)

        return {
            'month_wise_totals': month_totals_dict,
        }

    @http.route('/sale/order/year', auth='public', type='json')
    def sale_order_year(self):
        current_year = datetime.now().year
        next_year = current_year + 1

        # Initialize a dictionary to store month-wise data
        monthly_data = defaultdict(lambda: {'subtotal': 0.0, 'total': 0.0, })

        # Query sale.order.line records for the current year
        sale_order_lines = request.env['sale.order.line'].search([
            ('end_date', '>=', f'{current_year}-04-01'),
            ('end_date', '<=', f'{next_year}-03-31')
        ])

        # Iterate through the sale order lines and calculate month-wise totals
        for line in sale_order_lines:
            month = line.end_date.strftime('%B').lower()  # Get the month name in lowercase
            subtotal = line.forcast
            total = line.achieved

            # Ensure that the values in the dictionary are numerical before adding
            monthly_data[f'{month}']['subtotal'] += subtotal
            monthly_data[f'{month}']['total'] += total

        # for month, data in monthly_data.items():
        #     print("Month:", month)
        #     print("Total:", data['total'])
        #     print("sub total", data['subtotal'])
        #     try:
        #         percentage_month_wise = (data['subtotal'] / data['total']) * 100
        #         print("percentage_month_wise", percentage_month_wise)
        #     except ZeroDivisionError:
        #         percentage_month_wise = 0
        #         print("percentage_year_wise", percentage_month_wise)

        # Convert the defaultdict to a regular dictionary
        monthly_data_dict = dict(monthly_data)

        return {
            'month_wise_totals': monthly_data_dict,

        }

    @http.route('/month/filter', auth='public', type='json')
    def month_filter(self):
        current_year = datetime.now().year

        # Generate a list of 12 months for the current year
        z = {}
        months = [datetime(current_year, month, 1).strftime('%B') for month in range(4, 13)]
        month = [datetime(current_year, month, 1).strftime('%B') for month in range(1, 4)]

        for index, month_name in enumerate(months, start=4):
            z[index] = month_name
        for index, months_name in enumerate(month, start=1):
            z[index] = months_name
        # response_data = {'months': months,
        #
        #                  }
        response_data = {
            'z': z
        }

        # Log the response before returning
        print(json.dumps(response_data))
        print("Total month", z)

        return json.dumps(response_data)

    @http.route('/filter-apply/month-wise', auth='public', type='json')
    def filter_apply_month_wise(self, **kw):
        data = kw['data']
        print(f"Debug: Data received: {data}")

        # Extract start_date and end_date from the input data
        start_date = data['start_date']
        end_date = data['end_date']
        print(start_date)
        print(end_date)
        # Initialize variables to store the sum of price_subtotal and price_total
        subtotal_sum = 0.0
        total_sum = 0.0
        year, month, day = map(int, start_date.split("/"))
        new_start_date = datetime(year, 1, 1)
        new_end_date = datetime(year, month, day)
        formatted_start_date = new_start_date.strftime("%Y/%m/%d")
        formatted_end_date = new_end_date.strftime("%Y/%m/%d")

        # sale_order_pending_milestone = request.env['sale.order.line'].search(
        #     [('end_date', '>', formatted_start_date), ('end_date', '<=', formatted_end_date)])
        # p_achieved = 0.00
        # print("sale_order_pending_milestone::::", sale_order_pending_milestone)
        #
        # for pending in sale_order_pending_milestone:
        #     if pending.percentage == 100.00 and pending.invoice_status == "to invoice":
        #         p_achieved = p_achieved + pending.forcast
        #     if pending.invoice_status == "invoiced":
        #         print("Hii", pending.name)

        pending_milestone = request.env['sale.order.line'].search(
            [('end_date', '>', formatted_start_date), ('end_date', '<=', formatted_end_date)])
        pending_data = 0.0
        pending_data_dict = {}
        for pending in pending_milestone:
            if pending.pending_boolean_field:
                sale_order = pending.order_id  # Get the associated sale order
                sale_order_name = sale_order.name
                pending_data_dict[sale_order_name] = pending.forcast
                pending_data += pending.forcast
        print('pending data:', pending_data_dict)

        # invoice filtering previous month
        previous_invoice_dict = {}
        previous_invoice = request.env['account.move'].search(
            [('invoice_date', '>', formatted_start_date), ('invoice_date', '<=', formatted_end_date)])
        for invoice in previous_invoice:
            previous_invoice_dict[invoice.invoice_origin] = invoice.invoice_date.month

        print(previous_invoice_dict, 'previous')
        year, month, day = map(int, end_date.split("/"))
        # end_date_datetime = datetime.date(year, month, day)
        end_date_datetime = datetime(year, month, day)

        for key in previous_invoice_dict:
            if end_date_datetime.month > previous_invoice_dict[key]:
                if key in pending_data_dict:
                    pending_data = pending_data - pending_data_dict[key]

        # invoice filtering
        invoice_current_month = request.env['account.move'].search(
            [('invoice_date', '>', start_date), ('invoice_date', '<=', end_date)])
        current_invoice_data_dict = {}
        for inovice in invoice_current_month:
            current_invoice_data_dict[inovice.invoice_origin] = inovice.name
        print(current_invoice_data_dict)

        common_keys = set(pending_data_dict.keys()) & set(current_invoice_data_dict.keys())
        value = 0.0
        for key in common_keys:
            value += pending_data_dict[key]

        # calculating additional invoice amount
        additional_invoice_date = request.env['account.move'].search(
            [('invoice_date', '>', start_date), ('invoice_date', '<=', end_date), ('invoice_origin', '=', False),
             ('move_type', '=', 'out_invoice')])
        additional_invoice_amount = 0.0  # storing total value of additional invoice
        for invoice in additional_invoice_date:
            additional_invoice_amount = additional_invoice_amount + invoice.amount_untaxed

        # Query sale.order.line records based on start_date and end_date
        sale_order_lines = request.env['sale.order.line'].search(
            [('end_date', '>', start_date), ('end_date', '<=', end_date)])
        # Iterate through the sale order lines and calculate the sums
        sum_fixed = 0.0
        fixed_achived = 0.0
        sum_tm = 0.0
        tm_achieved = 0.0
        pending = 0.0
        for line in sale_order_lines:
            # if line.pending:
            #     pending = pending + line.price_unit

            if line.project_type == "ordered_timesheet":
                sum_fixed += line.forcast
                fixed_achived += line.achieved

            if line.project_type == "delivered_timesheet":
                sum_tm += line.forcast
                tm_achieved += line.achieved

        total_forcast = sum_fixed + sum_tm
        total_achieved = fixed_achived + tm_achieved
        if sum_tm != 0:
            tm_percentage1 = (tm_achieved / sum_tm) * 100
        else:
            tm_percentage1 = 0

        tm_percentage = tm_percentage1
        try:
            fixed_percentage = round((fixed_achived / sum_fixed) * 100, 2)
        except ZeroDivisionError:
            fixed_percentage = 0

        try:
            total_percentage = round((total_achieved / total_forcast) * 100, 2)
        except ZeroDivisionError:
            total_percentage = 0
        additional_invoice_amount_new = additional_invoice_amount
        total_estimation_this_month_forcast = total_forcast + additional_invoice_amount + pending_data
        total_estimation_this_month_achieved = total_achieved + value + additional_invoice_amount_new
        try:
            total_estimation_this_month_percentage = round((
                                                                   total_estimation_this_month_achieved / total_estimation_this_month_forcast) * 100,
                                                           2)
        except ZeroDivisionError:
            total_estimation_this_month_percentage = 0

        revenue_forcast_this_month = total_estimation_this_month_achieved
        total_not_achieved = total_estimation_this_month_forcast - total_estimation_this_month_achieved

        target_vs_achieved_percentage = total_estimation_this_month_percentage
        try:
            additional_invoice_percentage = round(
                ((additional_invoice_amount_new / additional_invoice_amount_new) * 100))
        except ZeroDivisionError:
            additional_invoice_percentage = 0

        actual_revenue = total_estimation_this_month_forcast - pending_data  # need to check
        actual_achieved = total_estimation_this_month_achieved - value
        try:
            actual_percentage = round((actual_achieved / actual_revenue) * 100, 2)
        except ZeroDivisionError:
            actual_percentage = 0
        try:
            percentage_pending_milestone = round((value / pending_data) * 100, 2)
        except ZeroDivisionError:
            percentage_pending_milestone = 0

        return {
            'fixed_forcast': sum_fixed,
            'timesheet_forcast': sum_tm,
            'fixed_achieved': fixed_achived,
            'timesheet_achieved': tm_achieved,
            'percentage_fixed': fixed_percentage,
            'percentage_timesheet': tm_percentage,
            'total_forcast': total_forcast,
            'total_achieved': total_achieved,
            'total_percentage': total_percentage,
            'pending_projection': pending_data,
            'additional_invoice': additional_invoice_amount,
            'additional_invoice_amount': additional_invoice_amount,
            'pending_achieved': value,
            'total_estimation_this_month_forcast': total_estimation_this_month_forcast,
            'total_estimation_this_month_achieved': total_estimation_this_month_achieved,
            'total_estimation_this_month_percentage': total_estimation_this_month_percentage,
            'revenue_forcast_this_month': revenue_forcast_this_month,
            'total_not_achieved': total_not_achieved,
            'target_vs_achieved_percentage': target_vs_achieved_percentage,
            'additional_invoice_percentage': additional_invoice_percentage,
            'actual_revenue': actual_revenue,
            'actual_achieved': actual_achieved,
            'actual_percentage': actual_percentage,
            'percentage_pending_milestone': percentage_pending_milestone,

        }
