# Copyright 2016-2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class JiraAdapter(Component):
    """ Generic adapter for using the JIRA backend """
    _inherit = 'jira.webservice.adapter'

    def __init__(self, work_context):
        super().__init__(work_context)
        self._client = None
        self._tempo = None

    @property
    def tempo(self):
        # lazy load the client, initialize only when actually needed
        if not self._tempo:
            self._tempo = self.backend_record.get_tempo_client()
        return self._tempo
