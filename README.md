# Project
Book Store
In the project, used: 
python3
flask
HTML
JavaScript

Packages that need to be installed:
autopep8==1.5.6
bcrypt==3.2.0
cffi==1.14.5
click==7.1.2
Flask==1.1.2
Flask-Bcrypt==0.7.1
Flask-UUID==0.2
itsdangerous==1.1.0
Jinja2==2.11.3
MarkupSafe==1.1.1
pycodestyle==2.7.0
pycparser==2.20
pysqlite3==0.4.6
six==1.15.0
toml==0.10.2
Werkzeug==1.0.1

Run main.py file using python3 to start the development server.
http://127.0.0.1:5000/  will take you to the login page where you can start registering as a Customer..
Fuctionality to Register a new User will be at http://127.0.0.1:5000/.
After registering, the customer can login using their credentials which will redirect them to http://127.0.0.1:5000/home
This is the Main Home Page for the Customer which contains all the functionality that the Customer will need to access.
**For Customer:**
Create new order
Create new rental
Return Rental
Cancel an Order: Only that has been placed in last 1 day
Check his suggested Books
Author Informations: Where they can access 1-degree and 2-degree separated authors
Add a review for a book
Check their Old Orders and their details
Browse other Customer Profile: Here they can mark a user trusted or not trusted and view their basic information
Request a New Book: Request a book that isn't their in the Book Store already
Display all Books
Search Books By Query: They have option to search book based on the Author, Title, Publisher, Language and can also sort them by Publish Date, Average Score, and avarage score by trsuted users
Add Money To Account: They can send request to add money to their account.
Mark Trusted/Untrusted: They can mark a user trusted and untrusted directly using their username

**For Manager:**
Manager have all the functinality that a customer has except he can't place an order or create a rental. 
Additional Functionality for a Manager:
Add New Books
Add New Manager
Update Inventory of Books
Can manager the request of Credits sent by Customer
Can manage the request of new books sent by Customer
Can View Book Statistics 
Can Look at User Awards
Display Details of All Customer
View Best Employee

Both the Customer and Manager have their Profile view to look at their information or to update basic information of their profile.

All the HTML templates are stored in the template folder. The static directory consist of the style.css file which contains all the styling for the website.
The main.py file that can be found in the home directory that serves the middleware connecting HTML pages with the databse and contains all the code for the functionality
