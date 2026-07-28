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
- The author navigates to the post and selects **Post Settings**.
- The author selects **Go Anonymous** (or **Reveal Identity** if currently anonymous).
- The form sends a POST request to anonymize_blog.
- The view updates the blog.is_anonymous boolean in the Blog model and redirects back to the post page.

#### Effect on Related Data
- **Collaborators:** Collaborator names are not affected by the owner's anonymization. Each collaborator controls their own anonymization independently.
- **Comments:** Comments on the post are not affected. Comment authors remain visible regardless of post anonymization status.
- **Profile links:** The owner's profile link is removed from the post and replaced with "Anonymous." The post no longer appears on the owner's public profile page.
- **Post content:** The title, content, and timestamp remain unchanged and publicly visible.
- **Editing privileges:** The owner retains full editing access and can still access Post Settings.

#### Edge Cases
- Account deletion process overrides an anonymous author, changing from Anonymous to deleted_user.
- If an owner anonymizes themselves and the post has collaborators, the collaborators names remain visible.

#### Reversibility
Anonymization is reversible for posts.


### 2.2 Collaborator Anonymization

#### Description
Collaborator anoynmization allows a co-author to hide their username on a shared post while maintaining their editing privileges and collaborator role. When selected, the collaborator's username is replaced with "Anonymous" on both the homepage and post detail page. The post remains published and the author's identity is preserved in the database.

#### Motivation
This feature was informed by our observation of AO3 (Archive of Our Own), which allows authors to post works anonymously while maintaining ownership. While AO3's implementation preserves content while hiding an author's identity, the platform uses an all-or-nothing approach, either hiding the identies of all authors or none. Our implementation builds on AO3's anonymization mechanism by enabling collaborators to indepedently toggle their public visibility without altering the primary owner's settings or revoking collaborator editing access.

#### Who Can Use It
Any active collaborator on a post.

#### How It Works
- The collaborator navigates to the post.
- In the collaborator controls block below the post, the collaborator selects **Go Anonymous** (or **Reveal Identity** if currently anonymous).
- The form submits a POST request to anonymize_collaborator.
- The view updates the collab.is_anonymous boolean on the user's Collaboration model and redirects back to the post page

#### Effect on Related Data
- **Post Owner:** The primary owner's name, visibility settings, and management controls remain unaffected.
- **Collaborators:** Other collaborator names are not affected by the one collaborators's anonymization. Each collaborator controls their own anonymization independently.
- **Comments:** Comments on the post are not affected. Comment authors remain visible regardless of post anonymization status.
- **Profile links:** The collaborator's profile link is removed from the author line on the post and replaced with "Anonymous." The post no longer appears on the colaborator's public profile page.
- **Post content:** The title, content, and timestamp remain unchanged and publicly visible.
- **Editing privileges:** The collaborator retains full editing access and can still access collaborator settings (**Edit Blog Post**, **Go Anonymmous**, and **Leave Collaboration**).

#### Edge Cases
- If an anoynmous collaborator deletes their account, the collaborator's name is changed to deleted_user. The collaboration record is preserved in the database to facilitate this name change.
- If an anonymous collaborator is promoted to primary owner via **Reassign Owner**, ownership transfers to the anonymous collaborator and the collaborator's anonymization state is preserved (name remains Anonymous).
- If an anonymous collaborator selects **Leave Collaboration**, their Collaboration record is deleted from the database. The user loses editing access and their name (Anonymous) is stripped from the post.

#### Reversibility
Collaborator anonymization is reversible. Collaborators can click **Reveal Identity** at any time on the post detail page.


### 2.3 Comment Anonymization

#### Description
Content anonymization allows the author of a comment to hide their username from public view while retaining ownership and editing privileges of the comment. When selected, the comment author's username is replaced with "Anonymous" on the post page, while the comment content and reply chain remain intact.

#### Motivation
This feature was informed by by our observation of AO3 (Archive of Our Own), which supports comment anonymization through temporary "anonymous collections". On AO3, commenters identities on a post can only be hidden if the post itself is placed in an anonymous collection. Even then, anonymity only applies to the post creator's comments/replies (marked as "Anonymous Creator"), while the identites of general commenters remain visible. If the post is later removed from the anonymous collection, all creator replied reveal the author's username. Our implementation improved upon this design by offering user-level comment anonymization. Indivual commenters can independently anonymize each of their own comments, ensuring their privacy selections are persistent and not tied to or overriddden by post owners.

