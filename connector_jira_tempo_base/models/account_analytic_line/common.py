# Copyright 2018 Camptocamp SA
# Copyright 2019 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.component.core import Component

import json

class WorklogAdapter(Component):
    _inherit = 'jira.worklog.adapter'

    def read(self, issue_id, worklog_id):
        worklog = super().read(issue_id, worklog_id)
        if self.env.context.get('jira_worklog_no_tempo_timesheets_data'):
            return worklog
        with self.handle_404():
            worklog['_tempo_timesheets'] = self.tempo_timesheets_read(
                worklog_id
            )
        return worklog

    def tempo_timesheets_read(self, worklog_id):
        with self.handle_404():
            response = self.tempo.get_worklogs(worklogId=worklog_id)
        return json.dumps(response)
