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

#### Description
Account deletion permanently removes a user's account, profile, and all associated account data from the platform. All previously published posts and comments are preserved on the site, with the author's name replaced by "deleted_user." This ensures that community content is not lost when a user leaves the platform.

#### Motivation
This feature was informed by our observations of Reddit, Pinterest, and Tumblr. Reddit's throwaway account culture demonstrated a clear need for users to be able to leave the platform without erasing their contributions. Pinterest and Tumblr both preserve user-generated content after account deletion. Our implementation follows a similar approach, ensuring all posts and comments remain publicly available while fully removing the user's identity and account data.

#### Who Can Use It
Any logged-in user can delete their own account from Profile Settings.

#### How It Works
1. The user navigates to Profile Settings and clicks "Delete Account."
2. A confirmation page warns that the action is permanent and irreversible.
3. Upon confirmation, the user is logged out via Django's `logout()` function.
4. The user object is deleted, which triggers Django's `CASCADE` behavior to remove the user's Profile, Collaboration entries, pending Invitations, and Transfer Requests.
5. Posts and comments are preserved because the author field uses `models.SET_NULL`, which sets the author to `null` rather than deleting the content.
6. The `get_display_author()` method detects the null author and displays "deleted_user."

#### Effect on Related Data
- **Posts:** All posts remain published. The author name changes to "deleted_user."
- **Comments:** All comments remain published. The author name changes to "deleted_user."
- **Collaborations:** The user is removed from all collaborations. Remaining collaborators can still edit posts they collaborate on.
- **Pending invitations:** All sent and received invitations are deleted.
- **Transfer requests:** All pending transfer requests submitted by the user are deleted.
- **Profile:** The user's profile and biography are permanently deleted.
- **Anonymous posts:** If the user had anonymized posts, the display changes from "Anonymous" to "deleted_user."
- **Preserved usernames:** If the user had previously used "preserve old username," the frozen username changes to "deleted_user."
- **Orphaned posts:** Posts that were orphaned before deletion remain as "orphan_account" and are not affected.

#### Edge Cases
- If the deleted user was the owner of a post with collaborators, collaborators retain editing access but the post has no owner and post settings are inaccessible.
- If the user had anonymized posts, the display overrides from "Anonymous" to "deleted_user."
- If the user had preserved an old username on past posts, those frozen usernames are replaced with "deleted_user."
- Orphaned posts are unaffected since the author link was already severed before deletion.

#### Reversibility
Account deletion is irreversible. Once confirmed, the account and all associated data cannot be recovered.

### 2.7 Direct Ownership Transfer

#### Description
Direct ownership transfer allows the current owner of a post to immediately transfer full ownership to any registered user by entering their username. Once transferred, the new user becomes the primary owner with full access to editing and Post Settings, while the original owner loses all access to the post.

#### Motivation
This feature was informed by our observation of direct transfer mechanisms across several platforms including YouTube (channel transfer), GitHub (repository transfer), Blogspot (blog transfer), and Shopify (store/blog transfer). These platforms offer a built-in "transfer ownership" feature where ownership is moved in a single action. Our implementation follows this model, providing a one-step transfer directly from Post Settings without requiring admin involvement or a collaboration relationship.

#### Who Can Use It
Only the current post owner can initiate a direct transfer.

#### How It Works
1. The owner navigates to Post Settings and locates the "Transfer Post" section.
2. The owner enters the username of the intended recipient.
3. A confirmation dialog warns that the action is permanent and the owner will lose all privileges.
4. Upon confirmation, the `transfer()` method updates `blog.author` to the new user and clears any preserved `original_author_name`.
5. The Collaboration table is updated to remove the old owner's entry and create or update an owner entry for the new user.
6. The original owner is immediately redirected and no longer has access to edit or manage the post.

#### Effect on Related Data
- **Collaborators:** All existing collaborators remain on the post and retain their editing access under the new owner.
- **Original owner:** The original owner loses all access. They do not become a collaborator.
- **Comments:** All comments remain unchanged.
- **Anonymous status:** If the old owner had anonymized themselves on the post, the post continues to display "Anonymous" for that author. The new owner's name displays normally unless they choose to anonymize themselves.
- **Preserved username:** Any previously frozen `original_author_name` is cleared so the new owner's current username displays.
- **Pending invitations:** Existing pending collaboration invitations remain tied to the post.

