Arctic Thermokarst Model

# Running the model
1. get the code by cloning this repo
2. get the  acp data or barrow data at https://drive.google.com/drive/folders/1LIWLwiMtuuMxhaZwV8LztJngzJIB1YHf?usp=sharing 
3. cd to repo root
4. make a copy of control_barrow.yaml or control_acp.yaml in example_control_files as my_control_copy.yaml
5. change the Input_dir field in my_control_copy.yaml to be the absoloute path to the data you downloaded
5. python atm/ATM.py example_control_files/my_control_copy.yaml
6. results will be generated in the directory output

# running tests
from atm root

## run all
`python -m unittest discover tests/`

## run a test
`python tests/test_<file>.py`
