![build status](./images/logo.png)

___
<p align="center"> A Simple deduction game based on facial reactions </p>

![build status](https://github.com/ThomasRubini/SAE-A2-TruthInquiry/actions/workflows/tests.yml/badge.svg)

## Screenshots
![title](./images/title.png)
![interrogation](./images/Interogation.png)
![debrief](./images/debrief.png)

___
## How to run

In ordre to run the server you will need ```python3``` and ```python3-pip```. 

Then to install the depedencies run ```pip install -r requirement.txt```. 

If you want to contribute you may install the dev dependecies as well : ```pip install -r dev-requirement.txt```

You will need to create the .env file from the .env.dist and fill the parameters. Do take note that this website was conceived to run on a mariadb sql database, however this can be easly changed in the data_access.py file. In order to fill the remote database with the data availible in this repo you will need to run the remote.py script : ```python3 truthinquiry/logic/data_persistance/remote.py ```

To launch the web server you will need to fill the .env file with the database connection and to fill the flask_secret within it then you can use 

 ```flask run```

to launch the web server

To run the tests, run the command ```python3 -m pytest --verbose```.

## Contributors

[CAZALS Matthias](https://github.com/mathiascazals)

[RUBINI Thomas](https://github.com/ThomasRubini)

[SIMAILA Djalim](https://github.com/DjalimSimaila)

[V Audric](https://github.com/AudricV)

[SujetDelta](https://github.com/SujetDelta)
