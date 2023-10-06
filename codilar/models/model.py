from odoo import api, models, fields
import datetime
from odoo.exceptions import AccessError
from datetime import date
from odoo.exceptions import ValidationError


class StartDateTask(models.Model):
    _inherit = 'project.task'

    start_date = fields.Date(string="Start Date")
    allocated_hr = fields.Float(string="Allocated Hours")
    total_allocate_hr = fields.Float(string="Remain allocated hours", readonly=True,
                                     compute='_compute_allocated_hr')
    task_progress = fields.Float(string="Achieved amount")
    forcast = fields.Float(string="Forcast amount", readonly=True)
    resource_count = fields.Integer(string="Resource count")

    @api.onchange('resource_count')
    def _onchange_resource_count(self):
        for rec in self:
            if rec.resource_count and rec.sale_line_id:
                rec.sale_line_id.resource_count = rec.resource_count

    @api.onchange('task_progress')
    def _onchange_task_progress(self):
        for rec in self:
            # if rec.task_progress >= rec.sale_line_id.forcast:
            #     raise ValidationError("Task achieved amount should not exceed forcast")
            if rec.task_progress and rec.sale_line_id:
                rec.sale_line_id.achieved = rec.task_progress
                rec.sale_line_id.not_achieved = rec.sale_line_id.forcast - rec.sale_line_id.achieved
                rec.sale_line_id.percentage = (rec.sale_line_id.achieved / rec.sale_line_id.forcast) * 100

    @api.depends('allocated_hr')
    def _compute_allocated_hr(self):
        for record in self:
            if record.name:
                if record.allocated_hr > 0:
                    record.total_allocate_hr = record.allocated_hr - record.effective_hours
                else:
                    record.total_allocate_hr = 0

    @api.onchange('allocated_hr')
    def _onchange_allocated_hr(self):
        if self.env.user.has_group('codilar.group_user_admin'):
            pass
        else:
            raise AccessError("You are not allowed to edit the 'Allocated Hours' field.")


class SalesOrderDate(models.Model):
    _inherit = "sale.order.line"

    project_type = fields.Char(string="Project type")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    invoice_date = fields.Date(string="Invoice Date")
    payment_terms = fields.Many2one('account.payment.term', String="Payment Terms")
    forcast = fields.Float(string="Forcast amount")
    achieved = fields.Float(string='Achieved %', readonly=True)
    not_achieved = fields.Float(string="Not achieved %", readonly=True)
    percentage = fields.Float(string='Percentage', store=True)
    pending = fields.Boolean(string="Pending Milestone")
    milestone_type = fields.Char(string="Milestone type")
    resource_count = fields.Float(string="Resource count")
    pending_boolean_field = fields.Boolean(string="Pending", default=False)


