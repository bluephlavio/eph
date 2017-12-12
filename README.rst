.. image:: https://travis-ci.org/bluephlavio/eph.svg?branch=master
   :target: https://travis-ci.org/bluephlavio/eph

.. image:: https://coveralls.io/repos/github/bluephlavio/eph/badge.svg?branch=master
   :target: https://coveralls.io/github/bluephlavio/eph?branch=master

Readme
======

The ``eph`` package provides some useful functions, classes and tools
to *retrieve*, *parse* and *manipulate* ephemerides
in an `astropy <http://www.astropy.org/>`_-compatible way.

See `eph-howto`_ (jupyter notebook) for more info.

.. _eph-howto: https://nbviewer.jupyter.org/github/bluephlavio/edu/blob/master/eph-howto.ipynb

Basic Usage
-----------

.. code-block:: python

    import eph

    req = eph.JplReq() # create the request
    req.read('eph.ini', section='jplparams') # read parameters from 'jplparams' section in 'eph.ini'
    req.set({
        'COMMAND': 'venus',
        'START_TIME': '2007-11-17',
        'STOP_TIME': '2017-4-22'
        'STEP_SIZE': '10d'
        }) # set parameters from dictionary
    req['OBJ_DATA'] = False # set parameter dict-like
    req.csv = True # set parameter as attributes
    req.set(
        TABLE_TYPE='V',
        VEC_LABELS=False,
        VEC_TABLE=1
    ) # set position vectors output

    res = req.query() # perform the request obtaining a response from Jpl Horizons service
    e = res.parse() # parse the ephemeris in an astropy QTable

    from astropy.io import ascii

    ascii.write(e, format='csv') # write output data

The content of ``eph.ini`` can be something like this
(see ftp://ssd.jpl_process.nasa.gov/pub/ssd/horizons_batch_example.long
for a complete description of JPL parameters)

.. code-block:: ini

    [jplparams]
    MAKE_EPHEM=YES
    REFERENCE_PLANE=ECLIPTIC
    REF_SYSTEM=J2000
    OUT_UNITS=AU-D

Shortcuts
---------

``eph`` package defines also some useful shortcut functions to easily access Jpl Horizons data.
Instead of building a JplReq and get back a JplRes to parse, you can get an astropy QTable with

.. code-block:: python

    from eph import *

    e = get('2000-1-1', '2018-1-1', 299, step=100).


This returns by default an observer table. If you want vectors, type

.. code-block:: python

    e = vec('2000-1-1', '2018-1-1', 299, step=100).


Command line tool
-----------------

``eph`` package also provides a command line tool:

.. code-block:: bash

    $ eph 2007-11-17 2017-4-22 venus

This command gives you an ephemeris table of Venus starting from 2007-11-17 to 2017-4-22.
You can also change the reference frame, the time-step size, the output etc..
through the options provided. Check available options typing

.. code-block:: bash

    $ eph --help