#### Edge Cases
- If the recipient is already a collaborator on the post, they are promoted to owner and their collaboration entry is updated. The old owner loses all access.
- Transferring to yourself is permitted but has no practical effect.
- If the post has pending admin-mediated transfer requests, those remain in the system after a direct transfer.
- If the old owner had anonymized themselves on the post, the "Anonymous" label remains for that author entry even after transfer.

#### Reversibility
Direct ownership transfer is irreversible. The original owner cannot regain ownership unless the new owner transfers it back.

### 2.8 Admin-Mediated Ownership Transfer

#### Description
Admin-mediated ownership transfer allows the current owner of a post to request a transfer of ownership to another user through an administrative review process. Unlike direct transfer, ownership is not updated immediately. A site administrator must review and approve the request before the transfer is executed.

#### Motivation
This feature was informed by our observation of admin-mediated transfer processes on Vimeo (video transfer), Internet Archive (content transfer), and Medium (publication transfer). These platforms require users to contact platform staff via emails, forms, or support tickets to complete a transfer between accounts. Our implementation formalizes this process through a built-in request system within Post Settings, allowing owners to submit a transfer request that administrators can review and approve or deny through the Django admin panel.

#### Who Can Use It
Only the current post owner can submit an admin-mediated transfer request.

#### How It Works
1. The owner navigates to Post Settings and locates the "Admin Mediated Transfer" section.
2. The owner enters the username of the intended recipient.
3. The system validates that the username exists and that the owner is not transferring to themselves.
4. A `TransferRequest` object is created in the database with a status of "PENDING."
5. An administrator reviews the request in the Django admin panel and changes the status to "APPROVED" or "DENIED."
6. If approved, the `TransferRequest.save()` method automatically executes the transfer, updating `blog.author` to the new user, identical to a direct transfer.
7. Both the requester and the recipient are notified of the outcome and can independently dismiss the notification.

#### Effect on Related Data
- **Collaborators:** All existing collaborators remain on the post and retain their editing access under the new owner.
- **Original owner:** The original owner loses all access upon approval. They do not become a collaborator.
- **Comments:** All comments remain unchanged.
- **Anonymous status:** If the old owner had anonymized themselves on the post, the post continues to display "Anonymous" for that author. The new owner's name displays normally unless they choose to anonymize themselves.
- **Preserved username:** Any previously frozen `original_author_name` is cleared so the new owner's current username displays.
- **Pending invitations:** Existing pending collaboration invitations remain tied to the post.

#### Edge Cases
- Only one transfer request can be pending for a post at a time. The owner cannot submit multiple requests to different users simultaneously.
- If the entered username does not exist, an error message is displayed and no request is created.
- If the owner tries to transfer to themselves, an error message is displayed and no request is created.
- If the owner directly transfers the post while an admin-mediated request is still pending, the pending request remains in the system.
- If the request is denied, the post remains unchanged and the owner retains full ownership.

#### Reversibility
Admin-mediated transfer is irreversible once approved. If denied, no changes are made and the owner can submit a new request.


### 2.9 Permission Reassignment

#### Description
Permission reassignment allows the current owner of a post to promote an existing collaborator to owner. The original owner is automatically demoted to a collaborator role, losing access to Post Settings and owner-only features while retaining editing access. This mechanism requires the recipient to already be a collaborator on the post, distinguishing it from direct transfer.

#### Motivation
This feature was informed by our observation of permission reassignment patterns across platforms like Google Drive (document transfer), Discord (server transfer), and AO3 (co-creation transfer). Users manually give someone else full or owner-level access through invitation or collaboration, then remove or demote their own role. Our implementation formalizes this pattern by allowing the owner to promote a collaborator to owner directly from Post Settings, with the demotion happening automatically.

#### Who Can Use It
Only the current post owner can initiate a permission reassignment, and only existing collaborators on that post are eligible to be promoted.

