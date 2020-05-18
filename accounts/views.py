from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact


# Create your views here.
def register(request):
    if request.method == 'POST':
        print ('----------SUCCESSFUL REGISTRATION----------')
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            # Check Username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is already in use')
                    return redirect('register')
                else:
                    # Looksgood
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    # # Login after register
                    # auth.login(request, user)
                    # messages.success(request, 'Successful Login')
                    # return redirect('login')
                    user.save()
                    messages.success(request, 'You are currently logged in')
                    return redirect('login')
        else:
            messages.error('Passwords Do Not Match')
            return redirect('register')

    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Currently Logged in')
            return redirect('dashboard')
            print ('----------LOGGED IN----------')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:    
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'YOu are logged out')
        return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    
    context ={
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)