from odoo import api, models, fields
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


# class HrEmployee(models.Model):
#     _inherit = 'sale.order'
#
#     @api.model
#     def mail_notification_invoice(self):
#         template = self.env.ref('codilar.invoice_mail_template')
#         print("hiijjjjjjjjjjjjj")
#         today_date = fields.Date.context_today(self)
#         sale_order = self.search([('end_date1', '!=', False)])
#         accountant = self.env['hr.employee'].search([('department_id', '!=', False)])
#         for account in accountant:
#             if account.department_id == "Administration":
#                 print(account, "hiii")
#             for sale in sale_order:
#                 if sale.end_date1 == today_date:
#                     template.send_mail(account.work_email, force_send=True)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def mail_notification_invoice(self):
        print("hii")
        template = self.env.ref('codilar.invoice_mail_template')
        today_date = fields.Date.context_today(self)
        print(today_date, "kkkkk")
        sale_orders = self.search([('end_date1', '!=', False)])
        accountant = self.env['hr.employee'].search(
            [('department_id.name', '=', 'Administration')])
        print(accountant.work_email, "kkkkk")
        for sale in sale_orders:
            if sale.end_date1 and sale.end_date1 == today_date:
                for account in accountant:
                    print(account.work_email, "pppppp")
                    template.send_mail(account.id, force_send=True)
