from django.shortcuts import get_object_or_404, render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, logout, authenticate

from profiling.models import UserProfile
from .models import Payment

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.contrib.auth.models import User
from profiling.models import UserProfile

def initiate_payment(request: HttpRequest, fee) -> HttpResponse:
    # if request.method == "POST":
    amount = 100
    # payer = request.POST['for']
    # state_code = request.POST['state_code']
    fee_type= request.POST.get('fee')
    owner = 'Myself'
    # state_ID= request.POST.get('state')


    if owner == 'yself':
        print('if')
        profile = request.user.profile
        email = request.user.email
        
        state_ID = UserProfile.objects.filter(state_code=profile.state_code)
        state_ID = 'hehsjrj'

    elif owner == 'Someone Else':
        print('elif')
        if UserProfile.objects.filter(state_code=state_ID).exists():
            user=UserProfile.objects.get(state_code=state_ID)
            name= f'{user.first_name} {user.last_name}' 
    else:
        print('else')
        messages.error(
            request,
            "please check again state id does not exist",
        )
        # return render(request, "connector.html", {'fee':fee_type})
    
    print('==============================================================================================')
    print(amount, fee, state_ID, profile.first_name)

    pay = Payment.objects.create(amount=amount,fee_type=fee,state_ID=state_ID,profile=profile)
    if pay:
        return render(request, 'receipt.html', {'payment': pay, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    # pays = Payment.objects.get(ref=pay.ref)
    return render(request, 'index.html', {'payment': pay, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY, 'fee':fee})

    return render(request, "connector.html",{'fee':fee})

def requestLogin(request, state_code):
    profile = UserProfile.objects.filter(state_code=state_code).first()
    user = User.objects.filter(profile=profile).first()
    
    # print(user)
    # print(profile)
    # if request.method == 'POST':
    if user is not None:
        login(request, user)
        print(user)
        # return redirect('general')
    else:
        messages.error(request,'Invalid user')

    if request.method == 'POST':
        amount = 10000
        payer = request.POST['payment']
        fee = request.POST['fee']

        print(payer)
        if payer == 'myself':
            print('if')
            profile = request.user.profile
            email = request.user.email
            
            
            state_ID = UserProfile.objects.filter(state_code=profile.state_code).first()
            if not state_ID:
                state_ID = 'hehsjrj'

        elif payer == 'Someone Else':
            print('elif')
            if UserProfile.objects.filter(state_code=state_ID).exists():
                user=UserProfile.objects.get(state_code=state_ID)
                name= f'{user.first_name} {user.last_name}' 
        else:
            print('else')
            messages.error(
                request,
                "please check again state id does not exist",
            )
            return render(request, "indexing.html",)
        
        print(amount, fee, state_ID, profile.first_name)

        pay = Payment.objects.create(amount=amount,fee_type=fee,state_ID=state_ID,profile=profile,email=email)
    
        return render(request, 'invoice.html', {'payment': pay, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})

    return render(request, 'indexing.html', {'profile': profile})

def payment(request):
    return render(request, 'payments.html')

def licences(request):
    return render(request, 'licences.html',)


def fines(request):
    return render(request, 'fines.html')


def fees(request):
    return render(request, 'fees.html')


def sales(request):
    return render(request, 'sales.html')


def services(request):
    return render(request, 'services.html')

def connect(request,fee):
    print(fee)
    d=False
    if str(fee) == 'Illegal Trading':
        d=True
    return render(request, 'connector.html', {'fee':fee,'d':d})


def verify_payment(request, ref: str):
    trxref = request.GET["trxref"]
    if trxref != ref:
        messages.error(
            request,
            "The transaction reference passed was different from the actual reference. Please do not modify data during transactions",
        )
    payment: Payment = get_object_or_404(Payment, ref=ref)
    
    if payment.verify_payment():
        payment.status = 'paid'
        payment.save()
        messages.success(
            request, f"Payment Completed Successfully, NGN #{payment.amount}."
        )
        # user = UserProfile.objects.filter(state_code = payment.state_ID).only('first_name', 'email')
        template = get_template('invoicetwo.html')
        data = {
            'order_id': payment.ref,
            'STATE_ID': payment.state_ID,
            'user_email': request.user.email, #user.email
            'date': str(payment.date_created),
            'name': payment.name, #user.name
            'fee': payment.fee_type,
            'amount': payment.amount,
        }
        html  = template.render(data)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result), #link_callback=fetch_resources)
        pdf = result.getvalue()
        filename = 'Value_' + data['fee'] + '.pdf'

        mail_subject = 'Trascation File'
        message = render_to_string('emailinvoice.html', {
            'orderid': payment.ref,
             'name': payment.name, #user.name
            'fee': payment.fee_type,
            'amount': payment.amount,
            'stateid' : payment.state_ID,
        })
        to_email = ['government1.irs@gmail.com', request.user.email] #user.email
        context_dict = {
            'user': f'{request.user.profile.first_name} {request.user.profile.last_name}',
            'orderid': payment.ref,
            'amount': payment.amount,
            'fee': payment.fee_type,
            'stateid' : payment.state_ID,
            'to_email' : to_email
        }
        template = get_template('emailinvoice.html')
        message  = template.render(context_dict)
        

        # I use this loop because I dont want the two parties to see each other's email
        for email in to_email:
            email = EmailMultiAlternatives(
                subject=mail_subject,
                body='This is your document',
                from_email =settings.EMAIL_HOST_USER,
                to = [email]
            )
            email.attach_alternative(message, "text/html")
            email.attach(filename, pdf, 'application/pdf')
            email.send(fail_silently=False)
            print('success')
  
    else:
        messages.warning(request, "Sorry, your payment could not be confirmed.")
    return redirect('payments:request', request.user.profile.state_code)


def logoutuser(request):
    logout(request)
    return redirect('landing')