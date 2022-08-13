# easygrid

easygrid is an OpenAI Gym environment of simple microgrid simulation for Reinforcement Learning applications. Its goal is to provide an environment that allows for somewhat realistic simulation of controling a microgrid with :  
-- A battery
-- A connection to the global grid
-- Some PV production
-- Some local demand
while also allowing for customization of the environment to test various RL approach that may not be easy to test on a realistic setting. Such customization includes the capacity to easily adapt the amount of power produced locally as well as electricity prices.

It is losely based on pymgrid (https://github.com/Total-RD/pymgrid) and should allow for a simpler framework and understanding, and thus easier customization. 

## Installation

This package uses poetry if you wish to build it yourself.

```bash
git clone https://github.com/YannBerthelot/easygrid.git
cd easygrid
poetry install
```
otherwise, using pip and Test PyPi (not yet released on regular pypi)

```bash
pip install -i https://test.pypi.org/simple/easygrid
```

## Usage

TBD

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## To-do

- Add example of simulation
- Extend usage in readme.
- Add PV production to the framework
- Add logging system to track results

