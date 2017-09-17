Cel
===

.. image:: https://travis-ci.org/a-musing-moose/cel.svg?branch=master
    :target: https://travis-ci.org/a-musing-moose/cel

Cel is the first part of a simple Function as a Service (FaaS) framework. It provides a command line tool to start, build and run locally individual Python function apps.


Prerequisite
------------

Cel requires that Docker_ is installed and running.



Getting Started
---------------

#. Ensure you have created and activated a virtual environment
#. run ``pip install cel``
#. Start an app using ``cel start <app_name>``

This will create a folder named *<app_name>* containing you new application

Usage
-----

To build:

.. code-block:: bash

    cel build


To run locally:

.. code-block:: bash

    cel run


The ``cel`` command line tool, as well as it's sub-commands have help documentation which you can access using the ``--help`` command line flag.



.. _docker: https://www.docker.com/