class SaleOrderTreeView(models.Model):
    _inherit = "sale.order"

    start_date1 = fields.Date(string="Start Date", compute="_compute_start_date1", store=True)
    end_date1 = fields.Date(string="End Date", compute="_compute_end_date1", store=True)
    note = fields.Char(String="Note")
    project_id = fields.Many2one('project.project', string="Project")
    project = fields.Char(string="Project", readonly=True, compute='_compute_project', store=True)
    not_achieved = fields.Float(string="Not achieved", compute="_compute_not_achieved")
    forcast = fields.Float(string="Forcast amount", compute="_compute_forcast")
    achieved = fields.Float(string="Achieved amount", compute="_compute_achieved")
    percentage = fields.Float(string="Percentage", compute="_compute_percentage")
    milestone = fields.Char(string="Milestone status", compute="_compute_milestone")
    project_type = fields.Char(string='Project Type')
    milestone_type = fields.Char(string="Milestone type")
    pending_boolean_field = fields.Boolean(string="Pending", readonly=True)
    user = fields.Many2one('res.users', String="Project manager")

    @api.onchange('payment_term_id')
    def _onchange_payment_term_id(self):
        for rec in self:
            if rec.payment_term_id:
                rec.order_line.payment_terms = rec.payment_term_id

    @api.onchange('order_line.pending_boolean_field')
    def _onchange_pending_boolean_field(self):
        for rec in self:
            if rec.order_line.pending_boolean_field == True:
                rec.pending_boolean_field = 'Pending'
                print("bool", rec.pending_boolean_field)

    @api.onchange('order_line.product_id')
    def _compute_project_type(self):
        for rec in self:
            if rec.order_line.product_id.service_policy:
                rec.order_line.project_type = rec.order_line.product_id.service_policy
                rec.project_type = rec.order_line.product_id.service_policy

    def _compute_percentage(self):
        for record in self:
            percentage_total = sum(order_line.percentage for order_line in record.order_line)
            record.percentage = percentage_total

    def _compute_achieved(self):
        for record in self:
            achieved_total = sum(order_line.achieved for order_line in record.order_line)
            record.achieved = achieved_total

    def _compute_not_achieved(self):
        for record in self:
            not_achieved_total = sum(order_line.not_achieved for order_line in record.order_line)
            record.not_achieved = not_achieved_total

    def _compute_forcast(self):
        for record in self:
            forcast_total = sum(order_line.forcast for order_line in record.order_line)
            record.forcast = forcast_total

    @api.depends('project_id')
    def _compute_project(self):
        for order in self:
            if order.project_id:
                order.project = order.project_id.name
            else:
                order.project = False

    # @api.depends('milestone')
    # def _compute_milestone(self):
    #     for order in self:
    #         if order.order_line.name:
    #             order.milestone = order.order_line.name
    #         else:
    #             order.milestone = False

    @api.depends('milestone')
    def _compute_milestone(self):
        for order in self:
            if order.order_line:
                milestone_names = order.order_line.mapped('name')
                if milestone_names:
                    order.milestone = ', '.join(milestone_names)
                else:
                    order.milestone = False
            else:
                order.milestone = False

    @api.depends('order_line.start_date')
    def _compute_start_date1(self):
        for order in self:
            start_dates = order.order_line.mapped('start_date')
            if start_dates and all(date for date in start_dates):
                order.start_date1 = min(start_dates)
            # else:
            #     order.start_date1 = False

    @api.depends('order_line.end_date')
    def _compute_end_date1(self):
        for order in self:
            end_dates = order.order_line.mapped('end_date')
            if end_dates and all(date for date in end_dates):
                order.end_date1 = max(end_dates)
            # else:
            #     order.end_date1 = False

    # def action_test(self):
    #
    #     for rec in self:
    #         if rec.order_line.product_id.service_policy:
    #             rec.order_line.project_type = rec.order_line.product_id.service_policy
    #             rec.project_type = rec.order_line.product_id.service_policy
    #
    #     for order_line in rec.order_line:
    #         if order_line.project_type == "ordered_timesheet":
    #             rec.order_line.milestone_type = 'Fixed cost'
    #         elif order_line.project_type == "delivered_timesheet":
    #             rec.order_line.milestone_type = 'Timesheet cost'
    #     if rec.order_line.milestone_type:
    #         rec.milestone_type = rec.order_line.milestone_type
    #         print("sale :", rec.milestone_type)
    #     rec.order_line.milestone_type = rec.order_line.milestone_type.rstrip(', ')
    #     print(rec.order_line.milestone_type)
    #     a = 0.0
    #     if rec.invoice_ids:
    #         a = rec.amount_untaxed - rec.invoice_ids.amount_untaxed
    #
    #         print("hii", rec.invoice_ids.amount_untaxed)
    #     print("dddddddddddd", a)
    #     project = self.env['project.task'].search([])
    #     for rec in self:
    #         if rec.order_line.forcast:
    #             for record in project:
    #                 if record.forcast:
    #                     record.forcast = rec.order_line.forcast
    #                     print("forcast :", record.forcast)

    def confirm_forcast(self):
        a = self.env['project.task'].search([])
        for i in a:
            if i.sale_line_id.forcast:
                i.forcast = i.sale_line_id.forcast

    def confirm_milestone(self):
        for i in self:
            if i.order_line.pending_boolean_field == True:
                i.pending_boolean_field = i.order_line.pending_boolean_field
            else:
                i.pending_boolean_field = False

    def _prepare_invoice(self):
        item = super(SaleOrderTreeView, self)._prepare_invoice()

        return item

    def action_confirm(self):
        super(SaleOrderTreeView, self).action_confirm()

        template = self.env.ref('codilar.sale_mail_confirm_template')
        for rec in self:
            email = {
                'to': rec.user.login
            }
            template.send_mail(rec.id, email)

        for rec in self:
            z = []
            if not rec.invoice_ids:
                z.append(rec.invoice_ids)
                print(rec.invoice_ids.name)
            print(z)
            for order_line in rec.order_line:
                if order_line.product_id.service_policy:
                    order_line.project_type = order_line.product_id.service_policy
                    rec.project_type = order_line.product_id.service_policy

                if order_line.project_type == "ordered_timesheet":
                    order_line.milestone_type = 'Fixed cost'
                elif order_line.project_type == "delivered_timesheet":
                    order_line.milestone_type = 'Timesheet cost'
                today = date.today()
                print("Today date is: ", today)

                # if rec.invoice_ids:
                #     a = rec.amount_untaxed - rec.invoice_ids.amount_untaxed
                #     print("hii", rec.invoice_ids.amount_untaxed)
                #     print("dddddddddddd", a)
                # # a = []
                # if rec.invoice_ids:
                #     a.append(rec.invoice_ids.invoice_date)
                #     # Get the current date and time
                #     today = date.today()
                #     print("Today date is: ", today)
                #     if rec.invoice_ids.invoice_date == datetime.date:
                #         print("invoice date :", rec.invoice_ids.invoice_date)
                #         print("current date :", datetime.date)
                #     else:
                #         print("no invoice")
                #
                #         print("invoice date :", rec.invoice_ids.invoice_date)
                #

                # if rec.order_line.milestone_type:
                #     rec.milestone_type = rec.order_line.milestone_type.rstrip(', ')
                #     print(rec.order_line.milestone_type)
                #
                # if rec.order_line.milestone_type:
                #     print("sale :", rec.order_line.milestone_type)

                milestone_type_list = []
                for order_line in rec.order_line:
                    if order_line.milestone_type:
                        milestone_type_list.append(order_line.milestone_type.rstrip(', '))
                rec.milestone_type = ', '.join(milestone_type_list)


class SendMailToAccountant(models.Model):
    _inherit = 'account.move'

    user = fields.Many2one('res.users', string="Accountant")

    def action_post(self):
        super(SendMailToAccountant, self).action_post()

        template = self.env.ref('codilar.invoice_mail_confirm_template')
        for rec in self:
            email = {
                'to': rec.user.login
            }
            template.send_mail(rec.id, email)
        # return item
