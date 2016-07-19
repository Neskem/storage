:mod:`storage.vmax`
======================

.. currentmodule:: storage.vmax

.. module:: storage.vmax

.. note:: You need to have SYMCLI installed and configured to use this module. Kindly refer to EMC Solutions Enabler documentation if you need help installing and configuring SYMCLI.

:mod:`storage.vmax` provides helper :class:`VMAXArray` class that allows you to run SYMCLI commands from Python by
setting necessary environmental variables and paths.Since SYMCLI is capable of producing XML output for most of the
read-only operations, you should be able to easily extract information you need using lxml xpath.

.. toctree::
   :maxdepth: 2

VMAXArray
---------

.. class:: VMAXArray(SYMCLI_CONNECT, SID, SYMCLI_CONNECT_TYPE='REMOTE', SYMCLI_PATH='/opt/emc/SYMCLI/bin/')

Adds SYMCLI_PATH to $PATH and sets SYMCLI_CONNECT, SYMCLI_SID and SYMCLI_CONNECT_TYPE environment variables.

Below table summarise various arguments used to initialize above class however you can find detailed description for each value by running SYMCLI command: "symcli -def".

+-------------------------------+--------------------------------------------------------------------------------------+
|          Argument             | Definition                                                                           |
+===============================+======================================================================================+
| SYMCLI_CONNECT                | String that represents SYMAPI Server in netcnfg file.                                |
+-------------------------------+--------------------------------------------------------------------------------------+
| SID                           | Symmetrix ID                                                                         |
+-------------------------------+--------------------------------------------------------------------------------------+
| SYMCLI_CONNECT_TYPE           | SYMAPI Server connection type. Valid values are: LOCAL, REMOTE, and REMOTE_CACHED.   |
+-------------------------------+--------------------------------------------------------------------------------------+
| SYMCLI_PATH                   | Solution Enabler install path where SYMCLI commands are available                    |
+-------------------------------+--------------------------------------------------------------------------------------+

Example:

    >>> from storage.vmax import VMAXArray
    >>> vmax34 = VMAXArray('VMAX1234', 34)
    >>> print vmax34
    <VMAXArray - VMAX1234 (SID:34)>
    >>>


command
^^^^^^^
.. classmethod:: VMAXArray.command(cmd, SYMCLI_OUTPUT_MODE='Standard')

:meth:`VMAXArray.command` runs the given command and returns the output. Default SYMCLI_OUTPUT_MODE mode is set to "Standard" as some of the commands do not support XML Output.

Example
::

    >>> #Print symcfg list output
    >>> print vmax34.command('symcfg list ')
    Symmetrix ID: 000000001234

                                    S Y M M E T R I X

                                           Mcode    Cache      Num Phys  Num Symm
        SymmID       Attachment  Model     Version  Size (MB)  Devices   Devices

        000000001234 Local       VMAX40K   5876      737280         9     21615

command_xml
^^^^^^^^^^^
.. classmethod:: VMAXArray.command_xml(cmd)

:meth:`VMAXArray.command_xml` runs etree parsed XML which can be used to run find or xpath methods to retrieve details provided command supports XML_ELEMENT output (Most read-only commands support XML_ELEMENT as output).

Example
::

    >>> # Retrieve Symmetrix ID using xpath.
    >>> a = vmax34.command_xml('symcfg list')
    >>> a.xpath('//symid/text()') #Read lxml xpath documentation on how to navigate through XML.
    ['000000001234']

symcfgDiscover
^^^^^^^^^^^^^^
.. classmethod:: VMAXArray.symcfgDiscover()

:meth:`VMAXArray.symcfgDiscover` runs 'symcfg discover' command.

Example
::

    >>> # Update SYMAPI Database
    >>> vmax34.symcfgDiscover()


getSymmInfo
^^^^^^^^^^^
.. classmethod:: VMAXArray.getSymmInfo()

:meth:`VMAXArray.getSymmInfo` returns Symmetrix Info as a python dictionary with 'microcode_version', 'symid', 'devices', 'physical_devices', 'attachment', 'cache_megabytes', 'model' as keys.

Example
::

    >>> info = vmax34.getSymmInfo()
    >>> info['symid']
    '000000001234'
    >>> info['microcode_version']
    '5876'
    >>> info['model']
    'VMAX40K'

getDiskGroupSummary
^^^^^^^^^^^^^^^^^^^
.. classmethod:: VMAXArray.getDiskGroupSummary()

:meth:`VMAXArray.getDiskGroupSummary` returns Disk Group Summary as a python dictionary with 'disk_group_summary', 'disk_groups', 'symid' as keys.

Example
::

    >>> dg_info = vmax19.getDiskGroupSummary()
    >>> dg_info['symid']
    '000000001234'
    >>> dg_info['disk_group_summary']
    {'units': 'megabytes', 'total': '918566715', 'actual': '918566715', 'free': '143205408'}
    >>> dg_info['disk_groups']
    [{'actual': '17864980', 'disk_size_megabytes': '279140', 'disk_group_name': 'DG_01', 'free': '303', 'rated_disk_size_gigabytes': '300', 'disk_location': 'Internal', 'disks_selected': '64', 'form_factor': '2.5', 'units': 'megabytes', 'disk_group_number': '1', 'technology': 'FC', 'total': '17864980', 'speed': '10000'}, truncated..... ]
    >>>

getThinPoolDetail
^^^^^^^^^^^^^^^^^
.. classmethod:: VMAXArray.getThinPoolDetail()

:meth:`VMAXArray.getThinPoolDetail` returns Thin Pool details as a list.

Example
::

    >>> tp_info = vmax19.getThinPoolDetail()
    >>> tp_info
    [{'subs_percent': '98', 'total_usable_tracks': '140703744', 'total_tracks_gb': '8587.9', 'total_tracks': '140703744', 'dev_emulation': 'FBA', 'technology': 'FC', 'total_used_tracks_gb': '5626.1', 'total_used_tracks': '92178564', 'total_tracks_mb': '8793990', 'total_shared_tracks_gb': '0.0', 'pool_name': 'TP_01', 'total_used_tracks_mb': '5761161', 'dev_config': '2-Way Mir', 'total_usable_tracks_mb': '8793990', 'total_usable_tracks_gb': '8587.9', 'total_shared_tracks_mb': '0', 'total_shared_tracks': '0', 'total_free_tracks': '48525180', 'total_free_tracks_mb': '3032823', 'percent_full': '65', 'disk_location': 'Internal', 'total_free_tracks_gb': '2961.7'}, truncated ..... ]


