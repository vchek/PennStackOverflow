# 350S18-34-PennStackOverflow

## Technology Requirements

1. Conda 4.4.9
2. Python 3.6.3
3. Django 2.0.2
4. sqlite3 (can switch for MySQL)
5. Bootstrap for CSS styling
6. Jinja for templating
7. Nginx (as opposed to Apache, which doesn't render images, etc as quickly)
8. Letsencrypt (for SSL/https certificates)
9. AWS for hosting (Ubuntu 14.04)

## Structure of Django Project
* For each application, the static directory holds the CSS and javascript responsible for
rendering that particular application. The templates directory holds the HTML templates.
The urls.py file contains the URLs that are mapped to that particular application.
The views.py contains all the logic needed to handle the user interactions with that
particular application.
* homepage: application that handles the interactions with the homepage.
* questionpage: application that handles the interactions for posting and answering a question.
* pso: application that handles all initial HTTP requests to Penn Stack Overflow.
* templates: directory that contains base.html template that all other HTML templates extend.
* userpage: application that handles interactions with the user profile. 


## Notes on Git Branches
- Run "git branch branch_name" to make new branch
- Run "git checkout branch_name" to checkout branch
- Run "git push origin branch_name" to push
- Run "git branch -d branch_name" to delete branch