#### Who Can Use It
The logged-in author of the comment.

#### How It Works
- The comment author navigated to the post detail page where their comment is posted.
- Below their comment, the author selects **Go Anonymous** (or **Reveal Identity** if currently anonymous).
- The form submits a POST request to anonymize_comment.
- The view updates the is_anonymous boolean on the Comment model and redirects back to the post page.

#### Effect on Related Data
- **Post Owner:** The primary owner's name, visibility settings, and management controls remain unaffected.
- **Collaborators:** Collaborator names are not affected by the an individual's comment anonymization. Each commenting user and collaborator controls their own anonymization independently.
- **Comments:** The specific comment's author name is updated to "Anonymous". Parent comments and nested reply chains remain unaffected.
- **Profile links:** The comment author's profile link is removed from the comment header and replaced with "Anonymous." The comment no longer appears on the authors public profile page under their comment history.
- **Post content:** The title, content, and timestamp remain unchanged and publicly visible.
- **Editing privileges:** The comment author retains full editing privileges over their comment. They can still access **Edit Comment**, **Go Anonymmous**/**Reveal Identity**, or **Orphan Comment**.

#### Edge Cases
- If an anonymous comment author deletes their account, the comment author's name updates to "deleted_user". The comment's contents and reply chain remain intact.
- If the parent post is orphaned, comment authors retain full ownership and control settings of their individual comments.
- If a comment is orphaned by its author, it can no longer be anonymized or de-anonymized. Orphaning permanately removes editing privileges and severs the link between a post/comment and its user account.

#### Reversibility
Comment anonymization is reversible. The author can select **Reveal Identity** on their comment at any time to restore their username and public profile link.


### 2.4 Post Orphaning

#### Description
Post orphaning allows the primary owner of a post to permanently sever their ownership link to the post while keeping the title, content, and comments publicly available on the platform. Once orphaned, all author usernames are replaced with "orphan_account", all associated collaboration records are deleted, and editing privileges are permanently revoked for all authors.

#### Motivation
This feature was directly informed by AO3 (Archive of Our Own), which allows creators to permanently orphan works so that contributions remain available to the community without remaining attached to the author's profile. Our implementation adapts AO3's orphaning mechanism to collaborative posts. When a primary owner chooses to orphan a post, the platform severs all author and collaborator links simultaneously, while preserving the post's contents and comments.

#### Who Can Use It
The primary owner of the post.

#### How It Works
- The primary owner navigates to the post detail page and selects **Post Settings**.
- The owner selects **Orphan Post**.
- The form submits a POST request to orphan_blog.
- The view updates the is_orphaned boolean and deletes all Collaboration records associated with the post

#### Effect on Related Data
- **Post Owner:** The primary owner's account link is permanently removed and the author name is changed to "orphan_account". The owner loses ownership of the post, removing editing and post settings access.
- **Collaborators:** All active collaboration records associated with the post are permanently deleted (thereby removing editing privileges). Collaborator names are removed from the author line, and the author display is updated to "By: orphan_account."
- **Comments:** Comments on the post remain publicly available. Comment authors retain full control over their individual comments (including the ability to edit, anonymize, or orphan their own comments).
- **Profile links:** The post is permanently removed from the primary owner's and all former collaborators' profile pages. The post detail page no longer links to any author profile.
- **Post content:** The title, content, and timestamp remain unchanged and publicly visible.
- **Editing privileges:** Editing access is permanently revoked for everyone. Neither the former primary owner nor former collaborators can edit the post or manage settings.

#### Edge Cases
- When a post with collaborators is orphaned, all collaborator ties are severed alongside the primary owner's tie. The entire author line is replaced by "orphan_account", and collaborators lose editing access and all controls (**Edit Blog Post**, **Go Anonymous**, and **Leave Collaboration**).
- If a post is orphaned while a collaboration invitation is pending, the invited user cannot join the orphaned work. When the invited user selects **Accept** on their Notifications page, the system displays an error banner reading "This post was orphaned and is no longer accepting collaborators," and automatically deletes the invitation from the database.
- If a post was anonymized prior to being orphaned, the orphaning state takes precedence ("Anonymous" is replaced with "orphan_account").
- When a user deletes their account, all orphaned posts will remain under the name "orphan_account" (will not be replaced with "deleted_user").


#### Reversibility
Post orphaning is irreversible. Once a post is orphaned, the connection between the account and the post is permanently deleted from the database and cannot be restored by the former owner or collaborators.


### 2.5 Comment Orphaning

#### Description
Comment orphaning allows the author of a comment to permanently sever their ownership link to their comment while keeping the comment body and reply thread publicly avaible. Once orphaned, the comment author's name is replaced with "orphan_account" and editing privileges over that comment are permanently revoked.

#### Motivation
This feature was informed by by our observation of AO3 (Archive of Our Own), which allows creators to permanently orphan works so that contributions remain available to the community without remaining attached to the author's profile. While AO3 allows users to orphan entire works, they do not offer a mechanims to orphan individual commenets. Our implementation extends AO3's orphaning mechanism to the comment level. By giving users the granular option to orphan individual comments, commenters can permanently detach their identity from public discussions without influencing the surrounding conversation or nested reply chains.

#### Who Can Use It
The logged-in author of the comment.

#### How It Works
- The comment author navigates to the post detail page where their comment is published.
- Beneath their comment, the author selects **Orphan Comment**
- The form submits a POST request to orphan_comment
- The view updates the is_orphaned boolean in the Comment model and redirects back to the post page.

#### Effect on Related Data
- **Post Owner:** The primary owner's name, visibility settings, and management controls remain unaffected.
- **Collaborators:** Collaborator names, visibility, and editing settings are not affected by an individual's orphaned comment.
- **Comments:** The specific comment's author name is permanently changed to "orphan_account". The comment text,timestamp, and all nested replies remain publicly available.
- **Profile links:** The author link is permanently removed from the comment header. The comment no longer appears on the author's profile page under comment history.
- **Post content:** The title, content, and timestamp remain unchanged and publicly visible.
- **Editing privileges:** Editing access is permanently revoked for the comment author. The author can no longer edit the comment or toggle anonymization.

#### Edge Cases
- If a parent comment is orphaned, any child replies nested beneath it remain publicly available and linked to the parent comment. Authors of the reply comments retain full ownership and editing access over their own replies.
- If a comment was set to "Anonymous" before being orphaned, the orphaning state takes precedence. get_display_author() overrides the "Anonymous" label and permanently displays "orphan_account".
- If a comment author later deletes their account after having orphaned a comment, the orphaned comment remains labelled "orphan_account" (is not changed to "deleted_user").
- If the parent post itself is orphaned, existing comments can still be orphaned independently by their respective authors.

#### Reversibility
Comment orphaning is irreversible. Once a comment is orphaned, the database connection between the user account and the comment is permanently severed and cannot be restored.


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

#### Description
Leaving a collaboration allows an active co-author of a shared post to remove themselves from the post's collaboration group. Upon leaving, the user's Collaboration record is deleted from the database, their username is removed from the post's author line, and all editing access and controls are permanently revoked for that user. 

#### Motivation
This feature was informed by multi-author collaboration on platforms like Google Docs (removing self from shared document) and Notion (removing self from shared workspace). On these platforms, contributors can disassociate themselves from a project at any time. Our implementation preseves this independent disassociation, allowing collaborators to remove themselves from a project without requiring intervention from administrators or the primary post owner.

#### Who Can Use It
Any active collaborator on a post (excluding the primary owner).

#### How It Works
- The collaborator navigates to the post detail page.
- In the collaborator controls section below the post, the collaborator selects **Leave Collaboration**.
- The form submits a POST request to leave_collaboration.
- The view deletes the collaborators Collaboration instance and redirects back to the psot page.

#### Effect on Related Data
- **Post Owner:** The primary owner's name, visibility settings, and management controls remain unaffected.
- **Collaborators:** The leaving collaborator's name is permanently removed from the author line, and the collaborator loses all editing and control access. Other collaborator names, visibility, and editing settings are not affected by an individual collaborator's departure.
- **Comments:** Comments left by the departing collaborator on the post remain intact and visible. The author link on those comments continues to point to their user profile. All other comments remain unchanged.
- **Profile links:** The post is permanently removed from the departing collaborator's profile under posts. The departing collaborator's name and profile link are permanently removed from the author line. All other profiles (primary owner and other collaborators) remain intact.
- **Post content:** The title, content, and timestamp remain unchanged and publicly visible.
- **Editing privileges:** Editing access is permanently revoked for the departing collaborator. They no longer have access to collaborator controls (**Edit Post**, **Go Anonymosu**, and **Leave Collaboration**).

#### Edge Cases
- Primary owners cannot use **Leave Collaboration** to leave a post. Ownership must be reassigned via **Reassign Owner**, **Transfer Post**, or **Admin Mediated Transfer**, or the post must be orphaned via **Orphan Post**.
- If an anonymized collaborator leaves the post, their Collaboration record is deleted, removing "Anonymous" from the author line and clearing all record of their involvement.
- If a post is orphaned, all Collaboration records are deleted automatically, making **Leave Collaboration** inaccessible.

#### Reversibility
Leaving a collaboration is irreversible by the user. To rejoin the collaboration, the pimary owner must send a new invitation from **Post Settings**, which the user must accept from their Notifications page.


## 4. Comments
### 4.1 Posting Comments

#### Description
Post comments allows authenticated users to submit public feedback and participate in discussions beneath a post. The platform supports both top-level comments directly on the post and nested replies to exisitng comments.

#### Motivation
This feature was informed by community discussion and Q&A platforms like Reddit and Tumblr, where user engagement and threaded commentary are essential features. Our implementation provides a similar comment structure, with both top-level commments and nested replies. This allows users to reply directly to specific comments, creating discussion threads that perserve multi-user conversations without cluttering the main post comment thread.

#### Who Can Use It
Any logged-in user.

#### How It Works
- The user navigates to the post detail page.
- To leave a top level-comment, the user enters text into the main comment box below the post and selects **Post Comment**.
- To reply to an existing comment, the user selects **Reply** beneath that specific comment, enters text into the reply field, and selects **Submit Reply**.
- The form submits a POST request to add_comment.
- The view creates a Comment record associated with the requesting user, and redirects back to the post page.

#### Effect on Related Data
- **Post Owner:** The primary owner's name, visibility settings, and management controls remain unaffected.
- **Collaborators:** Collaborator names, visibility, and editing settings are not affected by a comment posted by a user.
- **Comments:** A new Comment record is created in the database. If submitted as a reply, it is linked to its parent comment via parent_id, updating the thread structure under that comment. All previous comments remain unchanged and visible.
- **Profile links:** The new comment displays the author's name linked to their profile. The comment appears under the author's profile in their comment history. 
- **Post content:** The title, content, and timestamp remain unchanged and publicly visible.
- **Editing privileges:** The comment author gains editing and managment access over their new comment (**Edit Comment**, **Go Anonymous**, and **Orphan Comment**). Neither the post owner nor collaborators gain editing privileges over the new comment.

#### Edge Cases
- If a user selects **Post Comment** with an empty comment, a message bubble reading "Fill out this field" points to the text box.
- If a user selects **Post Comment** with a comment only containing whitespace, a comment record is not created in the database and the page reloads without throwing an error.
- If a post is orphaned, users may still comment freely below the post. If a comment is orphaned, users may still freely reply to the comment. A post's/comment's orphaned state does not restrict reader interaction or discussion threads.

#### Reversibility
Posting a comment is not directly reversible via an undo action. An author can modify the comment via **Edit**, hide thier identity via **Go Anonymous**, or permanently detach their account link via **Orphan**.


### 4.2 Threaded Replies

#### Description
Threaded replies allow authenticated users to respond directly to exisitng comments on a post. This organizes discussion into clear parent-child relationships, grouping replies beneach the specific comment they reference.

#### Motivation
This feature was informed by and modeled after platforms like Reddit, where multi-user discussions are displayed in a nested structure. In flat structures, context is easily lost when multiple users respond to different points simultaneously. Like Reddit, our implementation preserves conversation context by nested child replies directly under their parent comment. This allows sub-discussions to occur without cluttering the primary content section.

#### Who Can Use It
Any logged-in user.

#### How It Works
- The user navigates to the post detail page and locates the target comment.
- Below the comment, the user selects **Reply**, which toggles the inline reply text box.
- The user enters their response and selects **Submit Reply**.
- The form submits a POST request to add_comment, passing along the hiddent parent_id field
- The view creates a new Comment record linked to both the Blog post and the parent Comment instance, then redirects back to the post detail page.

#### Effect on Related Data
- **Post Owner:** The primary owner's name, visibility settings, and management controls remain unaffected.
- **Collaborators:** Collaborator names, visibility, and editing settings are not affected by a comment posted by a user.
- **Comments:** A new child Comment record is created in the database referencing the parent comment ID. The parent comment's thread expands to display the nested replay, while all existing comments remain intact.
- **Profile links:** The reply displays the commenter's name linked to their profile (unless anonymized). The reply appears under the commenter's profile under comment history.
- **Post content:** The title, content, and timestamp remain unchanged and publicly visible.
- **Editing privileges:** The reply author gains editing and managment access over their reply (**Edit Comment**, **Go Anonymous**, and **Orphan Comment**). Parent comment authors post owners, and collaborators gain no editing control over the new reply.

#### Edge Cases
- Users can freely reploy to comments authored by "Anonymous" and "orphan_account". The thread structure links to the parent comment ID regardless of whether the parent author's identity is hidden or if the parent is orphaned.
- If a parent comment is deleted or orphaned, all child replies remain nested beneath it without breaking the thread structure (parent comment's name merely changes to "deleted_user" or "orphan_account").
- If a user selects **Submit Reply** with an empty comment, a message bubble reading "Fill out this field" points to the text box.
- If a user selects **Submit Reply** with a comment only containing whitespace, a comment record is not created in the database and the page reloads without throwing an error.

#### Reversibility
Submitted a threaded reply is not directly reversible. The author can modify their response via **Edit**, hide their identity via **Go Anonymous**, or permanently detatch their account link via **Orphan**.


### 4.3 Editing Comments

#### Description
Editing comments allows the original author of a comment to modify its text content after posting. Once edited, the comment body is updated in place on the blog post detail page without altering the original creation timestamp, thread structure, or parent-child relationships.

#### Motivation
This feature was informed by platforms like Reddit and Discord, where users frequently update information, correct errors, or clarify phrasing in their posts. On discussion focused platforms, forcing users to delete and repost comments breaks thread continuity. Our implementation provides an editing button that allows commenters to change their existing comments while leaving surrounding nested discussion threads intact.

#### Who Can Use It
The logged-in author of the comment (provided the comment has not been orphaned).

#### How It Works
- The comment author navigates to the post detail page containing their comment.
- Beneath their comment, the author selects **Edit**.
- The user is navigated to the comment edit form view which pre-fills a text area with the comment's current content.
- After editing, the user selects **Save Changes**.
- The form submits a POST request to edit_comment.
- The view updates the comment's content with the new text submitted and redirects back to the posts detail page.

#### Effect on Related Data
- **Post Owner:** The primary owner's name, visibility settings, and management controls remain unaffected.
- **Collaborators:** Collaborator names, visibility, and editing settings are not affected by a comment edit posted by a user.
- **Comments:** The specific comment's content field is updated in the database. Its timestamp, parent, and nested child replies remain unchanged.
- **Profile links:** The comment author's profile link in the comment heading remains active. The updated comment text is viewable in the author's profile under comment history.
- **Post content:** The title, content, and timestamp remain unchanged and publicly visible.
- **Editing privileges:** The comment author retains all management controls (**Edit Comment**, **Go Anonymous**, and **Orphan Comment**). Neither ost owners nor collaborators gain editing control over the edited comment.

#### Edge Cases
- Once a comment is orphaned, a user permanently loses all editing access and management controls.
- If a comment author sets their comment to "Anonymous", they retain editing access and management controls as long as they remain logged into the account that created it.
- If a user edits a comment to be completely blank (deleting the pre-existing text) and selects **Save Changes**, the comment will publicly display the author's name and linked profile. The content of the comment disappears entirely.

#### Reversibility
Editing a comment is reversible through subsequent edits. An author can freely return to the edit form and revise or restore the comment text as many times as desired, provided the comment has not been orphaned. 


## 5. Account Management
### 5.1 Registration and Login

#### Description
Registration and login allow new users to create accounts on the platform and existing users to authenticate securely. Authenticating gives users access to personalized features, including creating posts, managing notifications, leaving and editing comments, and modifying account settings.

#### Motivation
Authentication is a foundational requirement for community-driven platforms. Platforms like AO3, Medium, and Reddit rely on account creation to attribute content, enforce authorization restrictions (ensuring users can only edit or delete their own work), and deliver personalized user dashboards and/or profiles. Our implementation uses Django’s built-in authentication system to provide users with safe login information, view-level access across the platform, and personal profiles.

#### Who Can Use It
- **Registration**: Unauthenticated new users without an account.
- **Login**: Registered users with active account credentials (username and password).

#### How It Works
##### Registration
- The guest user selects **Create User** in the top naviation bar.
- The user enters a unique username and password, and selects **Register User**.
- The form submits a POST rquest to register.
- The view creates a User instance, a corresponding Profile instance, and immediately logs in the user before redirecting to the **All Posts** page.

##### Login
- The user selects **Login** in the top navigation bar.
- The user enters their username and password, and selects **Log In**
- The view processes the POST request using Django's authenticate() and login() functions and redirects the user to **All Posts** page.

#### Effect on Related Data
- **Post Owner:** Logging in restores the user's access to their post management controls (such as **Edit Blog** **Create Post**, **Post Settings**, **Profile Settings** and other features).
- **Collaborators:** Loggin in restores access to active collaboration controls on shared posts (**Edit Post**, **Go Anonymous**, and **Leave Collaboration**).
- **Comments:** Authenticated users gain the ability to submit new top-level comments and replies, as well as access management controls (**Edit**, **Go Anonymous**, and **Orphan**) on their existing comments.
- **Profile links:** Registering establishes a new profile page where the user's authored posts and comment history are aggregated.
- **Post content:** Account creation and authentication do not directly alter existing blog post titles, body text, or timestamps.
- **Editing privileges:** Authentication unlocks permission checks across the platform (can_edit(), is_owner(), etc), enabling authorized users to modify their respective posts and comments.

#### Edge Cases
- Django's User model requires unique usernames. If a user attempts to register with an existing username, the platform displays an error reading "Username already taken".
- If a user attempts to log in using a password that does not match the password created during registration, the platform displays an error reading "Invalid credentials. Re-enter your username and password."

#### Reversibility
Registration creates a permanent User record in the database, though account credentials and profile details can be updated via **Profile Settings**. Users can log out at any time to end their session.


### 5.2 User Profiles

#### Description
User profiles serve as public hub pages for each registered user on the platform. A profile displays the user's username, biography, a collection of all active posts they have authored/co-authored as collaborators, and comments they have posted across the site.

#### Motivation
This feature was informed by community writing sites like Medium and Tumblr, where creators have a central profile page to showcase their work and public contributions. Rather than forcing readers to search for posts individually, the user profile aggregates an author's public activity into a single feed while respecting privacy states (such as anonymization and orphaning).

#### Who Can Use It
Any user (both authenticated users and guest visitors) can view user profiles.

#### How It Works
- A user clicks an author's username anywhere on teh platform.
- The profile view retrieves the target User object using get_object_or_404(User, username=username).
- The view searches for database records associated with the user, explicitly filtering out hidden or severed connections ("Anonymous" and "orphan_account").
- The view redirects to a user's profile, displaying the user's bio, created posts, and comment history

#### Effect on Related Data
- **Post Owner:** Viewing a profile does not alter post ownership or management settings. If a user views any profile, direct navigation links to the author's work are readily accessible.
- **Collaborators:** Shared posts where the profile owner is an active co-author are listed in the **Post** section on their profile.
- **Comments:** All active comments authored by the user across any public blog post are listed in their comment history section.
- **Profile links:** The profile page URL acts as the target for all public author links displayed across post headers and comment blocks.
- **Post content:** AViewing a profile does not modify blog post titles, body text, or timestamps.
- **Editing privileges:** Viewing a profile does not alter editing permissions. If a user views their own profile, administrative and editing shortcuts remain accessible via the respective post detail page.

#### Edge Cases
- When a user orphans a post or comment, the orphaned posts or comments automatically disappear from the user's profile history.
- If a post or comment is set to "Anonymous", the post or comment is filtered out of the public profile page.
- Navigating to a profile URL for a username that does not exist in the database returns a standard 404 Not Found error page (via get_object_or_404).
- If a registered user has not authored any posts or written comments, the profile page displays "No posts yet." under **Posts** and "No comments yet." under **Comments**.
- 

#### Reversibility
User profiles are dynamic represenations of the user's current public contributions. Adding, editing, or orphaning posts and comments will instantly update the content displayed on the profile page when refreshed.

### 5.3 Profile Settings

#### Description
Profile settings allow an authenticated user to customize their public profile by editing their biography, changing their username, or deleting their account entirely. This section provides a page for users to update their personal biography that appears at the top of their profile page.

#### Motivation
This feature was informed by community-focused platforms like Pinterest, Facebook, and Tumblr, where user profiles include customizable biographies/descriptions to help creators express their identity. Our implementation is modeled after these platforms, providing users with direct control and editing access over their profile biography and username.

#### Who Can Use It
The authenticated owner of the profile.

#### How It Works
- The logged-in user navigates to **Profile** in the top navigation bar and selects **Profile Settings** from the dropdown.
- The user is presented with three options: **Edit Profile**, **Change Username**, and **Delete Account**
##### Edit Profile 
- Selecting **Edit Profile** directs the user to a form containing a text area pre-filled with their current biography text.
- The user edits the biography text and selects **Save**.
- The form submits a POST request to profile_settings.
- The view updates profile.biography with the submitted text and redirects the user back to their profile page.
##### Change Username
- Selecting **Change Username** directs the user to a page where they may enter their desired new username
- The user selects one of two options: to update all exisitng posts to the new username, or to keep their old username on existing posts.
- The user selects **Change Username**.
- The form submits a POST request to change_username.
- The view updates either all posts or just future posts (based on the user's selection) to the new username and redirects the user back to their profile page.
##### Delete Account
- Selecting **Delete Account** directs the user to a page detailing what will happen.
- The user selects **Delete My Account**.
- The form sends a POST request to delete_account.
- The view deletes the User object, logging the user out and redirecting them to the **All Posts** page.

#### Effect on Related Data
- **Post Owner:** Ownership of authored posts remains intact. If a user changes their username, their posts reflect either the new username or preserve their original name as a static string, depending on the user's choice. If an account is deleted, the user profile page is deleted, preserving past posts on the site with the author name "deleted_user".
- **Collaborators:** Active collaboration links are preserved across username updates. If an account is deleted, their name is removed from the posts' author line without deleting the post itself.
- **Comments:** Comments remain intact and visible across all profile features. Username changes update profile links to point to the new username. If an account is deleted, comments are preserved under the name "deleted_user". Orphaned comments remain preserved under the name "orphan_account".
- **Profile links:** Changing a username updates the user's profile URL route to /profile/<new_username>/. Deleting an account permanently deletes the user's profile page and breaks all associated profile links.
- **Post content:** Profile edits, username changes, acn account deletion do not modify blog post titles, body text, or timestamps.
- **Editing privileges:** Updating a biography or username preserves all editing access. Deleting an account permanently revokes all editing privileges across all authored/co-authored posts and comments.

#### Edge Cases
- If a user attempts to change their username to a username that is already taken by another account, the platform displays an error message reading "Username already taken".
- When an account is deleted, posts and comments are preserved under the "deleted_account" username. Collaboration and Profile records are deleted.
- Posts or comments previously orphaned by the user remain attributed to "orphan_account" upon account deletion (not changed to "deleted_user").
- If a user chooses to preserve their old username on existing posts when changing their username, the system saves their old username in original_author_name on those existing posts and comments before updating the user account. The get_display_author() method checks this field first, ensuring older posts continue displaying the historical name while future posts display the new username.

#### Reversibility
##### Edit Profile (Bio): 
This action is reversible. Biographies can be edited or cleared at any time.
##### Change Username: 
This action is reversible by manually changing the username back to the original string (provided it has not been registered by another user in the interim).
##### Delete Account:
This action is irrevesible. Account deletion permanently deletes the User record, profile data, and collaboration ties in teh database. Preserved posts and comments cannot be reclaimed by the former user.


## 6. Notifications
### 6.1 Collaboration Invites
### 6.2 Transfer Request Updates
### 6.3 Notification Count