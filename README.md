# ADA-Artificial-Digital-Assistant
An artificial digital assistant for pc, more dynamic able to defines names and softwares as parameters to open when needed.

After the initial pull
  - user has to run the trainning.py to execute a model of the intents to a readable machine language (automatically creating)
  - test the JarvisBrain.py for compatibility issues

If everything working according to the need you can continue with project

If the user has to add more 3rd party softwares,
  - open absolute_paths_softwares.json and update it based on the given examples
    - ex: "sft_name" : "steam", this the software name where user asking to open from the AI
          "path": "D:\\Steam\\steam.exe", absolute path for the given software
