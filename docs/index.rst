.. _index:

=================================
The Storage Project Documentation
=================================
Storage project provides an easy to use `storage python package <https://pypi.python.org/pypi/storage>`_ to retrieve information from `Enterprise Storage Arrays, Switches <http://en.wikipedia.org/wiki/Enterprise_storage>`_ and Servers.

.. note:: `storage python package <https://pypi.python.org/pypi/storage>`_  is currently going through active `development <https://github.com/OpenSRM/storage>`_ where we aim to add more functionality and improve code stability. If you find any bugs/have other use cases, kindly let us know.
.. warning:: The Storage Project is no way linked to any of the storage vendors and comes with no guarantees either from developers or storage vendors, so test thoroughly in your environment before you use in production.

Why storage package
===================
SMI-S which many Enterprise Storage vendors support today requires lot of resources (hardware/human) to get simple things done and we believe storage engineers need an easy way to deal with common tasks like retrieving information and reporting.

`storage python package <https://pypi.python.org/pypi/storage>`_ is a collection of python modules we have written to deal with common tasks that we end up doing frequently and hopefully help other engineers as well. With little customisation you should be automate your provisioning/decommissioning as well.

.. pull-quote:: Ideally we would prefer Enterprise Storage vendors to adopt `REST API <http://en.wikipedia.org/wiki/Representational_state_transfer>`_ as standard instead of/along with SMI-S which will allow storage engineers to hack and automate most of their work in programming language they are most comfortable with.

Installation
============

We strongly recommend you use python virtual environments for all your python projects. If you are not familiar with python virtual environments, kindly read `Virtual Environments - The Hitchhiker's Guide to Python <http://docs.python-guide.org/en/latest/dev/virtualenvs.html>`_ to understand how to create and use python virtual environments.

Once in virtual environment, you can install storage via pip using:

::

    $ pip install virtualenv

Alternatively if you want to install `storage python package <https://pypi.python.org/pypi/storage>`_ in to your standard python environment, you can either install using pip or easy_install or downloading the code and running "python setup.py install"
::

    $ python setup.py install

If you are manually downloading the code and running "python setup.py install", make sure you install dependencies (paramiko >= 1.8.0 and lxml >= 3.2.1) prior to installing storage python package.

Currently Supported Devices/Platforms
=====================================
You can click on below links to read documentation for respective device/platform.

* :doc:`Brocade Switches (FOS 6.x, 7.x) <modules/brocade>`
* :doc:`EMC VMAX Arrays<modules/vmax>`
* :doc:`Red Hat Enterprise Linux (5.x, 6.x) <redhat>`
* :doc:`VMware ESX 4.x and ESXi 5.x <vmware>`
* :doc:`QLogic/Brocade HBA's <servers>`

Changes
=======
From version 0.6, we aim to track all changes to code.

* :doc:`Changes <changes>`

Roadmap
=======
* Extend current functionality and add more methods to currently supported devices. (Ongoing effort)
* NetApp - 2013, probably Q2

Indices and tables
==================
* :ref:`modindex`
* :ref:`genindex`
* :ref:`search`