# Copyright 2012 Managed I.T.
#
# Author: Kiall Mac Innes <kiall@managedit.ie>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import json
import os
import testtools
from designate.context import DesignateContext
from designate.tests import resources

FIXTURES_PATH = os.path.join(resources.path, 'sample_notifications')


class NotificationHandlerMixin(object):
    def get_notification_fixture(self, service, name):
        filename = os.path.join(FIXTURES_PATH, service, '%s.json' % name)

        if not os.path.exists(filename):
            raise Exception('Invalid notification fixture requested')

        with open(filename, 'r') as fh:
            return json.load(fh)

    def test_invalid_event_type(self):
        context = DesignateContext.get_admin_context(all_tenants=True)
        if not hasattr(self, 'plugin'):
            raise NotImplementedError
        event_type = 'invalid'

        self.assertNotIn(event_type, self.plugin.get_event_types())

        with testtools.ExpectedException(ValueError):
            self.plugin.process_notification(context, event_type, 'payload')
