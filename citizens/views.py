from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
import cv2
from django.conf import settings


def register(request):
    if request.user.is_authenticated:
        return redirect('adminpanel')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error('password is not matching')
            return redirect('register')


        if User.objects.filter(email=email).exists():
            messages.error('email already exist')
            return redirect('register')

        user = User.objects.create(
            email = email,
            username = email,
            password = password,
        )

        login(request, user)
        return redirect('personaldetail')
    

    return render(request, 'signup.html')

def personalDetails(request):
    user = request.user

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        middle_name = request.POST['middle_name']
        phone = request.POST['phone']
        nin = request.POST['nin']
        dob = request.POST['dob']
        gender = request.POST['gender']
        marital_status = request.POST['marital']
        occupation = request.POST['occupation']
        state_of_origin = request.POST['state_of_origin']
        address = request.POST['address']

        profile = Profile.objects.create(
            user = user,
            first_name = first_name,
            last_name = last_name,
            middle_name = middle_name,
            phone = phone,
            nin = nin,
            dob = dob,
            gender = gender,
            marital_status = marital_status,
            occupation = occupation,
            state_of_origin = state_of_origin,
            address = address,
            # first_name = first_name,
        )
    
        # first_name = request.POST['first_name']
        # first_name = request.POST['first_name']

        return redirect('nextofkin')
    return render(request, 'personaldetails.html')
    

def nextofKin(request):
    if request.method == 'POST':
        name = request.POST['name']
        relationship = request.POST['relationship']
        phone = request.POST['phone']
        address = request.POST['address']
        
        rel_name = request.POST['rel_name']
        rel_relationship = request.POST['rel_relationship']
        rel_phone = request.POST['rel_phone']

        rel_name1 = request.POST['rel_name1']
        rel_relationship1 = request.POST['rel_relationship1']
        rel_phone1 = request.POST['rel_phone1']
        
        NextOfKin.objects.create(
            profile = request.user.profile,
            name=name,
            relationship=relationship,
            phone=phone,
            address=address
        )

        return redirect('healthinfo')

        # Relatives.objects.bulk_create(
        #     profile = request.user.profile
        # )
    
    return render(request, 'nok.html')


def healthInfo(request):
    profile = request.user.profile

    if request.method == 'POST':
        blood_group = request.POST['blood_group']
        genotype = request.POST['genotype']

        profile.bloodgroup = blood_group
        profile.genotype = genotype
        profile.save()

        return redirect('face')


    return render(request, 'blood.html')
    
        
def face(request):
    return render(request, 'face.html')


def finger(request):
    return render(request, 'finger.html')

def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.filter(
                Q(profile__state_code__icontains=username) |
                Q(profile__phone__icontains=username) |
                Q(user__email__icontains=username)).first()
            
            username = user.username
            # user = User.objects.filter(username = username)
            # user = User.objects.get(username = username)
            # user = User.objects.get(username = username)

        except:
            messages.error(request, "User does not exist.")
            print('user doest not exist')

        user = authenticate(username = username, password = password)


        if user is not None:
            login(request, user)
            return redirect('profile')
            # return redirect(request.GET['next'] if 'next' in request.GET else 'profile')

        else:
            messages.error(request, "Something went wrong.")
            print('something went wrong')

    context = {'page': page,}
    return render(request, 'index.html', context)


# Create your views here.
def profile(request):
    # profile = Profile.objects.prefetch_related('nextofkin').filter(user = request.user).first() #prefetch related
    profile = Profile.objects.filter(user = request.user).first() #prefetch related
    nextofkin = NextOfKin.objects.filter(profile=profile).first()
    print(profile.bloodgroup)
    context = {'profile': profile, 'nextofkin': nextofkin}
    return render(request, 'profile.html', context)

def searchForProfile(request):

    search_query = "?"   # so that nothing is return from the query at first

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    profile = Profile.objects.distinct().filter(
    Q(state_code__icontains=search_query) |
    Q(phone__icontains=search_query) |
    Q(user__username__icontains=search_query)
    ).first()
    # if profile:
    #     nextofkin = NextOfKin.objects.filter(profile=profile).first()
    #     # print(profile.first_name)
    return profile, search_query

