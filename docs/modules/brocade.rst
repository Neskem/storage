:mod:`storage.brocade`
======================

.. currentmodule:: storage.brocade

.. module:: storage.brocade

.. warning:: * Since Brocade does not provide parsable outputs like NetApp (XML) and EMC VMAX (XML), we have to depend on command output to extract the information which is neither elegant nor reliable way of doing it.
 * This module will not work with root/factory accounts as they are supposed to be used only for diagnostics.

:mod:`storage.brocade` provides :class:`BrocadeSwitch` class that implements commonly used Brocade Fabric OS commands as
python methods and a generic :meth:`BrocadeSwitch.command` method which can be used to implement additional
functionality to automate daily tasks.

.. toctree::
   :maxdepth: 2

BrocadeSwitch
-------------

.. class:: BrocadeSwitch(hostname, username, password, timeout=60)

Establish :class:`SSHConnection` to Brocade switch using :class:`BrocadeSwitch` class. :class:`BrocadeSwitch` takes hostname/IP, username, password and timeout(optional) as arguments to create SSH session with Switch.


Example:

    >>> from storage.brocade import BrocadeSwitch
    >>> switch_A_1 = BrocadeSwitch('192.168.1.100', 'user', 'password')
    >>> print switch_A_1
    <BrocadeSwitch (192.168.1.100)>
    >>>

aliShow
^^^^^^^
.. classmethod:: BrocadeSwitch.aliShow(pattern='*', fid=None)

:meth:`BrocadeSwitch.aliShow` implements aliShow command with pattern '*' and fid=None as default arguments and returns output as dictionary with alias name as key and members(type:list) as value . If you use Virtual Fabrics on your switches, you can run aliShow on logical switch by specifying fid.

Example:
    >>> #Return Alias that match 'HBA_A_HR_ORADB01' on Virtual Fabric with FID 101
    >>> switch_A_1.aliShow(fid=101, pattern='HBA_A_HR_ORADB01')
    {'HBA_A_HR_ORADB01': ['10:00:00:05:1E:00:00:01']}
    >>>
    >>> #Return all Aliases that match given pattern ('HBA_A_HR_ORADB*') on Virtual Fabric with FID 101
    >>> switch_A_1.aliShow(fid=101, pattern='HBA_A_HR_ORADB*')
    {'HBA_A_HR_ORADB01': ['10:00:00:05:1E:00:00:01'], 'HBA_A_HR_ORADB02': ['10:00:00:05:1E:00:00:02'], '...(remaining elements truncated)...'}
    >>>
    >>> #Returns all aliases on base switch for the user as FID is not specified.
    >>> switch_A_1.aliShow()
    (output truncated)
    >>>


.. note:: We are returning members as lists because alias can have one or more members even though most of the
 environments may use one-to-one alias<->WWPN mapping.

fabricShow
^^^^^^^^^^
.. classmethod:: BrocadeSwitch.fabricShow(membership=False, chassis=False, fid=None)

:meth:`BrocadeSwitch.fabricShow` implements fabricShow command and takes optional arguments membership, chassis and fid
to mimic membership, chassis options when using fabricShow command. Returns dictionary with Switch ID as key and rest as
members.

Example:

    >>> # Return fabricShow output as dict with SwitchID (Hex) as key and list with core pid, WWN, Ethernet IP, FC IP
    >>> # and name as value
    >>> switch_A_1.fabricShow(fid=101)
    (output truncated)
    >>> # Return fabricShow output as dict with SwitchID (Hex) as key and list with core pid, name and Ethernet IP as value
    >>> switch_A_1.aliShow(membership=True, fid=101)
    (output truncated)
    >>> # Return fabricShow output as dict with SwitchID (Hex) as key and list with core pid, Name, Ethernet IP, Chassis
    >>> # WWN and Chassis name as value.
    >>> switch_A_1.aliShow(chassis=True, fid=101)
    (output truncated)


get_alias_zones
^^^^^^^^^^^^^^^
.. classmethod:: BrocadeSwitch.get_alias_zones(alias, fid=None)

:meth:`BrocadeSwitch.get_alias_zones` returns all zones that alias is member of.

Example:

    >>> # Return zones for alias 'HBA_A_HR_ORADB01'
    >>> switch_A_1.get_alias_zones('HBA_A_HR_ORADB01', fid=101)
    ['HBA_A_HR_ORADB01_VMAX1234', ]
    >>>


get_wwn_aliases
^^^^^^^^^^^^^^^
.. classmethod:: BrocadeSwitch.get_wwn_aliases(wwn, fid=None)

:meth:`BrocadeSwitch.get_wwn_aliases` returns aliases for given WWN if it exists in the configuration.

Example:

    >>> # Return alias for WWPN '10:00:00:05:1E:00:00:01'
    >>> switch_A_1.get_wwn_aliases('10:00:00:05:1E:00:00:01', fid=101)
    ['HBA_A_HR_ORADB01', ]
    >>> switch_A_1.get_wwn_aliases('10:00:00:05:1E:00:00:01')
    []
    >>>

is_wwn_on_fabric
^^^^^^^^^^^^^^^^
.. classmethod:: BrocadeSwitch.is_wwn_on_fabric(wwn, fid=None)

:meth:`BrocadeSwitch.is_wwn_on_fabric` returns True if given WWN is logged onto the Fabric, otherwise returns False.
This makes uses of nodefind, so it will match both WWPN and WWNN.

Example:

    >>> # Check if WWPN '10:00:00:05:1E:00:00:01' exists on Fabric
    >>> switch_A_1.is_wwn_on_fabric('10:00:00:05:1E:00:00:01', fid=101)
    True
    >>> switch_A_1.is_wwn_on_fabric('10:00:00:05:1E:00:00:01')
    False
    >>>

