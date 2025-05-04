# Create your views here.

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import User, Candidate, Vote, Election
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.

def home(request):
    return render(request, 'votingapp/index.html')


# View to handle user registration
def register(request):
    if request.method == 'POST':
        # Get data from the HTML form
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')


        # Validate form inputs
        if not email:
            messages.error(request, 'Email is required.')
            return redirect('register')

        # Validate passwords
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('register')
        
        username = email.split('@')[0]

        # Create the user
        user = User.objects.create_user(
            username=username,  # Use email as the username
            email=email,
            full_name=full_name,
            address=address,
            #password=password1
        )
        user.set_password(password1) 
        user.save()

        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')  # Redirect to the login page
    else:
        return render(request, 'votingapp/register.html')


# View to handle user login
def login(request):
    # Redirect authenticated users to the dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Log the user in
            auth_login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')

    return render(request, 'votingapp/login.html')

# View to handle user logout
@login_required
def logout(request):
    # Clear the session
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')  # Redirect to the login page



# View to handle the dashboard page
@login_required
def dashboard(request):
    user = request.user

    # Fetch all elections
    elections = Election.objects.all()

    # Fetch all candidates and their vote counts
    candidates = Candidate.objects.all()
    candidates_with_votes = [
        {
            'name': candidate.name,
            'party': candidate.party,
            'votes': Vote.objects.filter(candidate=candidate).count(),
            'image': candidate.image,
        }
        for candidate in candidates
    ]

    context = {
        'user': user,
        'elections': elections,
        'candidates_with_votes': candidates_with_votes,
    }

    return render(request, 'votingapp/dashboard.html', context)


#View to handle the voting page
from django.utils import timezone

@login_required
def vote_page(request):
    user = request.user
    now = timezone.now()
    
    # Fetch all elections
    elections = Election.objects.prefetch_related(
        'positions', 
        'positions__candidates'
    ).all()
    
    # Get positions the user has already voted in
    voted_positions = Vote.objects.filter(
        voter=user
    ).values_list('candidate__position_id', flat=True)
    
    # Check if each election has ended
    elections_status = {}
    for election in elections:
        elections_status[election.id] = {
            'has_ended': election.end_date <= now,
            'has_started': election.start_date <= now
        }
    
    context = {
        'user': user,
        'elections': elections,
        'voted_positions': voted_positions,
        'elections_status': elections_status,
        'current_time': now,
    }
    
    return render(request, 'votingapp/onlinevoting.html', context)


# View to handle the voting process
@login_required
def vote(request, candidate_id):
    user = request.user
    now = timezone.now()

    if not user:
        messages.error(request, 'User not found.')
        return redirect('login')

    # Fetch the candidate using candidate_id
    candidate = get_object_or_404(Candidate, id=candidate_id)
    
    # Check if the election has ended
    if candidate.election.end_date <= now:
        messages.error(request, f'The election "{candidate.election.name}" has ended. Voting is no longer allowed.')
        return redirect('vote_page')
    
    # Check if the election has started
    if candidate.election.start_date > now:
        messages.error(request, f'The election "{candidate.election.name}" has not started yet.')
        return redirect('vote_page')
    
    # Check if the user has already voted in this specific position
    if Vote.objects.filter(
        voter=user, 
        candidate__position=candidate.position
    ).exists():
        messages.error(request, 'You have already voted for this position.')
        return redirect('vote_page')
    
    # Handle the POST request to cast the vote
    if request.method == 'POST':
        # Create a new vote
        vote = Vote(candidate=candidate, voter=user)
        vote.save()
        messages.success(request, f'Your vote for {candidate.name} has been cast successfully!')
        
        # Redirect to voting page to continue voting in other positions
        return redirect('vote_page')

    # Render the voting page if the request is not POST
    context = {
        'candidate': candidate,
    }
    return render(request, 'votingapp/vote.html', context)

# View to handle the results page
@login_required
def results(request):
    elections = Election.objects.all()

    # Prepare data for each election
    elections_with_results = []
    for election in elections:
        positions_with_candidates = []
        for position in election.positions.all():
            candidates_with_votes = []
            for candidate in position.candidates.all():
                total_votes = Vote.objects.filter(candidate=candidate).count()
                candidates_with_votes.append({
                    'name': candidate.name,
                    'votes': total_votes,
                    'percentage': (total_votes / Vote.objects.filter(candidate_election=election).count() * 100) if Vote.objects.filter(candidate_election=election).count() > 0 else 0
                })
            positions_with_candidates.append({
                'position': position.name,
                'candidates': candidates_with_votes
            })
        elections_with_results.append({
            'name': election.name,
            'positions': positions_with_candidates
        })

    context = {
        'elections': elections_with_results,
    }
    return render(request, 'votingapp/results.html', context)


# Other views for different pages
def about(request):
    return render(request, 'votingapp/about.html')

def contact(request):
    return render(request, 'votingapp/contact.html')
