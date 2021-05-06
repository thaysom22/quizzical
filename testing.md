# Quizzical - Testing
----------

[README.md file](./README.md)
[Quizzical deployed on Heroku](https://quizzical-quiz-app.herokuapp.com/)

## Contents
----------
1. [Automated Testing](#automated-testing)
    * HTML, CSS and JS validation
    * Note on Unit Testing
2. [User Stories Testing](#user-stories-testing)
3. [Manual Testing](#manual-testing)
4. [Bugs Discovered](#bugs-discovered)
    * Fixed
    * Not fixed
5. [Further Testing](#further-testing)

# 1. Automated Testing
----------

### Validation Services

* [W3C Markup Validation Service](https://validator.w3.org/) used to validate HTML by passing each url of deployed app. 
    * All urls pass HTML validator with no errors or warnings.
* [W3C Jigsaw CSS Validation Service](https://jigsaw.w3.org/css-validator/) used to validate CSS. 
* [JSHint](https://jshint.com/) was used to validate Javascript files. 
    * All files pass after adding missing semicolons and changing a `return None` statement to `return;`
* Gitpod/VSCode [Python extension tool](https://marketplace.visualstudio.com/items?itemName=ms-python.python) used to validate Python code.
    * [autopep8](https://pypi.org/project/autopep8/) automatic Python formatter was used to format Python code to meet PEP8 guidelines.

### Unit Testing

* The amount and complexity of Javascript used in this project was not sufficient to warrant implementing unit tests with Jasmine - manual testing done on Javascript functionality. 
* I would liked to have implemented unit testing for the Python functions in the codebase, however given the deadline of the project and my limited time available I decided this was not a priority for this project. I aim to familiarize and improve my skills with unit testing in Python in a future project.

# 2. User Stories Testing
----------

This section goes through and confirms each user story in the [README](./README.md).

#### As a user of the site...

1. I want information on the landing page to be easy to digest, so that I can find what I need quickly and efficiently.

    * The landing page has links to sign up and login immediately visible in the navbar and in a prominent main heading section.
    * The navbar is laid out in an expected way on all device sizes.
    * The user can click either the login or sign up links when landing page is loaded without scrolling or navigating
    * User can scroll down on landing page to find out more about the beneifts, features and how to use the app.
    * Information about the site is found in the footer asper convention.
    * There is a link to sign up at the bottom of the main page content so a new user who has read information about site can proceed without needing to scroll to top.

2. I want to quickly find where to search for content, so that I can find the specific content I need.

    * Once signed up or logged in the user is immediately redirected to the discover page. This becomes the default route for app once user is signed in.
    * The discover page has a prominent searchbar input at the top of the page with a prompt to user - user can use to search for quizzes by title.
    * The discover page displays quizzes organized by age range and category to help the user find specific content.
    * Upon signup, the user can select a favorite category and age range: the discover page has a recommended section which displays quizzes with satisfy these criteria.
    * Each section on the discover page has a link to view more quizzes of the same criteria on the search page.
    * The user can click on a quiz from the discover page to view the content of that quiz.
    * The user is informed when a section has no quizzes in database.
    * At the bottom of the discover page there is a link to create a quiz or view all quizzes if the user cannot find content in the specific sections above.
    * If the user searches using the searchbar input or clicks any 'view more' link the matching quizzes are displayed on the search page.

3. I want search results to be presented to me clearly and succinctly, so that I have a useful overview of the content available

    * On search page each quiz is clickable to view. The number of results and the search term entered are displayed to the user at top of the search page.
    * Each Quiz is displayed in a card with the title, an image of the relevant category and also: number of questions, username of owner, category and age range information.

4. I want to be able to click on a search result to view the content in more detail, so that I can decide to use it more not

    * From the discover page or the search page quizzes are displayed in card elements that are links to view each quiz individually.
    * Each card link exhibits a subtle zoom in hover effect so user is assured in an unobtrusive way that they can click to view the quiz.
    * When an individual quiz link is clicked from the Discover or Search page the user is taken to the View Quiz page: a quiz summary is displayed (similar to the card on Discover/Search page) and beneath each question is displayed in it's own card.
    * Each question displays the answer options and an interactive button to show/hide answers for each question. On click the correct answer icon turns to a green tick and the others turn to red cross icons.

5. I want to be able to view a varied selection of content in a single clear view, so that I can get an idea of the content the site offers and what might be relevant for me.

    * The discover page displays quizzes organized and displayed by age range and category to help the user find specific content. Each section displays a random sample of 2 or 3 quizzes and a link to view more.
    * Upon signup, the user can select a favorite category and age range: the discover page has a recommended section which displays quizzes with satisfy these criteria.
    * Each section on the discover page has a link to view more quizzes of the same criteria on the search page.
    
6. I want quiz content to be categorized by subject/topic, so that I can find content that I need by navigating the site

    * As above

7. I want the navigation buttons and links to be intuitively located and designed, so that I can traverse the site easily and efficiently

    * Navbar is consistent on all pages when user is logged in or logged out and displays links to use main features of site
    * Most important/commonly required links are presented as large orange buttons with consistent styling
    * When a user scrolls to bottom of a page there is a section with links to redirect back or perform next action

8. I want to easily find where I can create by own quiz content and for the inputs to be intuitive and appropriate, so that I can share my own content effectively on the site

    * Link to create quiz page is prominently displayed in navbar and at bottom of search and discover pages
    * The Create Quiz process is separated out into entering quiz meta data and adding individual question data on separate pages so the user is not overwhelmed with inputs in one go. 
    * All inputs for quiz data and adding question data are clearly labelled and provide the user with appropriate feedback effects and messages.
    * The user is gudied by the labels and the form inpu feedback to enter the required data in a valid format.

9. I want the site to be responsive, so that it is easy to read and navigate on all of my devices

    * All pages on the site are designed to be responsive with a mobile first methodology.
    * Navbar is collapsible on mobile screens and retains all links in dropdown memu
    * No elements appear too cramped on small mobile devices and the layout and elements display clearly using up available space on larger desktops.
    * All buttons and links are not crampled and are easily usable on smaller device sizes.

10. I want feedback from the site when I interact with it, so that I am aware of the effects of my interactions at all times and can use the site confidently and efficiently

    * Button links provide a subtle hover effect to inform user they are interactive
    * Card links have a zoom in effect for image when user hovers cursor
    * All form input, select and textarea elements: label moves to top when in focus and green/red outline color with tick/cross icon is displayed for valid/invalid feedback. An appropriate invalid input message is displayed to user.

11. I want to be able to create an account and save my favorite content, so that I can easily find reuse quizzes.

    * The feature to view/edit/delete a profile page was removed from the scope during implementation for reasons of limited time amd moved to 'features left to implement' section of README.
    * Quizzes created by current user display a link to edit quiz

12. I want to easily search by topic/subject/age group, so that I can find specific and relevant content.

    * The feature to search by category/age range was removed from the scope during implementation for reasons of limited time amd moved to 'features left to implement' section of README.
    * Discover page displays seclection of quizzes from database organized to category and age range.

#### As a new user of the site...

1. I want to information on the landing page to clearly and succinctly communicate the purpose of the site and how to use it, so I can begin accessing quiz content quickly

    * See 1. above

2. I want the information on the landing page to guide me clearly on how to register for an account and for this process to be intuitive, so I can begin accessing quiz content quickly

    * See 1. above

#### As a regular user of the site...

1. I want to be able to connect with the site owner, to suggest new features or ask for assistance

    * The name, portfolio website (with contact information) and professional social media external links are displayed in the footer on all pages.

2. I want to be go to the login page easily from the landing page, so that I can access my account and the cotent specific to me quickly and easily

    * Link to login is displayed in navbar and immediately in main heading section on landing page.

# 3. Manual Testing
----------

Testing was done in a google chrome browser 

# 4. Bugs Discovered
----------

### Fixed

* HTML validator showing error: "button element must not appear as descendant of a element". Fix: changed `<button>` elements which are child of `<a>` elements into `<span>` elements.
* Quiz image on view quiz page is blurred on tablet sizes. Fix: reduced width of column containing image in grid container so image remains closer to natural dimensions.

### Not fixed

* 

# 5. Further Testing
----------

1. Posted link to deployed site and link to Github repo for project on 'peer review' section of Code Institute Slack channel to obtain helpful comments, suggestions and feedback from peers on the course.
2. Asked around 40 students aged 12-14 in my classes (I work as a Maths teacher) to sign up, view some quizzes and create and edit a quiz with questions whilst testing the functionality and interactions with the interface. These young people are very comfortable and familiar with interaction with software and web applications and provided some useful comments and feedback on layout, sizing, access to navigation links and interaction feedback as well as plenty of quiz content!





