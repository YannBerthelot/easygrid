
<a id='changelog-0.1.9'></a>
# 0.1.9 — 2022-09-01

## Added

- Added coverage as dev dependecy and allowed configuration to exclude lines

## Changed

- Modified tests to prevent graphs from showing
<a id='changelog-0.1.8'></a>

# 0.1.8 — 2022-08-14

## Added

- Added penalty for overcharge in the battery
- Added impact of the grid elements in the run timestep method of Microgrid.
- Added parameters to control the penalties in the config.
- Added logging of cost and energy at each timestep
- Extended tests to account for new code.
- Basic example when running the module
- Graph showing capacity

<a id='changelog-0.1.2'></a>

# 0.1.2 — 2022-08-13

## Added

- Added basic PV functionnalities (including production scaling).

## Changed

- Changed minimum coverage to 100%.
- Add scaling factor to prices (import and export) in Grid object.
- Changed line limit to 88 characters for isort and black.

## Fixed

- Fixed incapacity to have 100% coverage due to an assert statement

<a id='changelog-0.1.2'></a>

# 0.1.2 — 2022-08-13

## Added

- Types files for collecting different custom types
- Grid class to represent the grid object for importing/exporting operations

## Changed

- Changed from Python 3.8 to Python 3.9 for type subscription

<a id='changelog-0.1.2'></a>

# 0.1.2 — 2022-08-04

## Added

- Added CI for automatic publication to Test PyPi

## Fixed

- Fixed Coverage support on CI github actions

<a id='changelog-0.1.2'></a>

# 0.1.2 — 2022-08-04

## Added

- Added pylint config to the repo for easier consistency between CI and local env.
- Docstrings for Microgrid and Battery
- Added reward function template

## Changed

- Reworked the charge and discharge of the battery.

## Fixed

- Fixed a bug where discharging meant charging the battery
