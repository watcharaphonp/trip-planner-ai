## Introduction

crewAI is designed to facilitate the collaboration of role-playing AI agents.
This is a collection of examples of different ways to use the crewAI framework to automate the processes.
By [@joaomdmoura](https://x.com/joaomdmoura).

## Setup
1. Create file `.env` and add the same variables as the `.env.example` file

2. Prepare environment
   ```make prepare```

3. Activate virtual environment
   ```source "venv"/bin/activate```

4. Install dependencies
   ```make install```
   or
   ```make i```

## Start LiteLLM Proxy
1. Open your terminal

2. Activate virtual environment by running the following command in your terminal
   ```source "venv"/bin/activate```
   
3. Start LiteLLM proxy by running the following command in your terminal 
   ```litellm```
   
4.You will see the url `http://localhost:4000` (default port is `4000`)


## Start Trip Planner Services
1. Open your terminal

2. Activate virtual environment by running the following command in your terminal
   ```source "venv"/bin/activate```
Run
   ```make run```
   or
   ```make r```

3.You will see the url `http://localhost:3001` (default port is `3001`)
