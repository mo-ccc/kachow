# Overview
This project was created with the purpose to provide tech companies with an interface for managing and tracking the bugs within their projects. On login users will be presented with an overview dashboard. 

From there users can use the console to access various pages. One of the pages will allow users to view/submit/manage bugs (mark them as closed or open). The other pages such as the calendar page will serve as a compliment allowing the users to see a calendar for when bugs were submitted and squashed. Users will be able to edit their profile information and are able to upload profile pictures to represent themselves. 

The page where bugs are submitted will allow comments and collaboration between users and attachments are able to be submitted. 
Admins will be able to create new users and allocate them roles and teams. Users will be able to track their own performance and contributions from their personalised page.

# Installation instructions
The app makes use of the venv pip package to create a virtual environment. Therefore the package will need to be installed in order to run the app. There after the install instructions are as below:

- Clone the repo
- CD into the kachow folder
- Make sure venv is installed: pip install venv
- Create the virtual environment: python3 -m venv venv
- Activate the virtual environment: source venv/bin/activate
- Install the dependencies from requirments.txt: pip3 install -r requirements.txt
- Run the app: python src/main.py

# Wireframes
**Dashboard:**
Displays graphics related to the number of bugs. Menu options on the left allow the user to access different pages. clicking user profile in top right allows them to edit their settings. Notifications may also be displayed on this page.
![dashboard](docs/wireframes/dashboard.png)

**Login:**
![login](docs/wireframes/login-page.png)

**Settings:**
![settings](docs/wireframes/user-edit-page.png)
##### email and role is uneditable from this page

**Threads:**
Page containing all thread elements. the menu buttons filter which threads are displayed.
![threads](docs/wireframes/threads-page.png)

**Single Thread:**
Page for viewing a single thread. Posts are made here. at the end of the page a form will take user input to add replies to the thread. replies can contain quote blocks and will notify the replied to.
![threads](docs/wireframes/thread.png)

**Admin management page:**
Page that only the admins can view. Will allow them to create and remove accounts as well as edit roles and details of pre-existing accounts.
![management](docs/wireframes/admin-member-management-page.png)

# Class Diagrams (WIP)
![cd](docs/class_diagram.png)