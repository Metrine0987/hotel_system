import requests
import json

from django.http import HttpResponse
from myapp.credentials import LipanaMpesaPpassword, MpesaAccessToken
# Import the model

from django.shortcuts import render,redirect,get_object_or_404
from django.core.files.storage import FileSystemStorage
from .models import UploadedImage

#import models
from .models import Contact
# Create your views here.

#Import the login_required
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'index.html')


def portfolio(request):
    return render(request, 'portfolio.html')

def service(request):
    return render(request, 'service.html')

def about(request):
    return render(request,'about.html')

def team(request):
    return render(request, 'team.html')

@login_required(login_url='accounts:login')
def contact(request):
   

    """ To push data to db """
    #check if it is a POST request

    if request.method =='POST':
        #Create a variable to pick the input fields
        contact = Contact(
            #input fields
            name = request.POST['name'],
            email = request.POST['email'],
            subject = request.POST['subject'],
            message = request.POST['message'],
        )
        
        #save the variables
        contact.save()
        #redirect to a page
        return redirect('myapp:home')
    else:
        
        return render(request,'contact.html')

#Retrieve all appointments
def retrieve_contact(request):
    """Retrieve/fetch all contacts"""
    #create a variable to store these contacts
    contact = Contact.objects.all()
    context = {
        'contact':contact
    }
    return render(request, 'show_contact.html',context)


#Delete
def delete_contact (request,id):
    """ Deleting """
    contact = Contact.objects.get(id=id) #fetch a particular contact by its ID
    contact.delete() # actual action of deleting
    return redirect('myapp:show_contact') #just remain on the same page

#update
def update_contact(request,contact_id):
    """Update the query"""
    
    contact = get_object_or_404(Contact, id= contact_id)
    context = {'contact': contact}
    
    #put the condition for the form to update
    if request.method == 'POST':
        contact.name = request.POST.get('name')
        contact.email = request.POST.get('email')
        contact.subject = request.POST.get('subject')
        contact.message = request.POST.get('message')
        contact.save()

        return redirect('myapp:show_contact')
        
    else:
        return render(request,'update_contact.html',context)
       
      
def upload_image(request):
    if request.method == 'POST':
        #Retrieve data from the form
        title = request.POST['title']
        uploaded_file =request.FILES['image']
        
        #save the file using FileSystemStorage
        fs=FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)
        
        #Save file information to the database
        image = UploadedImage.objects.create(title=title, image=filename)
        image.save()
        
        return render(request,'upload_success.html',{'file_url':
            file_url})
    return render(request,'upload_image.html')
       
       
       #Adding the mpesa functionalites
       #Display the payment form
def pay(request):
   """ Renders the form to pay """
   return render(request, 'pay.html')


# Generate the ID of the transaction
def token(request):
    """ Generates the ID of the transaction """
    consumer_key = 'qvQFfRUmIIMKcLutXyGEdAbkKtYN7RzIjVKiMz8Ma94qQt4q'
    consumer_secret = 'HRSVAAGk1AEG4ZATjzWmqYSTpGluFG6Erf8gRab85NEepozIGSmTPmR6k2Cu9Ivr'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})


# Send the stk push
def stk(request):
    """ Sends the stk push prompt """
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "eMobilis",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")