switchName
^^^^^^^^^^
.. classmethod:: BrocadeSwitch.switchName(fid=None)

:meth:`BrocadeSwitch.switchName` returns the switch name as string.

Example:

    >>> # Returns Brocade FC switch name
    >>> switch_A_1.switchName()
    LON_DCX8510_A_1
    >>> switch_A_1.switchName(fid=101)
    LON_DCX8510_A_1_FINANCE

switchShow
^^^^^^^^^^
.. classmethod:: BrocadeSwitch.switchShow(fid=None)

:meth:`BrocadeSwitch.switchShow` returns the switchShow output as dictionary.

.. note:: Since the port details line vary depending on if switch is director or not, a helper method :meth:`BrocadeSwitch.isDirectorClass` (Returns True if Director class, otherwise False) is provided to identify the same.

Example:
    >>> a_1_switch_show = switch_A_1.switchShow()
    >>> type(a_1_switch_show)
    <type 'dict'>
    >>> a_1_switch_show.keys()
    ['FC Router', 'switchWwn', 'switchRole', 'LS Attributes', 'zoning', 'switchState', 'switchId', 'switchDomain', 'switchType', 'switchName', 'Allow XISL Use', 'switchBeacon', 'ports', 'switchMode']
    >>> #Returns Brocade FC switch role
    >>> a_1_switch_show['switchRole']
    Principal
    >>> #Returns Brocade FC switch domain
    >>> a_1_switch_show['switchDomain']
    41
    >>> switch_A_1.isDirectorClass(a_1_switch_show['switchType'])
    True

version
^^^^^^^
.. classmethod:: BrocadeSwitch.version()

:meth:`BrocadeSwitch.version` returns the version as dictionary.

Example:
    >>> # Returns Brocade Switch version information
    >>> switch_A_1.version()
    {'Kernel': '2.6.14.2', 'Flash': 'Sun Nov 20 02:04:57 2011', 'BootProm': '1.0.15', 'Fabric OS': 'v6.4.2b', 'Made on': 'Tue Sep 20 18:45:13 2011'}
    >>> # Get only Fabric OS version (Look at the dictionary keys above)
    >>> switch_A_1.version()['Fabric OS']

zoneShow
^^^^^^^^
.. classmethod:: BrocadeSwitch.zoneShow(pattern='*', fid=None)

:meth:`BrocadeSwitch.zoneShow` implements zoneShow command with pattern '*' and fid=None as default arguments and
returns output as dictionary with zone name as key and members(type:list) as value. If you use Virtual Fabrics on
your switches, you can run zoneShow on logical switch by specifying fid.

Example:

    >>> # Returns Exact Zone with name 'HBA_A_HR_ORADB01_VMAX1234' on Virtual Fabric with FID 101
    >>> switch_A_1.zoneShow(fid=101, pattern='HBA_A_HR_ORADB01_VMAX1234')
    {'HBA_A_HR_ORADB01_VMAX1234': ['HBA_A_HR_ORADB01', 'VMAX1234_PG44']}
    >>> # Returns all zones that match pattern 'HBA_A_HR_ORADB*_VMAX1234' on Virtual Fabric with FID 101
    >>> switch_A_1.zoneShow(fid=101, pattern='HBA_A_HR_ORADB*_VMAX1234')
    {'HBA_A_HR_ORADB01_VMAX1234': ['HBA_A_HR_ORADB01', 'VMAX1234_PG44'], 'HBA_A_HR_ORADB02_VMAX1234': ['HBA_A_HR_ORADB02', 'VMAX1234_PG13'], '...(remaining elements truncated)...'}
    >>> #Returns all zones on base switch for the user as FID is not specified.
    >>> switch_A_1.aliShow()
    Output truncated

command
^^^^^^^
.. classmethod:: BrocadeSwitch.command(cmd)

If any of the above methods do not meet your needs or need to overwrite the behaviour, subclass :class:`BrocadeSwitch`
and you you can easily override existing method or write your own method using :meth:`BrocadeSwitch.command`.
:meth:`BrocadeSwitch.command` runs any given command against switch and returns tuple (output, error) with which you
can implement any implement method you need.

Example:

::

    from storage.brocade import BrocadeSwitch
    class MyBrocadeSwitch(BrocadeSwitch):
        """
        Extending BrocadeSwitch to implement additional methods that may suit our environment
        """
        def wwn(self):
            """Displays the world wide name (WWN) of the switch or chassis."""
            output, error = self.command('wwn')

            if output:
                return "".join(output).strip()

        def bannerShow(self, fid=None):
            """Displays the banner text."""
            cmd = "bannershow"
            if fid:
                cmd = self.command_with_fid(cmd, fid)
            output, error = self.command(cmd)

            if output:
                return "".join(output) # Not stripping here as sometimes we may use blank chars or tabs for formatting.

Using MyBrocadeSwitch in action
::

    >>> import MyBrocadeSwitch
    >>> switch_A_1 = MyBrocadeSwitch('192.168.1.100', 'user', 'password')
    >>> # Print SwitchName. Since we sub-classed from BrocadeSwitch, we will have access to all parent methods.
    >>> switch_A_1.switchName()
    LON_DCX8510_A_1
    >>> # Displays the world wide name (WWN) of the switch or chassis
    >>> MyBrocadeSwitch.wwn()
    10:00:00:05:1e:7a:7a:00
    >>> # Displays the banner on the base swtich for the user.
    >>> MyBrocadeSwitch.bannerShow()
    '\t\tMy Switch\t\t'
    >>> print MyBrocadeSwitch.bannerShow()
    My Switch
    >>> MyBrocadeSwitch.bannerShow(fid=101)
    '\t\tYou are now on Virtual Fabric with FID 101\t\t'

