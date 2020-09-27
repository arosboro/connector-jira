# Copyright 2019 Camptocamp SA
# Copyright 2019 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.addons.component.core import Component

import simplejson as json
import logging

from datetime import datetime, timedelta


_logger = logging.getLogger(__name__)

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
        # with self.handle_tempo_404():
        #     worklog['_tempo_timesheets_approval'] = \
        #         self.tempo_timesheets_approval_read(worklog)
        return worklog

    @staticmethod
    def prior_week_end(self):
        return datetime.now() - timedelta(days=((datetime.now().isoweekday() + 1) % 7))

    @staticmethod
    def prior_week_start(self):
        return self.prior_week_end() - timedelta(days=6)

    # This one seems useless ATM.
    # def tempo_read_worklog(self, worklog):
    #     url = self._tempo_timesheets_get_url('worklogs')
    #     r = self.client._session.get(url, params={'dateFrom': '2018-01-01'})
    #     return {}

    def tempo_timesheets_approval_read(self, worklog):
        account_id = worklog['author']['accountId']
        date_from = datetime.now() - timedelta(days=364)
        date_to = datetime.now()
        prefetch = self.tempo.get_periods(date_from, date_to)
        result = []
        for period in prefetch:
            with self.handle_tempo_404():
                response = self.tempo.get_timesheet_approvals(dateFrom=period['from'], dateTo=period['to'],
                                                              userId=account_id)
                for approval in response:
                    result.append(approval)
        return json.dumps(result)

    def tempo_timesheets_approval_read_status_by_team(
            self, team_id, period_start):
        with self.handle_tempo_404():
            date_to = datetime.strptime(period_start, '%Y-%m-%d') + timedelta(days=6)
            response = self.tempo.get_timesheet_approvals(dateFrom=period_start, dateTo=date_to, teamId=team_id)
            _logger.info("%s", json.dumps(response, iterable_as_array=True))
            result = []
            for record in response:
                result.append(record)
        return json.dumps(result[0])
