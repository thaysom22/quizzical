# Quizzical - Testing

* [README.md file](./README.md)
* [Quizzical](https://quizzical-quiz-app.herokuapp.com/) deployed on Heroku

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

# Automated Testing

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

# User Stories Testing

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

# Manual Testing

Testing of all pages and functionality was performed in a Google Chrome web browser using the dev tools device toolbar to emulate mobile and tablet screen sizes (iPhone 6/7/8 and iPad).

The following was confirmed for each page/component/functionality:

### Components on all pages

1. Navbar

    * Quizzical Owl icon and heading are visible on left of navbar and padded from edge of display on all device sizes.
    * Clicking on icon or heading redirects user to welcome page (if logged out) and to discover page (if logged in)
    * Sign Up, Login and Welcome links are displayed on right of navbar when user is logged out and Create, Discover and Logout are displayed when user is logged in.
    * Links collapse on mobile display and a hamburger icon is displayed. Clicking on hamburger icon toggles a dropdown nav menu where links are displayed.
    * Sign up, Login and Welcome links redirect to correct pages when logged out.
    * Create, Discover and Logout links redirect to correct pages when logged in.
    * Hover effect on buttons is displayed.

2. Footer

    * Layout of sections is vertical and uncramped on mobile display. Text is readable.
    * Layout of sections is horizontal on tablet and desktop displays. 
    * Link to portfolio opens my developer portfolio website in a separate tab.
    * LinkedIn and Github links open my profiles on respective sites in a separate tab.

### Welcome page

1. Main header with sign up and login call to action

    * Sign up and login buttons are arranged horizontally on tablet and desktop displays and vertically on mobile displays
    * Sign up and login links redirect correctly to appropriate pages. Hover effect on buttons is displayed.
    * Text and icon is readable, uncramped and sized proportionally on each device size

2. Hero image

    * Image content scales and is visible on all device sizes
    * Caption is readable on all device sizes and whitespace breaks when text does not fit on a single line

3. List of benefits section

    * Three individual benefit elements are arranged horizontally on tablet and desktop sizes and vertically on phone.
    * Icons and text are aligned on all device sizes.

4. Main features carousel section

    * 3 images and captions display clearly on all device sizes
    * The text underneath caption heading is hidden on mobile devices so image not obscured
    * The carousel scrolls through images and captions automatically with a constant time interval
    * The next and previous buttons trigger the next or previous image and caption respectively to display
    * The carousel progress indicators update when image changes

5. Easy to get started section

    * Steps are arranged vertically on mobile and tablet device sizes and horizontally on desktop. 
    * Icons have sufficient padding and text is center aligned on all device sizes

6. Final sign up call to action section

    * Link to sign up redirects to correct page. Hover effect on button is displayed.

### Login page

1. Form layout

    * Scales with viewport width and remains at fixed max width of desktop display
    * Input outline widths remain fixed % of container


2. Username input

    * Label username is displayed inside of form outline when not in focus
    * When clicked or tapped cursor appears and label move to top edge of outline box
    * If an no username is submitted outline turns red and extends down vertically, an error message is displayed below input text and a warning icon slides into view at right of outline box.
    * If username is entered, the outline shrinks back to original size and becomes green , error message hides and warning icon is replaced by a tick and remains this way when no longer in focus.
    * If input deleted again then styling reverts to red, with error message and warning icon and remains this way when no longer in focus.
    * If input entered originally and sumbitted outline turns green and tick icon slides across to right of outline box.

3. Password input

    * As above for username input

4. Form submission

    * Submit button does not redirect to a new page when form not validated
    * Provides hover user feedback effect
    * If an unrecognized username (not in db) is entered, form validates and login page refreshed with a dismissable banner (incorrect username / password)
    * If a recognized username is entered without the correct password pairing (not empty), form validates and login page refreshed with a dismissable banner (incorrect username / password)
    * If all form inputs are valid, username is found and correct matching password is entered submit button redirects to Discover page with dismissable banner message ("welcome back, <username>")

5. Sign up button

    * Redirects to sign up (register page)
    * Provides hover user feedback effect

### Sign Up (Register) page

1. Form layout

    * Inputs are arranged vertically on mobile display and 2 columns of 2 on tablet and desktop.
    * Width of input outline boxes remains not too long/small

2. Username and password inputs

    * As above for username input on Login page. 
    * Invalid feedback as above if a left blank, or value less than 5 or greater than 20 (30 for password) or does not satify regex pattern is submitted

3. Main category / main age range select elements

    * Display red outline and warning icon if not selected when form submitted.
    * Green outline and tick icon when selected
    * Displys label inside form outline box prior to selection.

4. Form submission

    * Submit button does not redirect to a new page when form not validated
    * Provides hover user feedback effect
    * If a pre-existing username is entered in username input and all fields are valid form submits and redirects to same page with a dismissable banner ("The username <username> already exists")
    * If all form inputs are valid and username not already in db submit redirects to Discover page with dismissable banner message ("welcome to Quizzical, <username>")

5. Login button

    * Redirects to login page
    * Provides hover user feedback effect

### Discover page

1. searchbar

    * Displays as full width element on mobile size and as a centered container with rounded border on tablet and desktop
    * Orange search button (form submit) displays to right of searchbar input outline and exhibits hover feedback effect
    * Searchbar input displays "Find a quiz by title" label when page is loaded which move to top of input outline box when in focus and cursor appears.
    * If search is submitted with empty search query invalid feedback (as described above) is displayed with message: "Invalid Search"
    * If any value is entered into searchbar input valid feedback is displayed (as above) when form submits and user is redirected to search page where searchbar element displays text: "showing results for: <search_query>" and the number of results if any quizzes found by search. 
    * Input does not allow a search query to be entered of more than 30 characters.

2. Recommended section

    * Each quiz is displayed in a card element with an image (dependent on category of quiz), title and age range, category and quiz owner username information.
    * Quiz card images exhibit a hover zoom feedback effect. Hovering anywhere on the quiz card caused a pointer cursor to be displayed and if clicked user is directed to view quiz page for selected quiz.
    * Quizzes all in category matching user main category or user main age range selected at sign up. 
    * A more link is displayed at top right of section on mobile and middle right on tablet and desktop. Clicking redirects to search page and displays as search result cards all quizzes in db that are matching the current user's category or age range preference
    * Displays a carousel of 3 quizzes on mobile view. Cycles through quizzes in a constant time interval and next and previous buttons can be used to view next/previous quiz manually.
    * Displays 2 quiz cards arranged horizontally (not carousel) on tablet view
    * Displays 3 quiz cards arranged horizontally (not carousel) on desktop view

3. Categories and age range sections

    * Display as above (recommended section) for each category in db categories collection and each age range in age_ranges collection
    * Clicking view more link redirects to search page and displays as search result cards all quizzes in db that are matching the category or age range of the section of the view more link that was clicked

4. Create Quiz call to action section

    * Create quiz button displays hover feedback effect and when clicked redirects to create quiz page.
    * All Quizzes button displays hover feedback effect and when clicked redirects to search page displaying all quizzes in db quizzzes collection as search results

### Search page

1. searchbar

    * As above for searchbar on Discover page
    * Displays a "showing results for: <search_query>" message below input box with previously entered search query text
    * If quiz results are displayed below the searchbar element contains a "<num_of_quizzes> quizzes found" message

2. quiz results section

    * If no quiz results are found: displays no quizzes found section with "Discover" button (exhibits hover feedback effect and if clicked redirects to Discover page)
    * If quiz results are found (via search query entered or via clicking view more link on Discover page) 
    * Each search result displays as a card with quiz title, image (dependent on category) and quiz owner username, quiz category and quiz age range information. On tablet and desktop sizes the number of questions in the quiz is also displayed.
    * Image in search result card is full height on desktop. 

3. Create Quiz call to action section

    * As above on Discover page

### Create Quiz page 

1. Form layout

    * Input outlines are arranged vertically on mobile and tablet views and horizontally on desktop view. 
    * All input boxes remain sufficiently wide with ample padding on all screen sizes.

2. Quiz title input

    * Validation feedback as described for login/sign up forms.  
    * Invalid feedback shown if form is submitted when empty

3. Choose category/ choose age range select elements

    * As described above for sign up page

4. Form submit button

    * Will not submit request all form inputs are not validated
    * Displays hover interaction feedback
    * If form validated: redirects to add question page and dismissable banner message "<quiz_title> has been created" is displayed
    * Adds new quiz document to quizzes collection in db

5. Discover button

    * Displays hover interaction feedback
    * Redirects to Discover page when clicked

### Add Question (requested whilst creating a quiz) page

1. Form layout

    * Answer input boxes arranged vertically on mobile and tablet views and two by two on desktop view.
    * Correct answer radio buttons are adjacent to respective answer text input
    * Done and delete quiz buttons are arranged vertically on mobile and horizontally on tablet and desktop

2. Question text textarea

    * Box contains label "Question text" when page is loaded which moves to top of form outline when in focus. 
    * Error validation as described for text inpputs in previous sections except outline does not extend downward.
    * Provides invalid feedback and form will not submit if left empty

3. Answer option inputs

    * Validation feedback as described previously
    * All four answers must  be not empty for form to submit

4. Correct answer radio input 

    * Form will not submit unless at least one is selected
    * If none selected all four turn red to give invalid feedback
    * Once one is selected all four turn green and a green ring appears around selected button

5. Adding question info message

    * Reads "you are adding the first question to <quiz_title> when viewing add question page immediately after create qui page. 
    * Reads "you are adding  question number <question_num> to <quiz_title> when  adding subsequent questions

6. Save Question button (form submit)

    * Form will not submit unless all inputs are validated
    * If form submits, user is redirected to same page (add question) with empty input fields and adding question info message updated
    * Adds new question document to questions collection in db and updates quiz document with ObjectID of new question

7. Done button

    * Displayed only after at least one question is already added
    * Redirects to view quiz page for newly created quiz

8. Delete Quiz button

    * Clicking triggers browser confirmation pop up ("Are you sure you want to delete Quiz?") if cancelled nothing else occurs
    * If confirmed, removes newly created quiz and questions from quizzes and questions collections in db and redirects to create quiz page.

### View Quiz page

1. Quiz summary card

    * Displays quiz title, image, category, age range, username of owner and number of questions information.
    * If current user is the owner of thsi quiz a link to edit the quiz is displayed in the card. If not, no edit link is displayed. 
    * On mobile and tablet quiz information is arranged vertically and  on desktop it is arranged horizontally along bottom of card. 
    * IF shown, edit link is displayed under image on mobile and desktop and along bottom adjacent to quiz information on desktop. Image is full height of card on desktop.
    * IF shown, edit link redirects to edit quiz page for current quiz (passes ObjectID of current quiz to url). Edit quiz page displays same data as previous view quiz page as values of input elements on page loading.

2. View questions section

    * Each question displayed in separate card
    * For each question card: Question number displayed in top left. Question text displayed at center top of card. Answer choices arranged vertically down left hand side of card on mobile and tablet and 2 by 2 across card on desktop. Each answer option displays a ? icon when page loaded.
    * Show/hide answer button has text "show answer" on page load and when clicked, text changes to "hide answer" and causes all ? icons next to answer options to hide and be replaced by a green tick icon for correct answer and a red cross for an incorrect answer (tested with some really easy questions where I couldnt forget the correct answer I chose!). When clicked again original state of button and icon is reverted to.

3. Back button

    * If view quiz page was accessed by clicking a quiz card link on Discover page, back button redirects  to discover page
    * If view quiz page was accessed by clicking a search result card link on search page, back button redirects to search page with same results as were previously displayed.
    
### Edit Quiz page

1. Edit quiz form layout

    * Contains inut elements, buttons and image with padding and space around on all device sizes

2. Edit Quiz title input

    * When page loads contains text of quiz title of quiz from previous page
    * Invalid feedback if value deleted and form submitted (described previously) - see details in bugs not fixed section.

3. Edit Quiz category/age range select elements

    * When page loads value of these fields for quiz on previous page is selected

4. Submit edit quiz form (save changes) button

    * Will not submit  if title input is empty
    * If form inputs all valid form submits and user redirected to same page (edit quiz) with input populated by new quiz title and new category and age range values
    * Quiz document fields updated in db quizzes collection

5. Back button

    * Redirects to view quiz page for same quiz

6. Add question buttons

    * One inside top card below quiz image.
    * One at bottom of page beneath all question cards
    * Redirect user to add question page (tests described above) - add question page displays 'save question' button (same as described above) and a 'back' button which redirects back to previous edit quiz page.

7. Delete Quiz button

    * Clicking triggers browser confirmation pop up ("Are you sure you want to delete Quiz?") if cancelled nothing else occurs
    * If confirmed, removes newly created quiz and questions from quizzes and questions collections in db and redirects to Discover page with "Quiz and all questions" dismissible banner message displayed

8. View questions (with edit and delete links)

    * As described above for view quiz page
    * Link to edit question - redirects to edit question page for selected question populated with current question data
    * Link to delete question -  triggers browser confirmation as described above. If confirmed, removes question from questions field array of quiz in quizzes coleection and removes question from questions collection.


### Edit Question page

1. Form layout

    * Tested as described for create question page

2. Question text textarea element

    * When page loads contains question text of question from previous page.
    * Validation as described for create question textarea element

3. Answer choices inputs

    * When page loads these are populated with answer options from previous question
    * Validation as described ofr create question answer text inputs

4. Correct answer radio button inputs

    * Radio button corresponding to correct answer for question on previous page is selected when page loads. 

5. Save changes (form submit) button

    * Form does not submit if not all inputs are validated and validation feedback is shown as described above.
    * If form submits question document in db questions collection is updated with values of inputs and user is redirected  to edit quiz page for quiz question belongs to.

6. Back button

    * Redirects user is redirected to edit quiz page for quiz question belongs to without question document being updated.

### 404 url not found page

    * When an invalid url is entered 404 page is displayed.
    * Clicking on Home button  redirects user to Discover page (if logged in) and to Welcome page (if logged out)

# Bugs Discovered

### Fixed

* HTML validator showing error: "button element must not appear as descendant of a element". 
    * Fix: changed `<button>` elements which are child of `<a>` elements into `<span>` elements.
* Quiz image on view quiz page is blurred on tablet sizes. 
    * Fix: reduced width of column containing image in grid container so image remains closer to natural dimensions.
* When 'Love to learn' image on carousel displays on welcome page the caption jumps up slighly
    * Fix: Edit images in carousel so they all have equal proportions and carousel item container remains same height for each image.
* Username and password inputs showing validation feedback as on sign up page. This makes it easier to brute force authentication on login page and leads to ambiguous interactiions.
    * Fix: `minlength`, `maxlength` and `pattern` attributes removed from username and password inputs on login page.
* Images not loading on quiz search result cards on search page after 'view more' link is clicked from a category section on discover page (working for other sections - age range and recommended)
    * Fix: added lookup stage from categories colection to mongodb pipeline when request to search endpoint is made with category url parameter passed, category_img_url can now be accessed in quiz_data document returned from db
* On view/edit quiz page the show/hide answer button is not changing text content on first click and thereafter is out of sync with the icons displayed
    * Fix: added "show" class to HTML of button element when first loaded and check for then toggled this class in click event listener instead of checking current text content.

### Not fixed

* On pages with form text inputs if form is submitted and a new request is loaded then user presses broswer 'back' button then value entered is displayed on top of the form label and neither can be read clearly.
* When the initial value in the title input is deleted on edit quiz page ans the form submit button is pressed, form does not submit but input outline does not extend as expected to around invalid error message so error message appears outside of box

# Further Testing

1. Posted link to deployed site and link to Github repo for project on 'peer review' section of Code Institute Slack channel to obtain helpful comments, suggestions and feedback from peers on the course.
2. Asked around 40 students aged 12-14 in my classes (I work as a Maths teacher) to sign up, view some quizzes and create and edit a quiz with questions whilst testing the functionality and interactions with the interface. These young people are very comfortable and familiar with interaction with software and web applications and provided some useful comments and feedback on layout, sizing, access to navigation links and interaction feedback as well as plenty of quiz content!