def getProfile(request):
    page='home'
    if not request.user.is_authenticated:
        return redirect('login')
    profile, search_query = searchForProfile(request)
    nextofkin = NextOfKin.objects.filter(profile=profile).first()
    bank = Bank.objects.filter(profile=profile).first()

    bankpermission = False
    healthpermission = False
    securitypermission = False

    if request.user.profile.role.title in ['General', 'Finance']:
        bankpermission = True
    if request.user.profile.role.title in ['General', 'Health']:
        healthpermission = True
    if request.user.profile.role.title in ['General', 'Security']:
        securitypermission = True


    context = {'profile': profile, 'search_query': search_query, 'page':page, 'nextofkin':nextofkin, 'bank':bank,
               'bankpermission': bankpermission, 'healthpermission': healthpermission, 'securitypermission': securitypermission}
    return render (request,'adminpanel/index.html', context)


def searchForTransaction(request):
    search_query = ""   # so that nothing is return from the query

    if request.GET.get('search'):
        search_query = request.GET.get('search')

    transactions = Payment.objects.distinct().filter(
    # Q(owner__icontains=search_query) |
    Q(ref__icontains=search_query) |
    Q(fee_type__icontains=search_query)
    )

    paid_transactions = Payment.objects.distinct().filter(
    # Q(owner__icontains=search_query) |
    Q(ref__icontains=search_query) |
    Q(fee_type__icontains=search_query)
    ).filter(status = 'completed')

    pending_transactions = Payment.objects.distinct().filter(
    # Q(owner__icontains=search_query) |
    Q(ref__icontains=search_query) |
    Q(fee_type__icontains=search_query)
    ).filter(status = 'pending')

    failed_transactions = Payment.objects.distinct().filter(
    # Q(owner__icontains=search_query) |
    Q(ref__icontains=search_query) |
    Q(fee_type__icontains=search_query)
    ).filter(status = 'failed')

    return transactions, search_query, pending_transactions, paid_transactions, failed_transactions

def getTransaction(request):
    page = 'transaction'
    if not request.user.is_staff:
        return redirect('login')
    
 
    # houses = House.objects.all()
    transactions, search_query, pending_transactions, paid_transactions, failed_transactions = searchForTransaction(request)
 
    context = {'transactions': transactions, 'search_query': search_query, 'pending_transactions': pending_transactions,'paid_transactions': paid_transactions
               ,'failed_transactions': failed_transactions, 'page':page}
    return render (request,'adminpanel/index.html',context)




def logoutuser(request):
    logout(request)
    return redirect('login')


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


def scan_image(request):
    print(cv2.__version__)
    # Detect face
    #Creating a cascade image classifier
    faceDetect = cv2.CascadeClassifier(settings.BASE_DIR+'/ml/haarcascade_frontalface_default.xml')
    #camture images from the webcam and process and detect the face
    # takes video capture id, for webcam most of the time its 0.
    cam = cv2.VideoCapture(0)

    # Our identifier
    # We will put the id here and we will store the id with a face, so that later we can identify whose face it is
    id = "4444"
    # Our dataset naming counter
    sampleNum = 0
    # Capturing the faces one by one and detect the faces and showing it on the window
    while(True):
        # Capturing the image
        #cam.read will return the status variable and the captured colored image
        ret, img = cam.read()
        #the returned img is a colored image but for the classifier to work we need a greyscale image
        #to convert
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #To store the faces
        #This will detect all the images in the current frame, and it will return the coordinates of the faces
        #Takes in image and some other parameter for accurate result
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        #In above 'faces' variable there can be multiple faces so we have to get each and every face and draw a rectangle around it.
        for(x,y,w,h) in faces:
            # Whenever the program captures the face, we will write that is a folder
            # Before capturing the face, we need to tell the script whose face it is
            # For that we will need an identifier, here we call it id
            # So now we captured a face, we need to write it in a file
            sampleNum = sampleNum+1
            # Saving the image dataset, but only the face part, cropping the rest
            cv2.imwrite(settings.BASE_DIR+'/ml/dataset/user.'+str(id)+'.'+str(sampleNum)+'.jpg', gray[y:y+h,x:x+w])
            # @params the initial point of the rectangle will be x,y and
            # @params end point will be x+width and y+height
            # @params along with color of the rectangle
            # @params thickness of the rectangle
            cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)
            # Before continuing to the next loop, I want to give it a little pause
            # waitKey of 100 millisecond
            cv2.waitKey(250)

        #Showing the image in another window
        #Creates a window with window name "Face" and with the image img
        cv2.imshow("Face",img)
        #Before closing it we need to give a wait command, otherwise the open cv wont work
        # @params with the millisecond of delay 1
        cv2.waitKey(1)
        #To get out of the loop
        if(sampleNum>35):
            break
    #releasing the cam
    cam.release()
    # destroying all the windows
    cv2.destroyAllWindows()

    return redirect('/')
