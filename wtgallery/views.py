# Create your views here.

import os
from django.contrib.auth.models import User, AnonymousUser
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from pixzium import settings
from .forms import ImageForm, SignUpForm, LoginForm, VideoForm, MusicForm
from django.contrib import messages
from .models import Image, Video, Music, Profile, UserFollowing


def index(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    return redirect('/dashboard')
                return redirect("/")
            else:
                msg = "Username or Password Doesn't match"
        else:
            msg = 'Error validating the form'
    # current_user = request.user

    # current_user = request.user if type(request.user) is not AnonymousUser else None
    # profileRecord = Profile.objects.get_or_create(user=current_user)[0]
    # print(profileRecord.profile_pic)
    # image = Image.objects.filter(user__user__username__exact=profileRecord)

    portfolio = Image.objects.all().order_by('-uploaded_at').filter(status__exact='A')
    common_tags = Image.tags.most_common()[:4]
    context = {
        "form": form,
        "msg": msg,
        # "profileRecord": profileRecord,
        "portfolios": portfolio,
        "common_tags": common_tags
    }
    return render(request, "index.html", context)


# class IndexView(generic.ListView):
#     model = Image
#     context_object_name = 'portfolios'
#     template_name = 'index.html'
#
#     def get_context_data(self, **kwargs):
#         form = LoginForm(request.POST or None)
#         msg = None
#         if request.method == "POST":
#
#             if form.is_valid():
#                 username = form.cleaned_data.get("username")
#                 password = form.cleaned_data.get("password1")
#
#                 user = authenticate(username=username, password=password)
#                 if user is not None:
#                     login(request, user)
#                     if request.user.is_superuser:
#                         return redirect('/dashb')
#                     return redirect("/")
#
#                 else:
#                     msg = "Username or Password Doesn't match"
#             else:
#                 msg = 'Error validating the form'
#         context = super(IndexView, self).get_context_data(**kwargs)
#         context.update({
#             "form": form,
#             "msg": msg,
#             'common_tags': Image.tags.most_common()[:4],
#         })
#         return context
#
#     def get_queryset(self):
#         return Image.objects.order_by('-uploaded_at')


@login_required
def my_account(request):
    current_user = request.user
    profileRecord = Profile.objects.get_or_create(user=current_user)[0]
    print(profileRecord)
    image = Image.objects.filter(user__user__username__exact=profileRecord)
    video = Video.objects.filter(user__user__username__exact=profileRecord)
    music = Music.objects.filter(user__user__username__exact=profileRecord)

    if request.method == "POST":
        # Message for the team
        if 'btnContact' in request.POST:
            message = request.POST.get('message')
            detail = "Name : " + profileRecord.user.username + "\n" + "Email : " + profileRecord.user.email + "\n" + "Message : " + message
            send_mail("Complaint or Suggestion", detail, "Pixzium", ["yadavrajneesh999@gmail.com"])
            messages.success(request, 'Message Submitted Successfully. Our Team will reply you ASAP.')
        # User Profile Update(Basic Info)
        if 'btnSave' in request.POST:
            FirstName = request.POST.get("firstname", None)
            LastName = request.POST.get("lastname", None)
            Mobile = request.POST.get("mobile", 000)
            Address = request.POST.get("address", None)
            City = request.POST.get("city", None)
            State = request.POST.get("state", None)
            Country = request.POST.get("country", None)
            Pincode = request.POST.get("pincode", 000)

            current_user.first_name = FirstName
            current_user.last_name = LastName
            profileRecord.mobile = Mobile
            profileRecord.address = Address
            profileRecord.city = City
            profileRecord.state = State
            profileRecord.country = Country
            profileRecord.pincode = Pincode

            profileRecord.save()
            current_user.save()
            messages.success(request, 'Your Profile is successfully Uploaded')
        # User Public Profile Update
        if 'btnPPSave' in request.POST:
            # user_id = request.POST.get("user_id", None)
            if request.FILES:
                logo = request.FILES['profielogo']
                profileRecord.profile_pic = logo
            heading = request.POST.get("heading")
            message = request.POST.get("message")
            if request.POST.get("freelance") is None:
                profileRecord.freelance = False
            else:
                profileRecord.freelance = True

            profileRecord.profileheading = heading
            profileRecord.description = message
            profileRecord.save()
            messages.success(request, 'Your Payment Profile is successfully Uploaded')
        # User Social Links Update
        if 'btnSMSave' in request.POST:
            facebook = request.POST.get("facebook")
            twitter = request.POST.get("twitter")
            instagram = request.POST.get("instagram")
            youtube = request.POST.get("youtube")
            pinterest = request.POST.get("pinterest")

            profileRecord.facebook = facebook
            profileRecord.twitter = twitter
            profileRecord.instagram = instagram
            profileRecord.youtube = youtube
            profileRecord.pinterest = pinterest
            profileRecord.save()
            messages.success(request, 'Your Social Media Profile is successfully Uploaded')
        # User Payment links
        if 'btnPLSave' in request.POST:
            razorpay = request.POST.get("razorpay", None)
            paypal = request.POST.get("paypal", None)

            profileRecord.razorpay = razorpay
            profileRecord.paypal = paypal
            profileRecord.save()
            messages.success(request, 'Your Payment Link is successfully Uploaded')

        return HttpResponseRedirect(reverse('my_account'))
    context = {'profile': profileRecord,
               'image': image,
               'video': video,
               'music': music,
               'followers': '',}
    return render(request, "dashboard.html", context)


@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")


@login_required
def approval(request):
    if request.method == 'POST':
        pic_id = int(request.POST.get("pic_id"))
        status = str(request.POST.get("status"))
        user_id = request.POST.get("user_id")
        user = User.objects.get(id=user_id)
        u_email = user.email
        print(u_email)
        print(user)
        if status == "A":
            sts = Image.objects.get(id=pic_id)
            sts.status = status
            sts.save()
        else:
            sts = Image.objects.filter(id=pic_id)
            subject = 'Waring Message for Uploaded Image from Pixzium'
            message = f'Hi {user}, we have found Inappropriate Image. This is a waring Email, Please Follow ' \
                      f'Our Company Guideline. '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [u_email, ]
            send_mail(subject, message, email_from, recipient_list)
            sts.delete()
            messages.success(request, 'Record Deleted Successfully.')

    portfolio = Image.objects.all().filter(status__exact='P')
    context = {"portfolios": portfolio}
    return render(request, "dashboard/gallery.html", context)


@login_required
def pow(request):
    return render(request, "pow.html")


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        print(name)
        email = request.POST.get('email')
        print(email)
        subject = request.POST.get('subject')
        print(subject)
        message = request.POST.get('message')
        print(message)
        detail = "Name : " + name + "\n" + "Email : " + email + "\n" + "Message : " + message
        send_mail(subject, detail, email, ["yadavrajneesh999@gmail.com"])
        messages.success(request, 'Message Send Successfully.')
    return render(request, "contact.html")


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, "signup.html", {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    return redirect('/dashb')
                return redirect("/")

            else:
                msg = "Username or Password Doesn't match"

        else:
            msg = 'Error validating the form'
    return render(request, "login.html", {"form": form, "msg": msg})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.filter(user=user.id).first()
    image = Image.objects.filter(user=profile)
    video = Video.objects.filter(user=profile)
    music = Music.objects.filter(user=profile)
    context = {'profile': profile, 'image': image, 'video': video, 'music': music}
    return render(request, 'profile.html', context)


def photo_detail(request, id):
    image = get_object_or_404(Image, id=id)
    print(image)
    tagsList = []
    for tag in image.tags.all():
        tagsList.append(tag.name)
    print(tagsList)
    return render(request, 'photo_detail.html', {'image': image, 'tagsList': tagsList})


def image(request):
    portfolio = Image.objects.all().order_by('-uploaded_at')
    context = {"portfolio": portfolio}
    return render(request, "images.html", context)


def video(request):
    portfolio = Video.objects.all().order_by('-uploaded_at')
    print(portfolio)
    context = {"videooj": portfolio}
    return render(request, "video.html", context)


def music(request):
    portfolio = Music.objects.all().order_by('-uploaded_at')
    print(portfolio)
    context = {"portfolio": portfolio}
    return render(request, "music.html", context)


@login_required
def upload(request):
    if request.method == 'POST':
        image = ImageForm(request.POST, request.FILES)
        video = VideoForm(request.POST, request.FILES)
        music = MusicForm(request.POST, request.FILES)

        ext = os.path.splitext(str(request.FILES['file']))[-1].lower()
        print(ext)

        if ext == ".mp4":
            print("mp4 file!")

            if video.is_valid:
                # form.save()
                fs = video.save(commit=False)
                fs.user = Profile.objects.get(user=request.user)
                fs.save()
                video.save_m2m()
                messages.success(request, 'Video successfully Uploaded, It will be Visible after reviewed by our Team.')

                return redirect('upload')

        elif ext == ".mkv":
            print("mkv file!")

            if video.is_valid:
                # form.save()
                fs = video.save(commit=False)
                fs.user = Profile.objects.get(user=request.user)
                fs.save()
                video.save_m2m()
                messages.success(request, 'Video successfully Uploaded, It will be Visible after reviewed by our Team.')

                return redirect('upload')

        elif ext == ".mov":
            print("mov file!")

            if video.is_valid:
                # form.save()
                fs = video.save(commit=False)
                fs.user = Profile.objects.get(user=request.user)
                fs.save()
                video.save_m2m()
                messages.success(request, 'Video successfully Uploaded, It will be Visible after reviewed by our Team.')

                return redirect('upload')

        elif ext == ".mp3":
            print("mp3 file!")

            if music.is_valid:
                # form.save()
                fs = music.save(commit=False)
                fs.user = Profile.objects.get(user=request.user)
                fs.save()
                music.save_m2m()
                messages.success(request, 'Music Successfully Uploaded, It will be Visible after reviewed by our Team.')

                return redirect('upload')

        elif ext == ".png" or ".jpg" or ".jpeg":
            print("image file!")

            if image.is_valid():
                # if nude.is_nude(request.FILES['file']):
                #     messages.warning(request, 'Inappropriate image detected, This is against our company policy !!')
                # else:
                # form.save()
                fs = image.save(commit=False)
                fs.user = Profile.objects.get(user=request.user)
                fs.save()
                image.save_m2m()
                messages.success(request, 'Image Successfully Uploaded, It will be Visible after reviewed by our Team.')

                return redirect('upload')

        else:
            print("Unknown file format.")
            messages.warning(request, 'Unknown File Format !!')

        # if image.is_valid() or video.is_valid:
        #
        #     if nude.is_nude(request.FILES['image']):
        #         messages.warning(request, 'Inappropriate image detected, This is against our company policy !!')
        #     else:
        #         # form.save()
        #         fs = image.save(commit=False)
        #         fs.user = request.user
        #         fs.save()
        #         messages.success(request, 'Image inserted successfully.')
        #
        #     return redirect('upload')
    else:
        form = ImageForm() or VideoForm() or MusicForm()
    return render(request, 'upload.html', {'form': form})


class SearchResultsView(ListView):
    model = Image
    template_name = 'search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        st = self.request.GET.get('searchType')

        print(st)
        if st == 'image':
            object_list = Image.objects.filter(
                Q(title__icontains=query) | Q(file__icontains=query) | Q(tags__name__icontains=query))
            return object_list

        elif st == 'video':
            object_list = Video.objects.filter(
                Q(title__icontains=query) | Q(file__icontains=query) | Q(tags__name__icontains=query))
            return object_list

        else:
            print("HERE Goes the Blank Search")
            object_list = Image.objects.filter(
                Q(title__icontains=query) | Q(file__icontains=query) | Q(
                    tags__name__icontains=query))
            return object_list


def save_views(req):
    if req.method == "GET":
        pk = req.GET.get("obj")
        obj = Image.objects.get(pk=pk)
        obj.views += 1
        obj.save()

        print("inside save view")

        return JsonResponse({'status': obj.views})
    pass


def save_video_views(req):
    if req.method == 'GET':
        pk = req.GET.get("obj")
        obj = Video.objects.get(pk=pk)
        obj.views += 1
        obj.save()

        print("inside save view")

        return JsonResponse({'status': obj.views})
    pass


def music_views(req):
    if req.method == 'GET':
        pk = req.GET.get("obj")
        obj = Music.objects.get(pk=pk)
        obj.views += 1
        obj.save()

    print("inside save view")

    return JsonResponse({'status': obj.views})
    pass


def count_likes(req):
    if req.method == 'GET':
        id = req.GET.get('post_id')
        post = get_object_or_404(Image, id=id)

        liked = False
        if post.likes.filter(id=req.user.id).exists():
            post.likes.remove(req.user)

        else:
            liked = True
            post.likes.add(req.user)

        total_likes = post.number_of_likes
        return JsonResponse({'liked': liked, 'total_likes': total_likes, 'id': id})


def save_music_view(req):
    if req.method == 'GET':
        pk = req.GET.get("obj")
        obj = Music.objects.get(pk=pk)
        obj.views += 1
        obj.save()
        print('inside music views')
        return JsonResponse({'status': obj.views})
    pass


def count_downloads(req):
    if req.method == "GET":
        pk = req.GET.get("obj")
        obj = Image.objects.get(pk=pk)
        obj.total_downloads += 1
        obj.save()

        print("inside save view")

    return JsonResponse({'status': obj.total_downloads})


def sitemap(request):
    return render(request, "sitemap.xml")


def subscription(request):
    return render(request, "pricing.html")


def about(request):
    return render(request, "subscription.html")
