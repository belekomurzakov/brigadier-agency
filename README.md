# Brigadier agency
Web application "Brigadier agency" built for my EBC-VWA - Web Applications Development course.

## What I Learned
- Implemented backend using the Flask framework in the Python programming language
- Connected database to store and query data using SQLite
- Designed dynamic web based on different roles and provided authentication process with proper security

## How to run this project on your local machine?
Create virtual environment:
```
python -m venv venv
```
Activate your virtual environment:
```
source venv/bin/activate
```
Install required librabries from *requirements.txt*:
```
pip install -r requirements.txt
```
Enjoy:
```
flask run
```

## Repo Structure
```
/
├─ database/         # Database configuration and creating tables
├─ helpers/          # User class and func for generation hash for password
├─ static/           # Static resources
│  ├─ images/ 
│
├─ template/         # HTML templates
│  ├─ auth/       
│  │  ├─ macros/  
│  ├─ companies/  
│  ├─ contact/    
│  ├─ home/       
│  ├─ positions/  
│  ├─ shifts/     
│
├─ views/             # View functions
├─ README.md          # This file
├─ app.py             # Runner
├─ config.py          # Configuration
└─ requirements.txt   # Required librabries
```

## <p align="center">Entity–relationship model</p>
<p align="center"><img src="https://github.com/belekomurzakov/brigadier-agency/blob/master/static/images/ER.png" alt="ER" width="600"/></p>

## <p align="center">Use case diagram</p>
<p align="center"><img src="https://github.com/belekomurzakov/brigadier-agency/blob/master/static/images/UseCase.png" alt="ER" width="600"/></p>
