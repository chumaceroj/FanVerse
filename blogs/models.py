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
        self.author = new_owner
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
    # Links comment to specific Blog post (one-way connection)
    # "related_name" is a shortcut: allows us to grab all comments by looking at a Blog, using .comments
    # Automatically deletes comments from deleted Blog
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name = 'comments')
    # Links comment to User
    # If the User deletes their account, keep the comment (author = null)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_orphaned = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    original_author_name = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f"Comment by {self.get_display_author()} at {self.created_at} on {self.blog.title}"
    
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
        if self.is_anonymous:
            return "Anonymous"
        if self.author is None:
            return "deleted_user"
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collaborations')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blog', 'user')  # prevents duplicate entries

    def __str__(self):
        return f"{self.user.username} - {self.role} on {self.blog.title}"


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
