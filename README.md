<h1>#Book Store</h1>
In the project, used: 
python3
flask
HTML
JavaScript

Packages that need to be installed:\
autopep8==1.5.6\
bcrypt==3.2.0\
cffi==1.14.5\
click==7.1.2\
Flask==1.1.2\
Flask-Bcrypt==0.7.1\
Flask-UUID==0.2\
itsdangerous==1.1.0\
Jinja2==2.11.3\
MarkupSafe==1.1.1\
pycodestyle==2.7.0\
pycparser==2.20\
pysqlite3==0.4.6\
six==1.15.0\
toml==0.10.2\
Werkzeug==1.0.1\

Run main.py file using python3 to start the development server.\
http://127.0.0.1:5000/  will take you to the login page where you can start registering as a Customer.\
Fuctionality to Register a new User will be at http://127.0.0.1:5000/. \
After registering, the customer can login using their credentials which will redirect them to http://127.0.0.1:5000/home.  \
This is the Main Home Page for the Customer which contains all the functionality that the Customer will need to access.\
**For Customer:**
1. Create new order
2. Create new rental
3. Return Rental
4. Cancel an Order: Only that has been placed in last 1 day
5. Check Recommended Books
6. Author Informations: Where they can access 1-degree and 2-degree separated authors
7. Add a review for a book with a optional comment
8. Check their Old Orders and their details
   1. Show the orderID and total and option to see more details of order
   2. Complete detail include the books and quantity with unit price.
10. Browse other Customer Profile: Here they can mark a user trusted or not trusted and view their basic information
11. Request a New Book: Request a book that isn't their in the Book Store already
12. Display all Books
   1. Can Display Detailed Review for Each Book \
   2. Can mark a review useful, very useful or not useful \
13. Search Books By Query: They have option to search book based on the Author, Title, Publisher, Language and can also sort them by Publish Date, Average Score, and avarage score by trsuted users
14. Add Money To Account: They can send request to add money to their account.
15. Mark Trusted/Untrusted: They can mark a user trusted and untrusted directly using their username
16. A user can choose to delete his profile 
17. A user can choose to update his profile

All major Customer Functionality will be found on the home page of customer after they login (http://127.0.0.1:5000/home). \
Functionality to update and delete profile will be found if they go to their profile by selecting it from the menu bar (http://127.0.0.1:5000/profile). 

**For Manager:**
Manager have all the functinality that a customer has except he can't place an order or create a rental. 
Additional Functionality for a Manager:
1. Add New Books
2. Add New Manager
3. Update Inventory of Books
4. Can manager the request of Credits sent by Customer
5. Can manage the request of new books sent by Customer
6. Can View Book Statistics 
7. Can Look at User Awards
8. Display Details of All Customer
9. View Best Employee
10. A user can update his profile

All major functionality that Manager has similar to Customer or the additional facilities can be accessed through the manager home page after they login (http://127.0.0.1:5000/managerhome). \
Functionality to update their profile can be accessed if they go to their profile information by clicking on Profile in the menu bar (http://127.0.0.1:5000/profile).  

Both the Customer and Manager have their Profile view to look at their information or to update basic information of their profile.

All the HTML templates are stored in the template folder. The static directory consist of the style.css file which contains all the styling for the website.
The main.py file that can be found in the home directory that serves the middleware connecting HTML pages with the databse and contains all the code for the functionality
Add Login Page
