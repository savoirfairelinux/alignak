#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2016: Alignak team, see AUTHORS.txt file for contributors
#
# This file is part of Alignak.
#
# Alignak is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Alignak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Alignak.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This file incorporates work covered by the following copyright and
# permission notice:
#
#  Copyright (C) 2009-2014:
#     Jean Gabes, naparuba@gmail.com
#     Hartmut Goebel, h.goebel@goebel-consult.de
#     Grégory Starck, g.starck@gmail.com
#     Sebastien Coavoux, s.coavoux@free.fr

#  This file is part of Shinken.
#
#  Shinken is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Shinken is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Shinken.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from alignak_test import AlignakTest


class TestStarMemberGroup(AlignakTest):
    def setUp(self):
        self.setup_with_file('cfg/cfg_star_in_group_members.cfg')
        self._sched = self.schedulers['scheduler-master'].sched

    def test_star_in_group_member(self):
        """Test hostgroup with wildcard members and service with wildcard hostname
        """
        hg = self._sched.conf.hostgroups.find_by_name('ping-servers')

        assert hg is not None

        host_0 = self._sched.conf.hosts.find_by_name('test_host_0')
        router_0 = self._sched.conf.hosts.find_by_name('test_router_0')

        # host0 and router0 should be in ping-servers members
        assert host_0.uuid in hg.members
        assert router_0.uuid in hg.members

        svc_ping = self._sched.conf.services.find_srv_by_name_and_hostname('test_host_0', 'PING')
        assert svc_ping is not None

        # TEST service should be linked to host0
        svc_test = self._sched.services.find_srv_by_name_and_hostname("test_host_0", "TEST")
        assert svc_test is not None

        # TEST_HNAME_STAR service should be linked to host0
        svc_star = self._sched.services.find_srv_by_name_and_hostname("test_host_0", "TEST_HNAME_STAR")
        assert svc_star is not None


if __name__ == '__main__':
    unittest.main()
