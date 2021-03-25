# Quizzical
<hr>

[Quizzical]() was created for educators, learners and quiz enthusiasts to find and share topical mini-quizzes. 
The main goal of the site is to support and enhance the work of teachers and the learning of students whilst facilitating fun and friendly competition.
Quizzical was developed by Tom Haysom [thaysom22]() for data-centric project of the [Code Institute Full Stack Diploma]().

## Table of Contents
1. [UX](#ux)
    * 1.1 Goals
    * 1.2 User Stories
    * 1.3 Design Choices
    * 1.4 Wireframes
2. [Features](#features)
    * 2.1 Existing features
    * 2.2 Changes made during implementation
    * 2.3 Features left to implement
3. [Information architecture](#information-architecture)
    * 3.1 Database Choice
    * 3.2 Collection Schemas
4. [Testing](testing)
    * 4.1 Link to TESTING.md file
5. [Technologies Used](#technologies-used)
6. [Deployment](#deployment)
    * 6.1 Deployment to PaaS
    * 6.2 How to run this project locally
7. [Credits](#credits)
    * 7.1 Content
    * 7.2 Code
    * 7.3 Acknowledgements
8. [Evaluation](#evaluation) 
    * 8.1 What I have learned
    * 8.2 Questions I have
    * 8.3 What I would do differently

## 1. UX
<hr>

### Goals
Target audiences and possible user goals:

* Teachers and educators: 
    * To find educational quiz content that my students will enjoy
    * To share my own quiz content with others for the benefit of many
    * To find subject/topic/age group specific quiz content to use for lessons and homeworks
    * To use quiz content evaluate my students' understanding
    * To find content that I can use to help create effective teaching resources
* Students and learners:
    * To find engaging quiz content to have fun and challenge myself
    * To find subject/topic/age group specific quiz content to help me learn
    * To have fun competing against my peers
* Anyone who uses quiz content for personal use or for organizing an event:
    * To share my own quiz content with others for the benefit of many
    * To find general knoweledge quiz content for my own interest or for an event
    * To search by topic/subject for specific quiz content for my own interest or for an event
    
Quizzical is a great way to meet these user needs because:

* The interface allows users to easily search quiz content by subject and topic and select from a specific subset of content
* The quiz content stored can be easily updated and reused over time
* Quiz content can be easily copied and printed or shared for use in lessons
* As a professional educator, I understand the needs of teachers and students well 
* The design of the site interface is intuitive, easy and pleasing to use
* The site provides a community where expertise, knowledge and experience can be shared via high quality quiz content

Site owner's goals:

* Provide an easy to use, useful site that helps educators teach better and students enjoy learning and progress
* To practice building a full stack application using front end languages plus Python, Flask and MongoDB
* To collate searchable quiz content from users that I can use in my own teaching practice and design of resources
* To provide a virtual community where ideas can be shared and collaboration in teaching and learning is fostered
* To provide an educational means of fun!
* To create a scalable platform tha can be expanded in scope to include many more categories of topic and features such as ability to play quizzes interactively.

### User Stories

As a user of the site:
1. I want information on the landing page to be easy to digest, so that I can find what I need quickly and efficiently
2. I want to quickly find where to search for content, so that I can find the specific content I need
3. I want search results to be presented to me clearly and succinctly, so that I have a useful overview of the content available
4. I want to be able to click on a search result to view the content in more detail, so that I can decide to use it more not
5. I want to be able to view a varied selection of content in a single clear view, so that I can get an idea of the content the site offers and what might be relevant for me
6. I want quiz content to be categorized by subject/topic, so that I can find content that I need by navigating the site
7. I want the navigation buttons and links to be intuitively located and designed, so that I can traverse the site easily and efficiently
8. I want to easily find where I can create by own quiz content and for the inputs to be intuitive and appropriate, so that I can share my own content effectively on the site
9. I want the site to be responsive, so that it is easy to read and navigate on all of my devices
10. I want feedback from the site when I interact with it, so that I am aware of the effects of my interactions at all times and can use the site confidently and efficiently
11. I want to be able to create an account and save my favorite content, so that I can easily find reuse quizzes
12. I want to easily search by topic/subject/age group, so that I can find specific and relevant content.

As a new user of the site:
1. I want to information on the landing page to clearly and succinctly communicate the purpose of the site and how to use it, so I can begin accessing quiz content quickly
2. I want the information on the landing page to guide me clearly on how to register for an account and for this process to be intuitive, so I can begin accessing quiz content quickly

As a regular user of the site:
1. I want to be able to connect with the site owner, to suggest new features or ask for assistance
2. I want to be go to the login page easily from the landing page, so that I can access my account and the cotent specific to me quickly and easily

### Design Choices

#### Overview

The overall tone of the site is a balance of fun and friendly with educational depth and credibility. The design aims to appeal to both school age students using the site content directly, as well to other adult users accessing and sharing content.
The colors, styling, and icons were chosen to present a familiar and intuitive user interface whilst maintaining sufficient contrast between elements and areas of the page.
A consistent overall layout and feel across the site was a priority when designing the layout of pages and choice of icons and components.
A mobile first design approach was used to optimize the user experience for small devices first before adjusting layout and size of elements for larger screen sizes.

Inspiration for design and layout was taken from some existing (much more sophisticated) online quiz sites:
* [Quizziz]()
* [Kahoot]()

This project aims to create a basic implementation of quiz sharing functionality which is scalable into an application with it's own unique features and content in future versions.
Quizziz and Kahoot both include functionality for users to login and play head to head on a quiz interactively in real time: this functionality is beyond the scope of this project and the developer's current skill level and time available therefore the scope is limited to sharing static quiz content. 

#### Fonts 

* Fonts were chosen to help communicate the overall theme and feel of the site. Sans-serif, readable fonts were chosen for both the main title and main body fonts so they complement each other well.
* `Raleway` was used as a main title font. It is sans-serif, rounded and extremely clear, so is a good choice to engage student users. It is not frivilous or unserious to put off older users. The site is not intended to be used primarly for serious academic material and therefore clarity, accessibility and a bit of lightheartedness were reasons to choose this font. Some preliminary research into the aesthetic design of edTech applications suggested that this font is a popular choice in the industry due to it's readability and spacious feel. 
* `Open Sans` was selected as the main body font. It complements the main title font very well with rounded glyphs and ample spacing. It scales very well to small sizes so is appropriate for more granular elements on smaller device sizes. 
* `Oswald` was chosen as a third font for it's clear contrast both with the main title and main body fonts. It is much more clsely spaces and has taller, narrower glyphs. It is also a popular choice for education websites according to research.

#### Colors

[Link to color palette](https://coolors.co/000000-386b4d-0839d9-fadcb2-e0e0e0-ffffff)

The color palette was chosen using the [Coolors](https://coolors.co/) color picker.

* The overall theme of the pallete is a mixture of earthy colors and tactile office stationary colors.
* The palette contains some vibrance and color to engage younger users. 
* There are three lighter and three darker tones: one of each group is a more vibrant and garish and is used on the site to help bring contrast to certain elements - in particular, calls to action.
* There are not too many constrasting colors in the pallete overall to overwhelm the user and each group of three lighter and darker colors blend well together respectively
* White is used as a primary font color on darker blue or green background to provide maximum contrast and also as a background color paired with black or 'persian blue' text for a clean, high contrast effect when there is alot of content or smaller text.
* Main solid backgrounds for elements use the vibrant 'persian blue' and 'wheat' colors to visually separate elements and convey structure to help user easily navigate the page.
* 'Amazon green' and 'gainsboro gray' are used as secondary accent and styling colors for elements (horizontal rule elements, borders, minor text, secondary icons and buttons). These help add depth to the page but are not essential to the site experience so that users who need very high contast can still use the page effectively.

#### Icons

- Icons are used from [Font Awesome]()
- Icons are used across the site to help users navigate the site more easily to find and interact with the data they need.
- Icons are used to provide context concisely and universally to users to help them navigate the site with greater ease and confidence - aids a first time learning curve.
- Icons help to provide a familiar user experience so new users and younger users can understand how to use and navigate the site more easily. 
- Icons reduce the need for textual information and labels and facilitate a cleaner and less cluttered user interface - particularly on smaller devices.
- Icons are used to help orientate the user and communicate the purpose of a particular feature or page on the site - particularly important for non-English speaking users.
- Icons are also used as links (or in combination with a textual link) to help all users understand the site and particularly non-English speaking users. 
- Icons are always accompanied by appropriate aria-labels and attributes to meet accessibility guidelines for users with screen readers.

#### Styling and effects for components

- Horizontal rules are used to divide sections of page wherethere are multiple call to action sections and/or areas that are not as clearly delineated by color or layout of elements
- Buttons of various sizes and styles are used to distinguish priority calls to action from secondary interactions. Create and Login buttons are largest and most prominent as goal of site (which also benefits users) is to increase the number of quizzes in database and increase number of site users. 
- Hover and active psuedoclass effects are used to improve user experience through feedback across site. Buttons have interaction effects to provide reliable, useful and expected feedback to users.
- Carousels with images
- Cards to display groups of information (discrete quiz / question)
- Collapsible footer
- Collapsible navbar from Bootstrap & Material Design
- Progression indicators
- Box shadows and text shadows are used to add depth and definition to certain content and areas of the page.
- 

#### Images

- Main landing page image
- Images for main features carousel
- Smaller secondary images for help section 
- Images for each quiz category to be displayed in discover carousels, search results and view quiz pages

#### Wireframes

Wireframes for this project were created using [Balsamiq] (https://balsamiq.com/):

- [View all wireframes]()

## 2. Features
<hr>

- Note that the features included in this project for submission to Code Institute represent a 'Minimum Viable Project' (MVP) version. It was important not to allow the scope to become too large given the time constraints and the requirements and criteria of the course assessment. There are a large umber of features - big and small - that were left out in the scope phase of the project but which may well be added at a later date.

### Existing features

- Navbar
    - Logged out links: Sign Up, Login and How To
    - Logged in links: Discover, Create, Profile, Help and Logout
    - Quizzical icon at left
    - Links are collapsable on small screens into burger icon
    - Fixed position so always visible

- Footer
    - Single column layout on small screen
    - Link to top of page
    - Copyright information
    - About button: hides/unhides content below
    - About section (visible by default on landing page hidden by default on all other pages). Includes brief info about the project and the site owner/developer. Includes links to developer portfolio, LinkedIn and GitHub.
    - Inverse color contrast with background of elements above.

- Landing page
    - Visible to all users
    - Main title, tagline and Sign Up/ Log In links. Sign Up button is call to action for new users and is larger and more prominent.
    - Photo of engaged learners
    - List of benefits of using site
    - Carousel of 3 images related to main features of site each with explanatory caption text. Users can click arrow icons to scroll manually through images in carousel. Ellipsis icon shows current image displayed in list of images.
    - 'Easy to get started' section. 3 numbered steps, each has concise textual instruction and small associated image to inform user of most basic process to follow to start using the application.
    - Final call to action section: 'Ready to get Quizzical' prompt and large, prominent button to sign up page.

- Discover page
    - Visible to logged in users only
    - Main title with compass icon helps orientate user and provide context for page
    - Primary search bar CTA with text input and placeholder text 'find a quiz' on intial page load. Magnify icon acts as submit button for search input
    - Recommended section. Includes quizzes belonging to main category of interest and age range specified in current user settings. Arrow icon links to view search results page with all recommended quizzes. Carousel of three quizzes from recommended list is displayed on a card element. Each item in carousel shows quiz image and caption with title of quiz. Carousel cycles through each quiz automatically and arrows left and right allow user to cycle manually. Ellipsis icon is shown to specifiy position of currently viewed quiz.
    - Category sections have similar layout and functionality to recommended section. A carousel is shown for main categories and age ranges.
    - Secondary search bar CTA at end of main page content. Subtitle - "Can't find what you're looking for?". Another search bar, same as above so user can serach without scrolling up to top of page again. Create button linking to create quiz page and smaller link to 'see all quizzes' which links to view search results page. 

- Search results page
    - Visible to logged in users only
    - Search bar input and magnify icon submit (as as element on discover page).
    - Number of results displayed just above quiz results in small, subtle font (as it is secondary information)
    - Each quiz found in database that matches search criteria (from search box or via selecting from discover page) is displayed inside discrete card elementseparated by margin in a list. Each card displays the quiz title, quiz image, number of questions, category and age range information relating to that quiz.  Each card has a 'view' CTA button with an icon and text which links to a page displaying the specific quiz.
    - At bottom of main page content there is a section with subtitle: "Can't find what you're looking for?" and a CTA 'Create' button with icon which links to the create quiz page. There is a smller link 'see all quizzes' which links to view search results page. 

- View quiz page
    - Visible to logged in users only
    - Card element displays main, summary information about the selected quiz: quiz title, image, category, age range and author. If a user is the creator of a quiz they can edit and delete that quiz when logged in by clicking on edit and and delete icons that are displayed instead of the author information in this element and link to respective pages.
    - Admin users can edit and delete all quizzes on database when logged in - the edit and delete options that are displayed to a quiz owner for their own quizzes are displayed for all quizzes to admin.
    - Number of questions for quiz displayed just above quiz results in small, subtle font (as it is secondary information)
    - Each question in quiz is displayed in own card element in a list below the main, summary information card. Each card displays the number of the question in the quiz, text containing the quiz question, a small answer choices label followed by four answer options in a list each consisting of text and an empty checkbox icon. On initial page load all checkboxes have same default background color. At bottom of card for each question is a small text button 'show/hide answer' which uses JavaScript to toggle between one checkbox green and the rest red and all the same default color. The text in the link reads 'show' or 'hide' answer depending on current state.

- Edit quiz page
    - Visible to logged in users only
    - Title and edit icon at top of page to give context to user
    - 'Finish editing' button submits form data to db (in update operation) and redirects user to view quiz page for same quiz. Feedback is given if form fields are not validated. Adjacent to 'Finish editing' button is a smaller link to discard changes made and return to view quiz page for current quiz.
    - Input fields for quiz information. Quiz name is a text input, Category and Age Range fields are dropdown menu inputs with the selection options read from respective collections in db. Each input has a corresponding label.
    - Add question is large call to action icon. When clicked the focus moves to a newly created question card at end of current question card list.
    - Question list: each question is displayed as part of a list within it's own card component. 
    - Each question card contains: 'edit question {number}' text, a delete icon (triggers a defensive confrimation message, if confirmed the current card is removed from the display), a textarea input for question text (prefilled with current value on db on page load), 'edit answer choices' text label, four text input boxes each (prefilled with current value in db on page load) each with adjacent radio icon (one of which can be selected at a time to signify the correct answer to each question - selected answer is solid and green wheras others are grey and faded)
    - Duplicate of 'add question' button above. Adjacent and smaller 'delete quiz' button (triggers defensive confirmatory message) which when clicked and confirmed will remove current quiz from db and redirect user to profile page.
    - Duplicate of finish editing button and discard changes link displayed at bottom of main content of page.

- Create quiz page
    - Visible to logged in users only
    - Title and build icon at top of page to give context to user
    - 'Publish' button submits form data to db (in create operation) and redirects user to view quiz page for created quiz if form is validated. Feedback is given if form fields are not validated. Adjacent to 'Publish' button is a smaller link to discard changes made and return to view quiz page for current quiz.
    - Same input fields displayed as 'edit quiz' page but without prefilled values.
    - Same large 'add question' call to action button appears directly below main quiz information form on page load. This button has same function to add a new empty card component for a question to the display. The 'add question' button always displays below the last question in the list.
    - Duplicate of 'publish' and 'discard' links displayed at bottom of main page content. 

- Profile page
    - Visible to logged in users only
    - Username of logged in user displayed next to user icon
    - 'Create' button displayed which links to create quiz page
    - Link icon to edit profile of current user page displayed to right of username. 
    - Subtitle of My Quizzes displayed next to button which links to create quiz page.
    - Small '{number} of results' label displayed.
    - List of quizzes authored by current user displayed. Each quiz summary is displayed within a card component containing: quiz title, quiz image, number of questions in quiz, category of quiz, age range of quiz, icon link to view current quiz page and icon link to edit current quiz page.
    - A subtitle is displayed "Help grow our quizzical community!" and a larger duplicate of 'create' button.
    - At bottom of main page contnet is a logout button (icon and label) if clicked user is logged out and redirected to login page.

- Register account/edit profile page
    - If user logged out: Main title: "Let's get quizzical!" and subtitle of create account with add user icon. 
    - If user logged in: Main title: current user username and user icon is displayed and subtitle of change setting with settings icon.
    - Form with inputs: username (text), main category of interest (dropdown), main age range (dropdown) and password text displayed with labels. If user is logged in the fields are prefilled on page load with values for user from db.
    - If user logged out: Create account button to submit form and send to db (create operation). Form validates input to meet regex criteria and user is given feedback if a value in a field is invalid - user redirected to discover page. Smaller link to login page with 'already registered' label. 
    - If user logged in: Save changes button to submit form and send to db (update operation), user redirected to profile page. Smaller link to discard changes and user redirected to profile page. Beneath is a 'delete profile' button (icon and label) which when clicked displays a confirmatory message before deleting user and all associated quiz data from db and redirecting to landing page.

- Login page
    - Reachable via navigation to logged out users only (if logged in user tries to access corresponding route manually in URL bar they are redirected to profile page)
    - Title 'Login' and login icon to orientate and communicate context of page to user
    - Username and password input fields (with form validation for length and regex) with labels
    - Login button submits form (after validation) and redirects user to discover page. Smaller link 'create account' with 'new here' label redirects to registration page (displayed for logged out user)

### Features left to implement

Not implemented due to a balanced consideration of time constraints, developer skill and experience linitations and due to specific assessment guidelines of Code Institute course which this project was created for.

- Further admin user functionality: create/edit categories and age ranges. Page on site that only admin users can access. 
- Contact page with form hooked up to emailJS where users can ask questions, make comments, offer suggestions.
- Option to play each quiz interactively within the application. Button to play quiz added to search results and view quiz card element for each quiz. Play quiz is separate page where user selects an answer to each question before scrolling to next question in quiz. 
    - Quiz owner can set an optional time limit for users playing quiz interactively from the edit quiz page
    - User is given a high score based on percentages of answers correct and time taken for a quiz
    - Option to input high score manually if quiz is played offline
    - Each quiz has a high score leaderboard of top 10 scores displayed on view quiz page
- Users can upload a custom image for each quiz to be displayed in search results, discover and view quiz pages
- Users can add a custom number of answers to a question (2 or more) instead of a fixed number of four.
- Users can upload an image in addition to, or instead of, question text for each question in edit quiz page
- Button on view quix page to download or print quiz as a pdf file - users can then use quiz content more easily when no access to tecnology/internet
- Favorites (star) button on each quiz card on search results, discover and view quiz pages. Toggle on/off (checkbox) icon. 
    - Add/remove quiz from favorites section for current user which is displayed on user profile page
    - Discover page also includes a 'most favorited' section which displays quizzes which appear most times in favorited list for all users.
- Custom 404 error page. Consistent with overall site theme and styling. Allows user to redirect back to site easily.
- Rate up / down button on each quiz card on search results, discover and view quiz pages. 
    - A quiz can be labbled as 'like' or 'dislike' by current user. 
    - Each section organized by catergory/age range on discover page displays quizzes prioritized by net likes - dislikes score for all users.
- Carousel of similar quizzes at bottom of view quiz page (same category or age range) to help users find content they want
- Sort quizzes dropdown links at top of search results and user profile quiz lists. Sort alphabetically, most/least recently updated (db also stores date quizzes were created and last updated)
- Extra field to repeat password input on create/edit account page which must match first password input field exactly
- Forgotten password link on login page. User enters email address associated with account (user input and db stores an email address when account is created) and email JS sends a temporary password and db is updated. User is directed to page to enter and confirm a new password when they first login to account with temporary password.
- User can select account type on login page (and change this setting on edit account page) from teacher, student, other. Teacher accounts can create and edit quizzes and add scores manually, Students can play quizzes and register high scores interactively. Other users can do both teacher and student functions. 
- User can select mutiple categories and age ranges (primary and secondary) on login page (and change these settings on edit account page). Users are recommended quizzes from mutiple categories and age ranges on discover page.
- Terms and conditions checkbox on create account page which must be selected for form to submit. Terms and conditions can be viewed on separate page (in new window) or modal.
- Each quiz create and edit page has an optional secondary catergory and secondary age range selectable from dropdown menu
- Questions are stored in separate collection in db and referenced from each quiz. All questions added by all users can be searched from create/edit quiz page and added to the cuurent quiz.
- Questions and answers can be reordered on edit/create quiz page by dragging cards containing them (leveraging draggable.js library)
- Username of currently logged in user is displayed in Navbar element
- Navbar scrolls with page until 80% hidden then botton 20% remains visible only: until user scrolls up and 100%of navbar height slides back into view
- If a list of quizzes or questions displayed on any page is over 10, the list is paginated to display quizzes/questions in blocks of 10.
- Each quiz has a 'short description' and 'full description' field stored in db. The short description is generated programatically from full description by slicing the string. The short description is displayed on view quiz page with a link to view long description as tooptip/dropdown element.
- Each quiz has a last last updated field in db and discover page displays 'new content' carousel of quizzes with most recent values for this field.
- Edit quiz, edit profile an view quiz pages have a 'back' arrow element to easily naviagte back to previous page (without previous page reloading as default when using browser navigation)
- Login fields and button appears in navbar instead of separate page to limit navigation between separate pages on site.
- A 'flag question' link displayed on every question catd. sends an email to quiz owner and to admin that a question needs correcting or updating. When clickeda new page is opened up to input details and send email.

## 3. Information Architecture
<hr>

### Database choice

[MongoDB]() is a NoSQL, document-based database which groups data as key-value pairs within documents grouped into collections. MongoDB excels at storing and providing access to unstructured data at scale. 
The data schema for this project would be better suited to an SQL relational database due to the relationships between entities in different collections, however MongoDB was used because this is project is primarily a learning exercise and this was the specification for this project (a SQL database will be used in a future project) 

### Database collections structure

#### Users collection

Collection name: users

| Title | Key in DB | Form validation | Data Type | Details |
| --- | --- | --- | --- | --- |
| User ID | _id | None | ObjectId | Primary Key |
| Username | username | text, `maxlength=20` | string | not null, unique |
| Password | password | text, `maxlength=20` | string | not null |
| User category | user_category | None | ObjectId |   |
| User age range | user_age_range | None | ObjectId |   |

#### Quizzes collection

Collection name: quizzes

| Title | Key in DB | Form validation | Data Type | Details |
| --- | --- | --- | --- | --- |
| Quiz ID | _id | None | ObjectId | Primary Key |
| Quiz Title | title | text, `maxlength=20` | string | not null |
| Owner ID | owner_id | None | ObjectId | ref: > users._id  |
| Category ID | category_id | None | ObjectId | ref: > categories._id |
| Age Range ID | age_range_id | None | ObjectId | ref: >age_ranges._id |
|   |   |   |   |   |
| **Questions** | questions |   | **object** |   |
| Question Text | question_text | text, `maxlength=150` | string | not null |
| **Answers** | answers |   | **object** |  Embedded in questions object |
| Answer Text | answer_text | text, `maxlength=100` | string | not null, unique |
| Correct Boolean | correct_bool | radio | Boolean | not null |

#### Categories collection

Collection name: categories

| Title | Key in DB | Form validation | Data Type | Details |
| --- | --- | --- | --- | --- |
| Category ID | _id | None | ObjectId | Primary Key |
| Category Name | category_name | Dropdown menu | string | not null, unique |


#### Age ranges collection

Collection name: age_ranges

| Title | Key in DB | Form validation | Data Type | Details |
| --- | --- | --- | --- | --- |
| Age Range ID | _id | None | ObjectId | Primary Key |
| Age Range | age_range | Dropdown menu | string | not null, unique |

* ObjectIds for documents in `categories` and `age_ranges` collections are stored as field values in both `users` and `quizzes` collections - serves to define a relationship between documents in these different collections.
* ObjectIds for documents in `users` collection are stored as field values in `quizzes` collection - serves to define a relationship between documents in these different collections.

## 4. Testing
<hr>

## 5. Technologies Used
<hr>

* [Python3]() language and standard libraries
* [Flask]() web application framework used to simplify building appeal
* [Jinja]() template engine (Flask dependency)
* [Werkzeug]() WSGI toolkit (Flask dependency)
* [pip]() used to install dependencies for project
* [Balsamiq]() for wireframing
* [Gitpod]() as IDE
* [Git]() command line utility and GitHub for version control
* [Trello]() for planning and organizing project workflow and tasks. [Link to Trello board for project](https://trello.com/b/mleZppxL/quizzical-ms3)
* [MongoDB]() NoSQL document-based database 
* [Font Awesome for icons]()
* CDN for content delivery
* [Coolors]() to select color palette for website
* [Bootstrap & Material Design](https://mdbootstrap.com/)


## 6. Deployment
<hr>

## 7. Credits
<hr>



### Content

### Code

* Code Institute 'gitpod-full-template' repository
* Code Institute Task Manager walkthrough project

### Acknowledgements

* [Kahoot](https://kahoot.com/) inspiration for design of layout, icons, colors and styling.
* [Quizizz](https://quizizz.com/) inspiration for design of layout, icons, colors and styling.


## 8. Evaluation
<hr>

* [StackOverflow thread](https://stackoverflow.com/questions/12403240/storing-null-vs-not-storing-the-key-at-all-in-mongodb#:~:text=Query%20on%20key%3A%20null%20will,field%20key%20doesn't%20exist.&text=If%20you%20need%20to%20keep,field%20as%20null%20or%20empty.) guided decision to use null values for empty fields in mongodb rather than leaving fields out




