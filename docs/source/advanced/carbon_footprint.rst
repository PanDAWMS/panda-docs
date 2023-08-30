===========================
CO2 estimation of PanDA jobs
===========================

1. Emission intensities of the power grids
------------------------------
PanDA collects periodically *regional emission intensities* (CO2/kWh) of the power grids in the different regions,
where ATLAS Grid computing centers are running. Regions can be at the level of a country (e.g. Europe)
or, for larger countries (e.g. USA), at the level of a state. Emission intensities in a region
can fluctuate over the day, depending on what kind of powers is available (e.g. solar, wind, oil, coal, nuclear).

The ultimate source for our regional emission intensities is: https://www.co2signal.com/.

PanDA also aggregates regional intensities into a *global emission intensity*, taking into account the weight of each
region to the overall ATLAS Grid computing power.

2. Emission intensities of the power grids
------------------------------

In a next step, PanDA estimates the carbon footprint on a per job basis using the following formula:
.. figure:: images/co2_estimation.png
  :align: center

The *core_power_consumption* is currently a hardcoded estimation of how power hungry the hardware or computing center is.
There is flexibility for sites to overwrite this value in the CRIC information system and we hope that
with experience we will have more reliable information.

The *emission intensity* is integrated over the running period of the job. We calculate the carbon footprint of
a job using both the *regional and global emission intensities*.

3. Presentation of the carbon footprint information
------------------------------

We can aggregate the carbon footprint at different levels (task, user, site, Grid) and we are starting to include
the information in monitoring, accounting and task summary emails.

As a general rule, users/task submitters will see the estimation using the *global intensity* (not regional), since
generally they don't have influence over the site - or choosing a location with low carbon intensity will not make the
higher emission regions disappear.

|br|
