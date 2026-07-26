## Screenshots
 
<!-- Add screenshots of the site here -->
 
---
 
## Description
 
FanVerse is a Django blogging web application designed around flexible post ownership and user privacy. The platform allows users to invite co-authors, hand off full ownership to another user, or step down to a collaborator role. Authors can post anonymously while retaining editing rights, or permanately orphan a post to unlink their profile while preserving the post's contents for the community. The app also includes a notification center for collaboration invites and transfer requests, threaded comments, and account settings for profile customization and username changes.
<!-- Describe what FanVerse is and what it does -->
 
## Motivation

Many online platforms assume content ownership is straightforward, where one user creates, edits, and owns a post forever. In the real world, user needs are much more complex. People co-author projects, transfer ownership of a post, or leave platforms entirely without wanting their contributions to be deleted or permanately tied to their identity.

This application was built as part of a research project investigating existing unlinking mechanisms. These mechanisms allow users to detach their personal identity (username, email, or account) from content they previously posted online. As part of our research, we examined top global websites to study how different platforms support content unlinking, account deletion, anonymization, and ownership transfers.

We found that very few websites provide mechanisms to protect user privacy without erasing previously published content. We built FanVerse as a working prototype to bring these unlinking mechanisms together on a single platform. This allowed us to test how anoynmization, post orphaning, collaborator role reassignment, ownership transfers operate inside a single Django application.

To better understand each unlinking mechanims we've implemented, definitions are included below.

Anonymization: Identifying information is hidden from the public but still exists behind the scenes. Content remains published on the site under the "Anonymous" username.

Orphaning: A formal process where the tie between an account and its content is permanently severed, after which editing is not permitted. The account link vanishes while its content remains available on the platform under the "orphan_account" username.

Deletion: The user account is closed while content posted by the account is preserved on the site under the "deleted_account" username.

Username Change: Changing the username attached to the account. The site supports two types of username changes.
        1. All profile links with the old username are broken while the content on            the account is preserved.


<!-- Why we built this project -->
 
## Features
 
<!-- List features organized by category -->
 
## Installation
 
### Prerequisites
 
- Python 3.10 or newer
- Git
### Setup
 
```bash
git clone https://github.com/chumaceroj/FanVerse.git
cd FanVerse
pip install django
```
 
### Database Setup
 
```bash
cd Fandom
python manage.py makemigrations
python manage.py migrate
```
 
### Creating an Admin Account (Optional)
 
```bash
python manage.py createsuperuser
```
 
### Running the Server
 
```bash
python manage.py runserver
```
 
Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
 
## Usage
 
<!-- Describe how to use the site once it's running -->
 
## Project Structure
 
```
Fandom/
├── README.md
├── LICENSE
├── fandomsite/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── blogs/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── context_processors.py
│   └── templates/blogs/
│       ├── base.html
│       ├── index.html
│       ├── detail.html
│       ├── comment_item.html
│       ├── profile.html
│       ├── profile_settings.html
│       ├── post_settings.html
│       ├── notifications.html
│       ├── create_blog.html
│       ├── edit_blog.html
│       ├── edit_comment.html
│       ├── edit_profile.html
│       ├── change_username.html
│       ├── delete_account.html
│       ├── login.html
│       └── register.html
└── manage.py
```
 
## Technologies
 
- Python
- Django
- HTML
## Known Limitations
 
<!-- List any known bugs or limitations -->
 
## Authors
 
- Julian Chumacero
- Lewhat Kahsay
 
## License
This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.
