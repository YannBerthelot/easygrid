
<a id='changelog-0.4.0'></a>
# 0.4.0 — 2022-09-13

## Changed

- Switched to gym 0.21 for stable-baselines3 compatibility

<a id='changelog-0.3.0'></a>
# 0.3.0 — 2022-09-13

## Removed

- Removed realistic config as it is deprecated towards pymgrid.

## Added

- Added basic price timseries in the data

## Changed

- Changed config of timeseries from np.array to path to csv files.

## Fixed

- Allow to properly save config in json format
<a id='changelog-0.3.0'></a>

# 0.3.0 — 2022-09-12

## Removed

- Remove "Action" type as it would be too heavy to cast at every timestep, plus input is np.array

## Added

- Added mypy to the pipeline for type checking)
- Extended the gym env to init spaces (action and obs).
- Encapsulate the microgrid into a working gym environment.

## Changed

- Switched typing to using pydantic.
- Changed example to gym

<a id='changelog-0.1.9'></a>

# 0.1.9 — 2022-09-07

## Added

- Added load and pv data from pymgrid
- Added pymgrid_config to be used in experiments.
- Added config extraction from different classes
- Added battery configuration from duration and mean load
- Added mean attributes to classes if applicable

## Changed

- Version number tracking is now handled in pyproject.toml entirely

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

- Types files for collecting different custom types
- Grid class to represent the grid object for importing/exporting operations

## Changed

- Changed minimum coverage to 100%.
- Add scaling factor to prices (import and export) in Grid object.
- Changed line limit to 88 characters for isort and black.
- Changed from Python 3.8 to Python 3.9 for type subscription

## Fixed

- Fixed incapacity to have 100% coverage due to an assert statement

<a id='changelog-0.1.2'></a>

# 0.1.2 — 2022-08-04

## Added

- Added CI for automatic publication to Test PyPi
- Added pylint config to the repo for easier consistency between CI and local env.
- Docstrings for Microgrid and Battery
- Added reward function template

## Changed

- Reworked the charge and discharge of the battery.

## Fixed

- Fixed Coverage support on CI github actions
- Fixed a bug where discharging meant charging the battery

<a id='changelog-0.1.2'></a>

# 2022-08-02

## Added

- Added tox for quality checks
- Added more tests
- Added test coverage check and set it to 95% coverage
- Scriv to track changes in the changelog
- Basic battery implementation
- Basic battery tests

## Changed

- Switch to only supporting python3.8, at least for now
