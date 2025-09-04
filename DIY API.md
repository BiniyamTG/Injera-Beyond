Step 1: Install Dependencies
pip install fastapi uvicorn motor pydantic pymongo

fastapi → the web framework
uvicorn → ASGI server for running the app
motor → async MongoDB driver
pydantic → data validation
pymongo → optional, only needed if you use sync MongoDB

Step 2: Setup Mongodb 


To DO TASK
'''

'''

--------------------------------------------
1.Create a virtual environment
python -m venv .venv
.venv is the folder for your isolated Python environment.

2. Activate the virtual environment
.\.venv\Scripts\activate
should now see (.venv) in your prompt.

3. Upgrade pip ( this is to sure that pip is updated)
python -m pip install --upgrade pip

4. Install FastApi and uvicorn 
pip install "fastapi[all]" uvicorn

5. Freeze dependencies
pip freeze > requirements.txt
(this is to save all the packages to installed)

6. Git
git init
git add .
git commit -m "initial commit"
At this point, you have Git tracking your project.

7. Create main.py
New-Item main.py -ItemType File


// build all the end points I work with

8. TO run the application use 

python -m uvicorn main:app --reload




