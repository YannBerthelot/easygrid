# easygrid

easygrid is an OpenAI Gym environment of simple microgrid simulation for Reinforcement Learning applications. Its goal is to provide an environment that allows for somewhat realistic simulation of controling a microgrid with :

- A battery.
- A connection to the global grid.
- Some PV production.
- Some local demand

while also allowing for customization of the environment to test various RL approach that may not be easy to test on a realistic setting. Such customization includes the capacity to easily adapt the amount of power produced locally as well as electricity prices.

It is losely based on pymgrid (https://github.com/Total-RD/pymgrid) and should allow for a simpler framework and understanding, and thus easier customization.

The goal is to help build easy to track RL experiments and thus follow this philosophy :

- 100% deterministic.
- parsable configurations defining all the important parameters
- simple modifications of parameters for diverse scenarios
- efficient computation (at the expense of some accuracy)
- extensive logging of parameters to monitor the microgrid
  In addition :
- we chose to remove the forecast part for simplicity and performance
- simpler dependencies for easier integration in a lot of environments

## Installation

This package uses poetry if you wish to build it yourself.

```bash
git clone https://github.com/YannBerthelot/ easygrid.git
cd easygrid
poetry install
```

otherwise, using pip and Test PyPi (not yet released on regular pypi)

```bash
pip install -i https://test.pypi.org/simple/easygrid
```

## Usage

To run the example:

```bash
python -m easygrid
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## To-do

- Extend usage in readme.
- Extend and test logging system to track results
- Add more tests to the simulation
- Add CLI parsing (if necessary)
- Optimize efficiency of code for fast simulations
