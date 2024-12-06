from django.shortcuts import render,redirect
from django.contrib import messages
from . models import User
from django.contrib.auth import authenticate, login as auth_login,logout
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    # You can access the user's username using request.user
    username = request.user.username
    return render(request, 'home.html', {'username': username})

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken!")
            return redirect('register')

        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email,  # Using email as username
                password=password
            )
            messages.success(request, "Registration successful! Please log in.")
            user.generate_verification_code()
            return redirect('otp_verification')
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return redirect('register')
    
    return render(request, 'register.html')

def otp_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        
        try:
            user = User.objects.get(email=email)

            if user.otp == otp and user.otp_expire_at > timezone.now():
                user.is_verified = True
                user.otp = None
                user.otp_expire_at = None
                user.save()

                messages.success(request, "OTP verified successfully! Please log in.")
                return redirect('login')

            else:
                messages.error(request, "Invalid or expired OTP. Please try again.")
        
        except User.DoesNotExist:
            messages.error(request, "No user found with this email address.")

    return render(request, 'otp_verification.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(email,"email")
        print(password,"password")

        # Authenticate user using email and password
        user = authenticate(request, email=email, password=password)

        print(user,user)

        if user is not None:
            # If user exists and password is correct, log them in
            auth_login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('home')  # Redirect to home page after successful login
        else:
            # If authentication failed
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)  # Logs out the user
    return redirect('/')