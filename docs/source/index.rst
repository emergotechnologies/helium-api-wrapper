.. Helium Api Wrapper documentation master file, created by
   sphinx-quickstart on Wed Nov  2 12:08:24 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Helium Api Wrapper's documentation!
==============================================

This is an API, that provides real-time access and historical data from Helium blockchain.
More about Helium see at https://docs.helium.com/api/blockchain/introduction

Overview on How to Run this API
*******************************
1. Either install a Python IDE or create a Python virtual environment to install the packages required
2. Install required packages from requirements.txt
3. Reach API with commandline

Setup procedure
***************
1. To create a Python Virtual Environment
        - Install virtualenv::

            pip install virtualenv

        - Create virtialenv::

            virtualenv -p python3 <name of virtualenv>

        - Install requirements::

            pip install -r requirements.txt
            poetry install
            poetry shell

2. Type in commandline::

         python helium-api-wrapper --help

Documentation for the Code
==========================
.. toctree::
   :maxdepth: 2
   :caption: Contents:

DataObjects
******************
.. automodule:: src.helium_api_wrapper.DataObjects
   :members:

helpers
******************
.. automodule:: src.helium_api_wrapper.helpers
   :members:

ChallengeAPI
*********************
.. automodule:: src.helium_api_wrapper.ChallengeApi
   :members:
   :undoc-members:


DeviceAPI
*********************
.. automodule:: src.helium_api_wrapper.DeviceApi
   :members:
   :undoc-members:

HotspotAPI
*********************
.. automodule:: src.helium_api_wrapper.HotspotApi
   :members:

TransactionAPI
*********************
.. automodule:: src.helium_api_wrapper.TransactionApi
   :members:

ResultHandler
*********************
.. automodule:: src.helium_api_wrapper.ResultHandler
   :members:

Endpoint
*********************
.. automodule:: src.helium_api_wrapper.Endpoint
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
