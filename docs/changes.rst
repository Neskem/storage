===========================
0.0.6 (Under Development)
===========================

.. warning::  **This change has some backwards incompatibilities from previous versions and might break your existing code. Kindly read Backwards Incompatibilities section to understand what changed.**

Features
========

servers.py
----------
 - ESXi 5.x gets it's own class ESXiServer.

brocade.py
----------
 - Method is_wwn_on_fabric added, checks if given WWN (WWNN/WWPN) is logged on to the fabric.
 - Method get_wwn_aliases added, returns alias(es) for give WWN. This makes use of aliShow


Bug Fixes
=========

- SSHSession now returns error correctly, earlier both output and error returned output due to typo.

Backwards Incompatibilities
===========================

ssh.py
------

SSHSession class now refers 'host' as host rather than hostname. Should not impact you directly unless you are using SSHSession directly.

servers.py
----------

**servers.py re-written from scratch and might break some functionality.**

 - LinuxServer class now replaced with GenericLinuxServer
 - RedhatServer class now replaced with RedHatServer (notice uppercase H in RedHatServer)
 - Method get_hostname method replaced with property hostname.
 - Method has_hbas method replaced with property has_hba. Property has_hba now implemented locally in RedHatServer, ESXServer and ESXiServer.
 - Method get_hba_manufacturer method replaced with property hba_manufacturer. Property hba_manufacturer now implemented locally in RedHatServer, ESXServer and ESXiServer.
 - Method get_wwpns method replaced with property wwpns
 - As of now methods get_os_version, check_hba_driver and get_bcu_version are removed and not re-written yet. We do want to get those details, especially HBA driver versions.

brocade.py
----------
 - Method find_wwn renamed to more meaningful is_wwn_on_fabric.
 -

