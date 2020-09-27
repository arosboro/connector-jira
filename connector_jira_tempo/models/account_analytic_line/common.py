# Copyright 2019 Camptocamp SA
# Copyright 2019 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.addons.component.core import Component

import simplejson as json

from datetime import datetime

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    jira_tempo_status = fields.Selection(
        selection=[
            ('approved', 'Approved'),
            ('waiting_for_approval', 'Waiting for approval'),
            ('ready_to_submit', 'Ready to submit'),
            ('open', 'Open'),
        ]
    )


class WorklogAdapter(Component):
    _inherit = 'jira.worklog.adapter'

    def read(self, issue_id, worklog_id):
        worklog = super().read(issue_id, worklog_id)
        if self.env.context.get(
                'jira_worklog_no_tempo_timesheets_approval_data'):
            return worklog
        with self.handle_tempo_404():
            worklog['_tempo_timesheets_approval'] = \
                self.tempo_timesheets_approval_read(worklog)
        return worklog

    # This one seems useless ATM.
    # def tempo_read_worklog(self, worklog):
    #     url = self._tempo_timesheets_get_url('worklogs')
    #     r = self.client._session.get(url, params={'dateFrom': '2018-01-01'})
    #     return {}

    def tempo_timesheets_approval_read(self, worklog):
        account_id = worklog['author']['accountId']
        with self.handle_tempo_404():
            date_from = datetime(1969, 12, 31, 19, 00, 00, 00000)
            date_to = datetime.now()
            response = self.tempo.get_timesheet_approvals(dateFrom=date_from, dateTo=date_to, userId=account_id)
        return json.dumps(response, iterable_as_array=True)

    def tempo_timesheets_approval_read_status_by_team(
            self, team_id, period_start):
        with self.handle_tempo_404():
            date_to = datetime.now()
            response = self.tempo.get_timesheet_approvals(dateFrom=period_start, dateTo=date_to, teamId=team_id)
        return json.dumps(response, iterable_as_array=True)
