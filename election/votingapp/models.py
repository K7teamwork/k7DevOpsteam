from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib import messages
from django.shortcuts import render, redirect


# Custom User model extending AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


# Custom User model extending AbstractUser
class User(AbstractUser):
    # Validator for username field
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=False,  # Email will be used for login instead of username
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, primary_key=True)
    address = models.CharField(max_length=255)
    has_voted = models.BooleanField(default=False)
    is_eligible = models.BooleanField(default=True) 
     

    # Add related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Custom related name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    # Set email as the field used for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'address']

    # String representation of the User model
    def __str__(self):
        return self.email
    

# Candidate model for election candidates
class Candidate(models.Model):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100, null=True, blank=True)
    votes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='candidates', null=True, blank=True)
    # Add related_name to avoid clashes with auth.User
    position = models.ForeignKey('Position', on_delete=models.CASCADE, related_name='candidates', null=True, blank=True)
    election = models.ForeignKey('Election', on_delete=models.CASCADE, related_name='candidates', null=True, blank=True)
    image = models.ImageField(upload_to='candidate_images/', blank=True, null=True)
    

    # String representation of the Candidate model
    def __str__(self):
        return f"{self.name} ({self.party})"

# Position model for election positions
class Position(models.Model):
    name = models.CharField(max_length=100)
    election = models.ForeignKey('Election', on_delete=models.CASCADE, related_name='positions', null=True, blank=True)
    #candidates = models.ManyToManyField(Candidate)

    # String representation of the Position model
    def __str__(self):
        return self.name

# Vote model to track votes cast by voters
class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)

    # String representation of the Vote model
    def __str__(self):
        return f"{self.voter.full_name} voted for {self.candidate.name}"    


# Election model to manage elections
class Election(models.Model):
    # Name of the election
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    #candidates = models.ManyToManyField(Candidate)
    #positions = models.ManyToManyField(Position)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    # String representation of the Election model
    def __str__(self):
        return self.name

    # Method to check if the election is currently active
    def is_active(self):
        from django.utils import timezone
        return self.start_date <= timezone.now() <= self.end_date

    # Method to get the winner of the election based on votes
    def get_winner(self):
        return max(self.candidates.all(), key=lambda candidate: candidate.votes, default=None)
    
# ElectionResult model to store the results of an election
class ElectionResult(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    winner = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    # String representation of the ElectionResult model
    def __str__(self):
        return f"Result of {self.election.name}: {self.winner.name}"