#### How It Works
1. The owner navigates to Post Settings and locates the "Reassign Owner" section, which only appears if the post has at least one collaborator.
2. The owner selects a collaborator from a dropdown menu.
3. A confirmation dialog warns that they will lose owner privileges and become a collaborator.
4. Upon confirmation, the selected collaborator's role is updated to "owner" in the Collaboration table.
5. The old owner's role is updated to "collaborator" using `get_or_create` to handle cases where the owner may not have had an existing Collaboration entry.
6. The `blog.author` field is updated to the new owner via the `transfer()` method.
7. The old owner is redirected to the blog detail page, where they now see the collaborator panel instead of Post Settings.

#### Effect on Related Data
- **New owner:** Gains full access to Post Settings, including anonymization, transfers, orphaning, inviting collaborators, and reassigning ownership again.
- **Old owner:** Demoted to collaborator. Retains editing access and can anonymize themselves, but loses access to Post Settings. Can leave the collaboration at any time.
- **Other collaborators:** Unaffected. They retain their existing roles and editing access.
- **Comments:** All comments remain unchanged.
- **Anonymous status:** If the old owner had anonymized themselves on the post, they remain anonymous as a collaborator. The new owner's name displays normally unless they choose to anonymize themselves or are already anonymous
- **Preserved username:** Any previously frozen `original_author_name` is cleared so the new owner's current username displays.

#### Edge Cases
- The reassign option only appears in Post Settings when at least one collaborator exists on the post.
- If the owner does not have an existing Collaboration entry (possible for posts created before the collaboration system was added), one is automatically created and then demoted.
- The new owner can immediately reassign ownership to another collaborator if desired.
- If the old owner wants to fully disconnect from the post after being demoted, they can use the "Leave Collaboration" button.

#### Reversibility
Permission reassignment is not directly reversible. The demoted owner would need the new owner to reassign ownership back to them. The demoted owner can also leave the collaboration entirely at any time.

### 2.10 Username Change

#### Description
Username change allows a user to update their username with two options for how past content is handled. The "preserve old username" option keeps the old username displayed as unlinked plain text on all existing posts, comments, and collaborations, while all future content uses the new username. The "update all posts" option retroactively updates all past content to display the new username with an active profile link.

#### Motivation
This feature was informed by our observation of GitHub, where email is linked to commit history. If a user changes their email, old commits are no longer linked to their account and become unclickable. We applied a similar concept to usernames, treating them as identity markers tied to content. Our implementation gives users explicit control over whether their past content stays linked to their old identity or updates to reflect their new one.

#### Who Can Use It
Any logged-in user can change their username from Profile Settings.

#### How It Works
1. The user navigates to Profile Settings and clicks "Change Username."
2. The user enters a new username and selects one of two options:
   - **Preserve old username:** The current username is saved to `original_author_name` on all blogs and comments, and `original_username` on all collaborations owned by the user. These display as plain text with no profile link.
   - **Update all posts:** Any previously saved old usernames are cleared from blogs, comments, and collaborations, so all content displays the new username with an active profile link.
3. The system checks that the new username is not already taken.
4. The `User.username` field is updated and saved.
5. The user is redirected to their profile under the new username.

#### Effect on Related Data
- **Posts (preserve):** All existing posts display the old username as unlinked plain text. Future posts display the new username with a profile link.
- **Posts (update):** All existing and future posts display the new username with a profile link.
- **Comments:** Same behavior as posts for both options.
- **Collaborations:** Same behavior as posts for both options. The old username shows as unlinked plain text on posts the user collaborates on when "preserve" is selected.
- **Profile:** The profile URL updates to the new username. The old profile URL no longer works.
- **Profile link on past content (preserve):** Old username text is not clickable and does not link to any profile.

#### Edge Cases
- If the new username is already taken, an error is displayed and no changes are made.
- If a user changes their username multiple times using "preserve," the saved name updates to whatever their username was at the time of the most recent change.
- If a user previously used "preserve" and later changes again with "update all posts," the previously saved old usernames are cleared and everything updates to the newest username.
- The old username becomes available for other users to claim after the change.

#### Reversibility
Username changes are reversible by changing back to the original username, provided no other user has taken it. However, if "preserve old username" was selected, previously saved old names would need to be manually cleared by choosing "update all posts" on a subsequent change.

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