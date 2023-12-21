from django.shortcuts import render, redirect
# from profiling.models import *
# from payment.models import Payment
from citizens.models import Profile, NextOfKin
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def loginPage(request):

    page = 'login'

    if request.user.is_authenticated and request.user.is_staff:
        return redirect('adminpanel')

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username = username)
            print(password,username)

        except:
            messages.error(request, "User does not exist.")
            print('user doest not exist')

        user = authenticate(username = username, password = password)
        print(user)

        if user is not None :
            login(request, user)
            print("hhhhh")
            return redirect('adminpanel')

        else:
            messages.error(request, "You are not an admin.")
            print('something went wrong')

    context = {'page': page,}
    return render(request, 'adminpanel/index.html', context)


@csrf_exempt
def profile(request):

    if request.user.is_authenticated and request.user.is_staff:
        return redirect('adminpanel')
    profile = Profile.objects.filter(user = request.user).first()
    context = {'profile': profile}
    return render(request,'adminpanel/profiles.html', context)

def searchForProfile(request):


    search_query = request.GET.get('search','')
    # profileExist = Profile.objects.distinct().filter(
    # Q(state_code__icontains=search_query) |
    # Q(phone__icontains=search_query) |
    # Q(user__username__icontains=search_query)
    # ).exists()
    # if profileExist:
    #     return redirect("getrofile")
    profile = Profile.objects.distinct().filter(
    Q(health_code__icontains=search_query) |
    Q(phone__icontains=search_query) |
    Q(user__username__icontains=search_query)
    ).first()
    # if profile:
    #     nextofkin = NextOfKin.objects.filter(profile=profile).first()
    #     # print(profile.first_name)
    return profile, search_query

def getProfile(request):
    # return render(request, 'adminpanel/overview.html')
    page='home'
    if not request.user.is_authenticated:
        return redirect('login')
    query=request.GET.get("search",'')
    if query=='':
        return render(request, 'adminpanel/overview.html')

    profile, search_query = searchForProfile(request)
    nextofkin = NextOfKin.objects.filter(profile=profile).first()

    # bankpermission = False
    # healthpermission = False
    # securitypermission = False

    # if request.user.profile.role.title in ['General', 'Finance']:
    #     bankpermission = True
    # if request.user.profile.role.title in ['General', 'Health']:
    #     healthpermission = True
    # if request.user.profile.role.title in ['General', 'Security']:
    #     securitypermission = True


    context = {'profile': profile, 'search_query': search_query, 'page':page, 'nextofkin':nextofkin, 
               'bankpermission': True, 'healthpermission': True, 'securitypermission': True}
    print(context)
    return render (request,'adminpanel/profiles.html', context)



def logoutuser(request):
    logout(request)
    return redirect('login')

# def searchForTransaction(request):
#     search_query = ""   # so that nothing is return from the query

    
#     if request.GET.get('search'):
#         search_query = request.GET.get('search')

#     transactions = Payment.objects.distinct().filter(
#     # Q(owner__icontains=search_query) |
#     Q(ref__icontains=search_query) |
#     Q(fee_type__icontains=search_query)
#     )

#     paid_transactions = Payment.objects.distinct().filter(
#     # Q(owner__icontains=search_query) |
#     Q(ref__icontains=search_query) |
#     Q(fee_type__icontains=search_query)
#     ).filter(status = 'completed')

#     pending_transactions = Payment.objects.distinct().filter(
#     # Q(owner__icontains=search_query) |
#     Q(ref__icontains=search_query) |
#     Q(fee_type__icontains=search_query)
#     ).filter(status = 'pending')

#     failed_transactions = Payment.objects.distinct().filter(
#     # Q(owner__icontains=search_query) |
#     Q(ref__icontains=search_query) |
#     Q(fee_type__icontains=search_query)
#     ).filter(status = 'failed')

#     return transactions, search_query, pending_transactions, paid_transactions, failed_transactions

# def getTransaction(request):
#     page = 'transaction'
#     if not request.user.is_staff:
#         return redirect('login')
    
 
#     # houses = House.objects.all()
#     transactions, search_query, pending_transactions, paid_transactions, failed_transactions = searchForTransaction(request)
 
#     context = {'transactions': transactions, 'search_query': search_query, 'pending_transactions': pending_transactions,'paid_transactions': paid_transactions
#                ,'failed_transactions': failed_transactions, 'page':page}
#     return render (request,'adminpanel/index.html',context)





# def getTransactionsApi(request):
#     search_term = request.GET.get('search', '')
#     current_page = request.GET.get('page', 1)
#     params = {'search': search_term, 'page':current_page}

#     res = requests.get(url='http://127.0.0.1:8002/api/gettransactions/', params=params)

#     if request.user.profile.role.title == 'Health':
#         return redirect('usertransaction')
#     if res.status_code == 200:
#         transactions = res.json()
    
#     # if not 
#     current_page = request.GET.get('page', 1)
#     current_page = int(current_page)
#     total = math.ceil(int(transactions['count'])/10)

    # print(page)
    # print(transactions['paginator'])
    # try:
    #     next = transactions['next'][(str(transactions['next']).find('='))+1:]
    # except:
    #     next = None
    # try:
    #     previous = transactions['previous'][(str(transactions['previous']).find('='))+1:]
    # except:
    #     previous = "1"


    # leftIndex = (int(current_page) - 4)

    # if leftIndex < 1:
    #     leftIndex = 1

    # rightIndex = (int(current_page) + 5)

    # if rightIndex > total:
    #     rightIndex = total + 1

    # print(current_page, leftIndex, rightIndex)
    # custom_range = range(leftIndex, rightIndex)

    # # print('next; ', next)
    # context = {'transactions': transactions, 'next': next, 'previous':previous, 'custom_range': custom_range, 'current_page': current_page}
    # return render(request, 'adminpanel/orderapi.html', context)
        # print(transaction) 

# def userTransaction(request):
#     search_term = request.GET.get('search', '')
#     current_page = request.GET.get('page', 1)
#     params = {'search': search_term, 'page':current_page}

#     res = requests.get(url='http://127.0.0.1:8002/api/usertransaction/{}'.format('YA08107095017'), params=params)
#     if res.status_code == 200:
#         transactions = res.json()
    
#     # if not 
#     current_page = request.GET.get('page', 1)
#     current_page = int(current_page)
#     total = math.ceil(int(transactions['count'])/10)

    # print(page)
    # print(transactions['paginator'])
    # try:
    #     next = transactions['next'][(str(transactions['next']).find('='))+1:]
    # except:
    #     next = None
    # try:
    #     previous = transactions['previous'][(str(transactions['previous']).find('='))+1:]
    # except:
    #     previous = "1"


    # leftIndex = (int(current_page) - 4)

    # if leftIndex < 1:
    #     leftIndex = 1

    # rightIndex = (int(current_page) + 5)

    # if rightIndex > total:
    #     rightIndex = total + 1

    # print(current_page, leftIndex, rightIndex)
    # custom_range = range(leftIndex, rightIndex)

    # # print('next; ', next)
    # context = {'transactions': transactions, 'next': next, 'previous':previous, 'custom_range': custom_range, 'current_page': current_page}
    # return render(request, 'adminpanel/usertransaction.html', context)
        # print(transaction)


