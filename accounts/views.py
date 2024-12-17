from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login


# Create your views here.




def register(request):
    """Show the registration form"""
    
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        #Check the password
        if password == confirm_password:
            try:
                user = User.objects.create_user(username =username, password=password)
                user.save()
                
                #Display a message
                messages.success(request,"Chambilecho wahenga.")
                return redirect('accounts:register')
            except:
                #Display a message if the above fails
                messages.error(request,"Ina exist")
            else:
                #Display a message saying passwords don't match
                messages.error(request,"Hazimatch")
    return render(request, 'accounts/register.html')

#register 
def login_page(request):
    
    """Log in function"""
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username = username, password=password)
    
     #Check if the user exists
        if user is not None:
            login(request, user)
        messages.success(request,'you are logged in')
        return redirect('accounts:home')
       
    else:
           messages.error(request , 'Invalid credentials')
        
    return render(request,'accounts/login.html')