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

#### Colors

#### Icons

- Icons are used across the site to help users navigate the site more easily to find and interact with the data they need. 
- Icons help to provide a familiar user experience so new users and younger users can understand how to use and navigate the site more easily. 
- Icons reduce the need for textual information and labels and facilitate a cleaner and less cluttered user interface - particularly on smaller devices.
- Icons are used to help orientate the user and communicate the purpose of a particular feature or page on the site. 
- Icons are also used as links (or in combination with a textual link) to help all users understand the site and particularly non-English speaking users. 

#### Styling 

- Horizontal rules are used to divide sections of page wherethere are multiple call to action sections and/or areas that are not as clearly delineated by color or layout of elements
- Buttons of various sizes and styles are used from [MaterializeCSS](https://materializecss.com/) to distinguish priority calls to action from secondary interactions. Icons are used with buttons to convey clear meaning to all users. Buttons have inbuilt interaction effects to provide reliable, useful and expected feedback to users.
- Carousels with images
- Cards to display groups of information (discrete quiz / question)
- Collapsible footer
- Navbar
- Progression indicators

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
    - Main title, tagline and Sign Up/ Log In links. Sign Up button is call to action for new users and is larger and more prominent.
    - Photo of engaged learners
    - List of benefits of using site
    - Carousel of 3 images related to main features of site each with explanatory caption text. Users can click arrow icons to scroll manually through images in carousel. Ellipsis icon shows current image displayed in list of images.
    - 'Easy to get started' (help) section. 3 numbered steps, each has concise textual instruction and small associated image to inform user of most basic process to follow to start using the application.
    - Final call to action section: 'Ready to get Quizzical' prompt and large, prominent button to sign up page.

- Discover page

- Search results page

- View quiz page
    - Admin users can edit and delete all quizzes on database when logged in
    - If a user is the creator of a quiz they can edit and delete that quiz when logged in 

- Edit quiz page

- Create quiz page

- Profile page

- Register account/edit profile page

- Login page

### Features left to implement

## 3. Information Architecture
<hr>

### Database choice

### Database collections structure

#### Users collection

- User_id (ObjectId)
- Username (String)
- Main_category (ObjectId)
- Main_age_range (ObjectId)
- Password (String)

#### Quizzes collection

- Quiz_id (ObjectId)
- Owner_id (ObjectId)
- Category_id (ObjectId)
- AgeRange_id (ObjectId)
- Quiz_title (String)
- Questions (Array)
    - Question_text (String)
    - Answers (Array)
        - Answer_text (String)
        - Correct (Boolean)
 
#### Categories collection

- Category_id (ObjectId)
- Category_name (String)

#### Age ranges collection

- Age_range_id (ObjectId)
- Age_range (String)

## 4. Testing
<hr>

## 5. Technologies Used
<hr>

* Balsamiq for wireframing
* Gitpod as IDE
* Git and GitHub for version control

## 6. Deployment
<hr>

## 7. Credits
<hr>

* Code institute 'gitpod-full-template' repository

### Content

### Code

### Acknowledgements

* [Kahoot](https://kahoot.com/) inspiration for design of layout, icons, colors and styling.
* [Quizizz](https://quizizz.com/) inspiration for design of layout, icons, colors and styling.





