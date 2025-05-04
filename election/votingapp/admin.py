from django.contrib import admin

# Register your models here.

from .models import User, Candidate, Vote, Election, ElectionResult, Position

# Register the User model with the admin site
admin.site.register(User)

# Register the Candidate model with the admin site
admin.site.register(Candidate)

# Register the Vote model with the admin site
admin.site.register(Vote)

# Register the Election model with the admin site
admin.site.register(Election)

# Register the ElectionResult model with the admin site
admin.site.register(ElectionResult)

# Register the Position model with the admin site
admin.site.register(Position)