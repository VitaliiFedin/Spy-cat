# Spy Cat
__________________________________________________________________

## How to start

### Clone project
```bash
git clone https://github.com/VitaliiFedin/Spy-cat.git
```
### Start project
To start application you need to create .env file inside root directory (where requirements.txt file is located) with variables (look for examples in file .env.sample).Then open terminal and run this command (make sure you have Docker installed)
```bash
docker-compose up -d --build
```
- -d detach mode, so you can still use terminal
- --build build image
## Access application
__________________________________________________________________

To access application via browser go to [Application](http://localhost:8000/docs)  
Make sure to access this endpoint firstly (it will check database connection and create initial tables in database) [DB](http://localhost:8000/db)
You can download the Postman collection from [this link](https://drive.google.com/file/d/1VPYa71VIQky0UykEeWdqK8aAOEEFV7tf/view?usp=sharing)
