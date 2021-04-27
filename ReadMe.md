Step 1: check python version    
    `$ python --version`     
    If your system is not running python version 3.x, you will need to install python 3.    
    *FWIW, mine is 3.8.3 - I think as long as we're all running 3.5 and up, we're good*      

Step 2: create virtual environment     
    I used the instructions on this page: [https://flask.palletsprojects.com/en/1.1.x/installation/#installation]    
    Stop at the heading 'Install Flask'   
    
Step 3: install project dependencies     
    Once the venv is created and activated, you can install all dependencies by running:    
    `$ pip install -r requirements.txt`  
	
Step 4: set up database (if necessary)    
	  The app expects a user 'postgres', so if it is not already there then you must create that user and possibly 
	  create the university (or in future, grocery) database under it.  I think that's how our lab had it set up as well.    
      If your database requires a password, this could also cause issues.
      
Step 4: run app and view web page     
    I used the instructions on this page: [https://flask.palletsprojects.com/en/1.1.x/quickstart/]     
    (now substitute app.py for hello.py)
    See your terminal window for the URL to view the page.