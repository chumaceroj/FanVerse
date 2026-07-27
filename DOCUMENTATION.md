# FanVerse Documentation

## 1. Overview

## 2. Unlinking Mechanisms
### 2.1 Post Anonymization

#### Description
Post anonymization allows the owner of a post to hide their username from public view while retaining full editing privileges and ownership. When activated, the author's name is replaced with "Anonymous" on both the homepage and the post detail page. The post remains published and the author's identity is preserved in the database.

#### Motivation
This feature was informed by our observation of AO3 (Archive of Our Own), which allows authors to post works anonymously while maintaining ownership. AO3's implementation handled the core concept well, preserving content while hiding identity. Our implementation builds on this by making anonymization a simple toggle that can be turned on and off at any time directly from Post Settings, making it more accessible for users who may want to temporarily hide their identity.

#### Who Can Use It
Any author, including the owner and any collaborators can anonymize themselves on any post.

#### How It Works

#### Effect on Related Data
- **Collaborators:** Collaborator names are not affected by the owner's anonymization. Each collaborator controls their own anonymization independently.
- **Comments:** Comments on the post are not affected. Comment authors remain visible regardless of post anonymization status.
- **Profile links:** The owner's profile link is removed from the post and replaced with "Anonymous." The post no longer appears on the owner's public profile page.
- **Post content:** The title, content, and timestamp remain unchanged and publicly visible.
- **Editing privileges:** The owner retains full editing access and can still access Post Settings.

#### Edge Cases
- Account deletion process overrides an anonymous author, changing to deleted_user
- If an owner anonymizes themselves and the post has collaborators, the collaborators names remain visible


### Reversibility
Anonymization is reversible for posts


### 2.2 Collaborator Anonymization
### 2.3 Comment Anonymization
### 2.4 Post Orphaning
### 2.5 Comment Orphaning
### 2.6 Account Deletion
### 2.7 Direct Ownership Transfer
### 2.8 Admin-Mediated Ownership Transfer
### 2.9 Permission Reassignment
### 2.10 Username Change

## 3. Collaboration System
### 3.1 Inviting Collaborators
### 3.2 Accepting and Declining Invitations
### 3.3 Collaborator Permissions
### 3.4 Removing Collaborators
### 3.5 Leaving a Collaboration

## 4. Comments
### 4.1 Posting Comments
### 4.2 Threaded Replies
### 4.3 Editing Comments

## 5. Account Management
### 5.1 Registration and Login
### 5.2 User Profiles
### 5.3 Profile Settings

## 6. Notifications
### 6.1 Collaboration Invites
### 6.2 Transfer Request Updates
### 6.3 Notification Count