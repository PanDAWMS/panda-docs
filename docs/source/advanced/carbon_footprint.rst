===========================
Estimation of PanDA job carbon footprint
===========================

1. Carbon emissions and global warming background
------------------------------
Carbon is a chemical element found in various forms on Earth. One of the most common forms is
carbon dioxide (CO2), a greenhouse gas naturally present in the atmosphere.

Global warming refers to the long-term increase in Earth's average surface temperature. It is
primarily driven by the greenhouse effect, where certain gases, including CO2, trap heat from
the sun in the atmosphere, preventing it from escaping into space. This results in a gradual rise
in global temperatures.

Human activities, such as burning fossil fuels (coal, oil, and natural gas) and deforestation, have
significantly increased the concentration of CO2 in the atmosphere. This enhanced greenhouse
effect has led to accelerated global warming, resulting in various environmental impacts,
including rising sea levels, more frequent and severe weather events, and disruptions to
ecosystems.

Efforts to address global warming include reducing carbon emissions, transitioning to cleaner
energy sources, and implementing international agreements like the Paris Agreement to limit
temperature increases and mitigate its consequences.

The ATLAS experiment must continue its scientific program to unlock fundamental insights
into particle physics. However, it is also conscientious about estimating and minimizing CO2
emissions and adopting sustainable practices to reduce its carbon footprint and contribute
to a more environmentally responsible research endeavor. PanDA, as ATLAS' workflow management
system, wants to help by raising awareness on the emissions of computing workloads.

More information on Global warming: https://en.wikipedia.org/wiki/Global_warming_potential
For comparisons to the emissions from other sources, see:  https://en.wikipedia.org/wiki/Carbon_footprint

2. Emission intensities of the power grids
------------------------------
PanDA periodically gathers data on the *regional* emission intensities (measured in gCO2/kWh) of the power grids in
various regions where ATLAS Grid computing centers are operational. These regions can range from individual
countries (e.g. Europe) to states in larger countries (e.g. the USA). Emission intensities within a region
can vary throughout the day, depending on the energy sources available, such as solar, wind, oil, coal, or nuclear power.

Our primary source for regional emission intensity data is: https://www.co2signal.com/.

PanDA also combines these *regional* intensities to calculate a *global* emission intensity, which considers the contribution
of each region to the overall ATLAS Grid computing capacity.

3. Estimation of a job's carbon footprint
------------------------------

In the next step, PanDA calculates the carbon footprint for each job using the following formula:

.. figure:: images/carbon.png
  :align: center

The *core_power_consumption* is currently a fixed estimate of the energy consumption of the hardware or computing center.
There is an option for sites to update this value in the CRIC information system, and over time, we aim to have
more accurate information.

The emission intensity is integrated over the job's runtime. We compute the carbon footprint of a job by considering
both the *regional* and *global* emission intensities.

4. Presentation of the carbon footprint information
------------------------------

We have the capability to aggregate carbon footprint data at various levels, including tasks, users, sites, and
the entire Grid. We are gradually incorporating this information into monitoring, accounting, and task summary emails.

As a general practice, users and task submitters will view estimates using the global emission intensity rather
than regional data. This choice is made for three primary reasons:

 * First, our data is not yet sufficiently detailed to understand which sites are greener than others; hardware lifetimes and lifecycles, the use of renewable energy, how data centers are constructed, and how waste heat is used are among the many considerations when comparing total carbon footprints of sites.
 * Second, pledged CPU does not sit idle — if a user moves their job to another site, a production job will trade places with it, and the total worldwide carbon footprint will be conserved.
 * Third, many users forcing jobs to a limited number of sites will generate a backlog of jobs at that site, as well as additional pressure on network and disks, causing operational difficulties, delays for users and potentially an increased total carbon footprint.


|br|
