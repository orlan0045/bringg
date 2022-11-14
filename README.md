# Fedex Integration task

## Installation steps
1. Create venv
2. Install requirements from the root directory
```bash
pip install -r requirements.txt 
```
3. Run local webserver with (from the root directory)
```bash
uvicorn main:app --reload
```
4. Make sure your server is running on `127.0.0.1:8000`(default), otherwise go to `templates/main.html` and change line 21 to whatever your localhost is. 
5. Done

## Usage

1. Go to `http://127.0.0.1:8000/`
2. Enter the code `122816215025810` and click button 'Track'
3. Check the json result below
4. To run tests use `pytest` command

## Example of scenarios 

1. Try the app with original given code - 122816215025810
2. Try the app with some silly code like 123
3. Try the app with another mock code - 403934084723025
4. Try the app with no Internet connection

## Comments

- I have tried this small app with a bunch of other codes given in the Developer's docs pdf 
on `6.1 Test Server Mock Tracking Numbers`
- I've left comments whenever I think it is necessary in order to understand my logic and codestyle
- I decided to make some extra job, so it works better than the original task asked to.
