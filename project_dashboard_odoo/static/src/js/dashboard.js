odoo.define('pj_dashboard.Dashboard', function(require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');
    var _t = core._t;
    var session = require('web.session');
    var web_client = require('web.web_client');
    var abstractView = require('web.AbstractView');
    var flag = 0;
    var tot_so = []
    var tot_project = []
    var tot_task = []
    var tot_employee = []
    var tot_hrs = []
    var tot_margin = []
    var PjDashboard = AbstractAction.extend({
        template: 'PjDashboard',
        cssLibs: [
            '/project_dashboard_odoo/static/src/css/lib/nv.d3.css'
        ],
        jsLibs: [
            '/project_dashboard_odoo/static/src/js/lib/d3.min.js'
        ],

        events: {
            'change #income_expense_values': 'onchange_profitability',
             'click #filter_button': '_onchangeFilter',
            'change #employee_selection': '_onchangeFilter',
            'change #year_wise_selection': 'yearly_report',
               'click #project_selection': '_onProjectSelectionClick',
               'click #month_selection': '_onMonthSelectionClick',
               'click #year_wise_selection': '_onyearSelectionClick',
        },

        init: function(parent, context) {
            this._super(parent, context);
            this.dashboards_templates = ['DashboardProject', 'DashboardChart'];
            this.today_sale = [];
        },


        willStart: function() {
            var self = this;
            return $.when(ajax.loadLibs(this), this._super()).then(function() {
                return self.fetch_data();
            });
        },

        start: function() {
            var self = this;
            this.set("title", 'Dashboard');
            return this._super().then(function() {
                self.render_dashboards();
//                self.render_graphs();
                self.render_filter()
            });
        },

        render_dashboards: function() {
            var self = this;
            _.each(this.dashboards_templates, function(template) {
                self.$('.o_pj_dashboard').append(QWeb.render(template, {
                    widget: self
                }));
            });
        },

        render_filter: function() {

            ajax.rpc('/sale/order/year').then(function(response) {
            console.log(response)
            var currentYear = new Date().getFullYear();
             let serialNumber = 1;
             for (const key in response.month_wise_totals)
{
             var Html="<tr>
                <td >"+serialNumber+" </td>
                <td>"+key+"</td>
                <td>"+response.month_wise_totals[key]['subtotal']+"</td>
                <td>"+response.month_wise_totals[key]['total']+"</td>
            </tr>";
            $('#tbody').append(Html);
            serialNumber++;
    }
       });
                },


        on_reverse_breadcrumb: function() {
            var self = this;
            web_client.do_push_state({});
            this.fetch_data().then(function() {
                self.$('.o_pj_dashboard').empty();
                self.render_dashboards();

            });
        },
        _onchangeFilter: function() {
            flag = 1
            var selectedYear = $('#project_selection').val();
            var selectedMonth = $('#month_selection').val();
            var startDate = new Date(selectedYear, selectedMonth - 1, 1); // Set the day to 01
            var endDate = new Date(selectedYear, selectedMonth, 1);
            var start_date = startDate.toISOString().split('T')[0].replace(/-/g, '/');
            var end_date = endDate.toISOString().split('T')[0].replace(/-/g, '/');
            ajax.rpc('/filter-apply/month-wise', {
               'data': {
                    'start_date': start_date,
                    'end_date': end_date,

                }
            }).then(function(data) {
             console.log(data)

                document.getElementById('fixed_forcast').innerHTML = data['fixed_forcast'];
                document.getElementById('timesheet_forcast').innerHTML = data['timesheet_forcast'];
                document.getElementById('total_forcast').innerHTML = data['total_forcast'];
                document.getElementById('fixed_achieved').innerHTML = data['fixed_achieved'];
                document.getElementById('timesheet_achieved').innerHTML = data['timesheet_achieved'];
                document.getElementById('total_achieved').innerHTML = data['total_achieved'];
                document.getElementById('percentage_fixed').innerHTML = data['percentage_fixed'];
                document.getElementById('percentage_timesheet').innerHTML = data['percentage_timesheet'];
                document.getElementById('total_percentage').innerHTML = data['total_percentage'];
                document.getElementById('pending_projection').innerHTML = data['pending_projection'];
                document.getElementById('additional_invoice').innerHTML = data['additional_invoice'];
                document.getElementById('pending_achieved').innerHTML = data['pending_achieved'];
                document.getElementById('additional_invoice_amount').innerHTML = data['additional_invoice_amount'];
                document.getElementById('total_estimation_this_month_forcast').innerHTML = data['total_estimation_this_month_forcast'];
                document.getElementById('total_estimation_this_month_achieved').innerHTML = data['total_estimation_this_month_achieved'];
                document.getElementById('total_estimation_this_month_percentage').innerHTML = data['total_estimation_this_month_percentage'];
                document.getElementById('revenue_forcast_this_month').innerHTML = data['revenue_forcast_this_month'];
                document.getElementById('total_not_achieved').innerHTML = data['total_not_achieved'];
                document.getElementById('target_vs_achieved_percentage').innerHTML = data['target_vs_achieved_percentage'];
                document.getElementById('additional_invoice_percentage').innerHTML = data['additional_invoice_percentage'];
                document.getElementById('actual_revenue').innerHTML = data['actual_revenue'];
                document.getElementById('actual_achieved').innerHTML = data['actual_achieved'];
                document.getElementById('actual_percentage').innerHTML = data['actual_percentage'];
                document.getElementById('percentage_pending_milestone').innerHTML = data['percentage_pending_milestone'];
            });
        },

        yearly_report: function() {

            var selectedYear = $('#year_wise_selection').val();
            var startDate = new Date(selectedYear, 0, 1);
            var endDate = new Date(selectedYear, 11, 31);
            var start_date = startDate.toISOString().split('T')[0].replace(/-/g, '/');
            var end_date = endDate.toISOString().split('T')[0].replace(/-/g, '/');
            $('#tbody').empty();
            ajax.rpc('/project/filter-apply/year-wise', {
                'data': {
                    'start_date': start_date,
                    'end_date': end_date,

                }
            }).then(function(data) {
             console.log(data.month_wise_totals)
             let serialNumber = 1;
             for (const key in data.month_wise_totals)
        {

             var Html="<tr>
                <td >"+serialNumber+" </td>
                <td>"+key+"</td>
                <td>"+data.month_wise_totals[key]['subtotal']+"</td>
                <td>"+data.month_wise_totals[key]['total']+"</td>
            </tr>";
            $('#tbody').append(Html);
            serialNumber++;
        }

            })
        },

     _onProjectSelectionClick: function() {
      var $projectSelection = $('#project_selection');
        if ($projectSelection.data('loaded') !== true) {
        $projectSelection.data('loaded', true);
        ajax.rpc('/project/filter').then(function(response) {
            var data = JSON.parse(response);
            console.log(data.years)
                var years = data.years;
                $(years).each(function(index,year) {
                    $('#project_selection').append("<option value=" + year + " class='fs-5'>" + year + "</option>");
                });
                 });
                 }
        },
    _onyearSelectionClick: function() {
         var $projectSelection = $('#year_wise_selection');
    if ($projectSelection.data('loaded') !== true) {
        $projectSelection.data('loaded', true);
        ajax.rpc('/project/filter').then(function(response) {
            var data = JSON.parse(response);
            console.log(data.years)
                var years = data.years;
                $(years).each(function(index,year) {
                    $('#year_wise_selection').append("<option value=" + year + " class='fs-5'>" + year + "</option>");
                });
                 });
                 }
        },
        _onMonthSelectionClick: function() {
         var $monthSelection = $('#month_selection');
    if ($monthSelection.data('loaded') !== true) {
        // Set a flag to indicate that options have been loaded
        $monthSelection.data('loaded', true);
        ajax.rpc('/month/filter').then(function(response) {
            var data = JSON.parse(response);
            console.log(data.months)
                var years = data.months;
                $(years).each(function(index,year) {
                var monthNumber = index + 1;
                    $('#month_selection').append("<option value=" + monthNumber + " class='fs-5'>" + year + "</option>");
                });
                 });
                 }
        },

        fetch_data: function() {
            var self = this;
            var def4 = self._rpc({
                    model: "project.project",
                    method: "get_task_data",
                })
                .then(function(res) {
                    self.task_data = res['project'];

                });

            return $.when(def4);
        },

    });

    core.action_registry.add('project_dashboard', PjDashboard);

    return PjDashboard;

});