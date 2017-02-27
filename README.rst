Readme
======

The ``eph`` package provides some useful classes to retrieve and manipulate ephemerides. 

**Basic Usage**

.. code-block:: python

	import eph

	req = eph.JPLReq() # create the request
	req.read('defaults.cfg', 'jplparams') # read parameters from file
	req.set({'COMMAND': '399', 'START_TIME': '2017-01-01', 'STOP_TIME': '2017-12-31'}) # set parameters from dictionary
	res = req.request() # perform the request obtaining a response from jpl
	eph = res.ephemeris # extract the ephemeris from the response

	print(eph) # print data

The content of ``defaults.cfg`` can be something like this (see ftp://ssd.jpl.nasa.gov/pub/ssd/horizons_batch_example.long for a complete description of JPL parameters)

.. code-block:: ini

	[jplparams]
	CENTER='@0'
	OBJ_DATA=NO
	MAKE_EPHEM=YES
	TABLE_TYPE=VECTORS
	VEC_TABLE=1
	REFERENCE_PLANE=ECLIPTIC
	REF_SYSTEM=J2000
	OUT_UNITS=AU-D
	CSV_FORMAT=YES
	VEC_LABEL=NO
	STEP_SIZE=1d

