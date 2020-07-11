# AtypicalCognition
cognitive science project 2019

###### installing requirements
assumes python and pip are pre-installed  
if not, install them prior to running this command

```
pip install -r requirements.txt
```

###### to simulate agent
1. genetrate an agent (edit agentSimulation.py)
```
line 54 a = AgentSimulation(config_atypical) # for atypical agent
line 54 a = AgentSimulation(config_typical) # for typical agent
```
2. Simulate the agent's memory
```
python agentSimulation.py 
```

###### to generate covariance
```
jupyter notebook Correlation.ipynb

```
###### hyperparameter tuning
```
nBackTest.py
```

