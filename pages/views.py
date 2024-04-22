from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.core.mail import send_mail
import random
from django.contrib.auth import logout as auth_logout




#region[White] Home Page

def index(request):
    # if not request.user.is_authenticated:
    #     messages.info(request, 'You are not logged in.')
    return render(request, 'pages/index.html')

#endregion

#region[purple] User Page


def user(request):
    user_info = request.session.get('user_info', None)
    if user_info is None:
        # Handle the case when user is not logged in
        # For example, you can render a different template or return an error message
        return render(request, 'pages/login_pages/login.html')
    else:
        return render(request, 'pages/user.html', {'user_info': user_info})
    

#endregion

#region[Yellow] Register
def register(request):
    if request.method == 'POST':
        # Extract form data
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # Validate form data
        if not all([username, email, password, cpassword]):
            messages.error(request, 'All fields are required.')
            return redirect('register')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already in use.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email address is already in use.')
            return redirect('register')

        # Check if passwords match
        if password != cpassword:
            messages.error(request, 'Passwords do not match. Please try again.')
            return redirect('register')

        
       # Generate verification code
        code = str(random.randint(111111, 999999))


     # Create and save user
        hashed_password = make_password(password)
        user = User.objects.create(
            username=username,
            email=email,
            password=hashed_password,
            first_name=firstname,
            last_name=lastname,
            level='Beginner',
            registration_method='default',
            registration_date=timezone.now(),
            verification_code=code,
            is_verified=False,
        )
        
        subject = "Email Verification Code"
        message = f"Your verification code is: {code}"
        from_email = 'nour3dell@gmail.com'
        to_email = [email]
        try:
            send_mail(subject, message, from_email, to_email, fail_silently=False)
            messages.success(request, f"We've sent a verification code to your email - {email}")
            request.session['email'] = email
            return redirect('verify-code')  # Redirect to the OTP verification page
        except Exception as e:
            messages.error(request, 'Failed while sending code!')
            # Log the exception or handle it appropriately

        messages.success(request, 'Registration successful. Welcome!')
        return redirect('dashboard')

    return render(request, 'pages/login_pages/register.html')
#endregion

#region[Blue] Login

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validate form data
        if not username or not password:
            messages.error(request, 'Both username and password are required.')
            return redirect('login')

        try:
            user = User.objects.get(username=username)

            # Check the provided password against the hashed password in the database
            if check_password(password, user.password):
                if user.is_verified:
                    # messages.success(request, f'Login successful. Welcome back!, {user.username}')
                   # Storing user information in session
                    request.session['user_info'] = {
                        'id':user.id,
                        'username': user.username,
                        'email': user.email,
                        'firstname': user.first_name,
                        'lastname': user.last_name,
                        'is_verified': user.is_verified,
                        'picture': user.picture.url if user.picture else None, 
                        'level':user.level,
                    } 
                    return redirect('dashboard')
                else:
                    messages.info(request, 'Your account is not verified. We have sent a verification code to your email. Please verify it.')
                    request.session['email'] = user.email
                    return redirect('verify-code') 
            else:
                messages.error(request, 'Incorrect email or password!')
        except User.DoesNotExist:
            messages.error(request, "It's look like you're not yet a member! Click on the bottom link to signup.")

    return render(request, 'pages/login_pages/login.html')

#endregion 

#region[Red] Forget Password
def generate_verification_code():
    # Generate a random 6-digit verification code as an integer
    return int(''.join([str(random.randint(0, 9)) for _ in range(6)]))


def forget(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user_profile = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'This email address does not exist!')
            return render(request, 'pages/login_pages/forgetpassword.html')

        # Generate verification code
        code = str(random.randint(111111, 999999))
        user_profile.verification_code = code
        user_profile.save()

        # Send verification email
        subject = "Email Verification Code"
        message = f"Your verification code is: {code}"
        from_email = 'nour3dell@gmail.com'
        to_email = [email]

        try:
            send_mail(subject, message, from_email, to_email, fail_silently=False)
            messages.success(request, f"We've sent a verification code to your email - {email}")
            request.session['email'] = email
            return redirect('reset-code')  # Redirect to the OTP verification page
        except Exception as e:
            messages.error(request, 'Failed while sending code!')
            # Log the exception or handle it appropriately

    return render(request, 'pages/login_pages/forgetpassword.html')

#endregion

#region[Magenta] Reset Code

def check_reset_otp(request):
    if request.method == 'POST':
        otp_values = request.POST.getlist('otp[]')
        if len(otp_values) == 6 and all(value.isdigit() for value in otp_values):
            otp_code = ''.join(otp_values)
       
            try:
                user_profile = User.objects.get(verification_code=otp_code)
                user_profile.verification_code = 0
                user_profile.is_verified = True
                user_profile.save()
                
                request.session['email'] = user_profile.email
                request.session['info'] = "Please create a new password that you don't use on any other site."
                return redirect('new-password')
            except User.DoesNotExist:
                messages.error(request, "You've entered incorrect code!")
        else:
            messages.error(request, "Invalid OTP format.")
    
    return render(request, 'pages/login_pages/reset-code.html')


#endregion
 
#region[Brown] New Password

def new_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password != cpassword:
            messages.error(request, 'Passwords do not match. Please try again.')
            return redirect('new-password')

        # Assuming you have stored the email in the session during OTP verification
        email = request.session.get('email', None)

        if email:
            # Retrieve user profile using email
            user_profile = User.objects.get(email=email)

            # Hash the new password and save it to the user profile
            hashed_password = make_password(password)
            user_profile.password = hashed_password
            user_profile.save()

            # Clear the email from the session
            del request.session['email']

            messages.success(request, 'Password successfully updated. You can now log in with your new password.')
            return redirect('login')

    return render(request, 'pages/login_pages/new-password.html')

#endregion

#region[Pink] Verify Code

def verify_otp(request):
    if request.method == 'POST':
        otp_values = request.POST.getlist('otp[]')
        if len(otp_values) == 6 and all(value.isdigit() for value in otp_values):
            otp_code = ''.join(otp_values)

            try:
                user_profile = User.objects.get(verification_code=otp_code, is_verified=False)
                user_profile.verification_code = 0
                user_profile.is_verified = True
                user_profile.save()

                request.session['email'] = user_profile.email
                messages.success(request, "Registration successful. Welcome!")
                return redirect('user')
            except User.DoesNotExist:
                messages.error(request, "You've entered an incorrect code or the account is already verified.")
        else:
            messages.error(request, "Invalid OTP format.")

    return render(request, 'pages/login_pages/verify-code.html')


#endregion

#region[Gold] Logout

def logout(request):
    auth_logout(request)
    request.session.pop('user_info', None)  
    return redirect('index') 

#endregion

