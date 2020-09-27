# Copyright: 2015 LasLabs, Inc.
# Copyright 2016-2019 Camptocamp SA
# Copyright 2019 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api

try:
    from tempoapiclient import client
except ImportError:
    pass  # already logged in components/backend_adapter.py

import logging

_logger = logging.getLogger(__name__)


class JiraBackend(models.Model):
    _inherit = 'jira.backend'

    tempo_auth_token = fields.Char(
        help="Cloud uses a different authorization for api.tempo.io."
    )

    @api.model
    def get_tempo_client(self):
        self.ensure_one()
        # tokens are only readable by connector managers
        backend = self.sudo()
        _logger.print(backend.tempo_auth_token[3:8])
        return client.Tempo(
            auth_token=backend.tempo_auth_token,
            base_url='https://api.tempo.io/core/3',
        )
