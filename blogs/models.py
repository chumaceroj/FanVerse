from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model): # creates the Blog class and creates a database table with each field as a column, inherits from models.Model
    title = models.CharField(max_length=200) # Anything in the title column has a max length of 200 characters
    content = models.TextField() # The column of the table with the content of the blog, no length limit
    # ForeignKey links the author column (of IDs) in the Blog table to the column of IDs in the User table
    # If the User deletes their account, keep the blog on the site (author = null)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # null = True allows for null author, blank = True allows for blank authors from admin side
    created_at = models.DateTimeField(auto_now_add=True) # Automatically saves the exact date & time of creation
    is_orphaned = models.BooleanField(default=False)  # Y/N for oprhaning 
    is_anonymous = models.BooleanField(default=False) # Y/N for anonymization
    original_author_name = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} by {self.get_display_author()}"
    
    def orphan(self):
        """Permanently remove the author link, but the content stays posted"""
        self.author = None
        self.is_orphaned = True
        self.save() # saves the changes to the database, only needed when changing the database
        self.collaborations.all().delete()

    def can_edit(self, user):
        """Checks if the blog can still be edited (cannot be orphaned and must be author or collaborator)"""
        if self.is_orphaned:
            return False
        if self.author == user:
            return True
        if self.collaborations.filter(user=user, role='collaborator').exists():
            return True
        return False

    def is_owner(self, user):
        """Checks if the user is the owner (not just a collaborator)"""
        if self.is_orphaned:
            return False
        return self.author == user
    
    def anonymize(self):
        """Hide author from public but keep the link in the database"""
        self.is_anonymous = True
        self.save()

    def deanonymize(self):
        """Reveal author again"""
        self.is_anonymous = False
        self.save()

    def transfer(self, new_owner):
        """Transfer blog ownership to another user"""
        old_owner = self.author 

         # updated: save the existing collaborator's anoynmity state
        existing_collab = Collaboration.objects.filter(blog=self, user=new_owner).first()
        is_anon = existing_collab.is_anonymous if existing_collab else False

        #update the old owner's collaboration record to "collaborator" 
        if old_owner:
            Collaboration.objects.update_or_create(
                blog=self, user=old_owner,
                defaults={'role': 'collaborator'}
            )

        # updated: change new owner's collaboration record to "owner"
        Collaboration.objects.update_or_create(
            blog=self, user=new_owner,
            defaults={'role': 'owner', 'is_anonymous': is_anon}
        )

        self.author = new_owner
        self.original_author_name = None # prevents bugs with changing username

        if is_anon:
            self.is_anonymous = True

        self.save()

    def get_display_author(self):
        """Returns the name to display publicly"""
        if self.is_orphaned:
            return "orphan_account"
        if self.is_anonymous:
            return "Anonymous"
        if self.author is None: # only reaches if is_orphaned is False
            return "deleted_user"
        if self.original_author_name:
            return self.original_author_name
        return self.author.username

    
class Comment(models.Model):
    # links comment to specific Blog post (one-way connection)
    # "related_name" is a shortcut: allows us to grab all comments by looking at a Blog, using .comments
    # automatically deletes comments from deleted Blog
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name = 'comments')
    # links comment to User
    # if the User deletes their account, keep the comment (author = null)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # link to parent comment for comment chaining
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_orphaned = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    original_author_name = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f"Comment by {self.author if not self.is_orphaned else 'Orphaned'} on {self.blog.title}"
    
    def orphan(self):
        self.author = None
        self.is_orphaned = True
        self.save()

    def can_edit(self, user):
        if self.is_orphaned:
            return False
        if self.author != user:
            return False
        return True
    
    def anonymize(self):
        self.is_anonymous = True
        self.save()

    def deanonymize(self):
        self.is_anonymous = False
        self.save()

    def get_display_author(self):
        if self.is_orphaned:
            return "orphan_account"
        if self.author is None:
            return "deleted_user"
        if self.is_anonymous:
            return "Anonymous"
        if self.original_author_name:
            return self.original_author_name
        return self.author.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.CharField(max_length=150)


class Collaboration(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('collaborator', 'Collaborator'),
    ]
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='collaborations')
    # updated: making on_delete to SET_NULL, null=True, blank=True (so the record isn't deleted when account is deleted)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='collaborations')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_anonymous = models.BooleanField(default=False)  # each collaborator can anonymize independently
    original_username = models.CharField(max_length=200, null=True, blank=True)  # frozen username when user picks "preserve"
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blog', 'user')  # prevents duplicate entries

    def __str__(self):
        # update for fallback if user is None
        username = self.user.username if self.user else "deleted_user"
        return f"{username} - {self.role} on {self.blog.title}"

    # updated: helper method to display the right name
    def get_display_name(self):
        if self.user is None:
            return "deleted_user"
        if self.is_anonymous:
            return "Anonymous"
        if self.original_username:
            return self.original_username
        return self.user.username
        


class Invitation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blog', 'invited_user')  # one invite per user per blog

    def __str__(self):
        return f"Invite: {self.invited_user.username} to {self.blog.title} ({self.status})"


class TransferRequest(models.Model):
    # links the blog post being transferred (deletes request if the blog is deleted)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='transfer_requests')
    # links the current owner requesting the transfer 
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transfer_requests')
    # saves target username entered by the requester
    target_user_identifier = models.CharField(max_length=150)
    # tracking request categories
    STATUS_CHOICES = [
        ('PENDING', 'Pending Admin Approval'),
        ('APPROVED', 'Approved'),
        ('DENIED', 'Denied'),
    ]
    # current status of the request (default is PENDING)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    # saves the time when the request was created
    created_at = models.DateTimeField(auto_now_add=True)

    # tracks notification dismissal for each user independently 
    requester_notified = models.BooleanField(default=False)
    target_notified = models.BooleanField(default=False)

    def __str__(self):
        # return a human-readable summary string
        return f"Transfer Request for '{self.blog.title}' to '{self.target_user_identifier}' ({self.status})"

    def save(self, *args, **kwargs):
        # Automatically execute transfer whenever status is changed to APPROVED
        if self.status == 'APPROVED' and self.blog_id is not None:
            new_owner = User.objects.filter(username=self.target_user_identifier).first() or \
                        User.objects.filter(email=self.target_user_identifier).first()
            if new_owner and self.blog and self.blog.author != new_owner:
                self.blog.transfer(new_owner)
        super().save(*args, **kwargs)