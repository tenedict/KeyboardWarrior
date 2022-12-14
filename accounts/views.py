import requests
from django.shortcuts import render, redirect
from .forms import CreateUser
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login as my_login, logout as my_logout
from django.contrib import messages
from articles.models import Visit
from .forms import CustomUserChangeForm, SocialUserForm
from .models import User, Notification
from trade.models import Trades
from reviews.models import Review
from django.db.models import Q


# Create your views here..


def index(request):
    context = {
        "datas": get_user_model().objects.all(),
        "user": request.user,
    }
    return render(request, "accounts/index.html", context)


def signup(request):
    if request.method == "POST":
        form = CreateUser(request.POST, request.FILES)
        print(1)
        if form.is_valid():
            user = form.save()
            my_login(request, user)
            print(2)
            return redirect("articles:main")
        else:
            messages.warning(request, "이미 존재하는 ID입니다.")

    else:
        form = CreateUser()
        print(3)
    context = {
        "form": form,
    }
    print(form.errors)

    return render(request, "accounts/signup.html", context)


def delete(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.user == user:
        user.delete()
    return redirect("articles:main")


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        print(1)
        if form.is_valid():
            my_login(request, form.get_user())
            return redirect(request.GET.get("next") or "articles:main")
        else:
            form = AuthenticationForm()
            messages.warning(request, "ID가 존재하지 않거나 암호가 일치하지 않습니다.")
            context = {"form": form}
            return render(request, "accounts/login.html", context)
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context)


@login_required
def logout(request):
    my_logout(request)
    return redirect("articles:main")


def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    rank_percent = (user.rank % 1000) * 10
    trades = Trades.objects.all()
    tradeslist = []
    for trade in trades:
        if trade.user.pk == pk:
            tradeslist.append(trade)
    tradecount = len(tradeslist)

    reviews = Review.objects.all()
    reviewslist = []
    for review in reviews:
        if review.user.pk == pk:
            reviewslist.append(review)
    reviewcount = len(reviewslist)

    trades = Trades.objects.all()
    jjim_list = []
    for trade in trades:
        jjims = trade.marker.all()
        for j in jjims:
            if j.pk == pk:
                jjim_list.append(trade)
    jjimsc = len(jjim_list)

    reviews = Review.objects.all()
    like_list = []
    for review in reviews:
        likes = review.like_users.all()
        for l in likes:
            if l.pk == pk:
                like_list.append(review)
    likesc = len(like_list)

    if request.user.is_authenticated:
        new_message = Notification.objects.filter(Q(user=request.user) & Q(check=False))
        message_count = len(new_message)
        context = {
            "count": message_count,
            "user": user,
            "rank_percent": rank_percent,
            "trades": tradeslist,
            "reviews": reviewslist,
            "tradesc": tradecount,
            "reviewsc": reviewcount,
            "jjim_list": jjim_list,
            "jjimsc": jjimsc,
            "like_list": like_list,
            "likesc": likesc,
        }
    else:
        context = {
            "user": user,
            "rank_percent": rank_percent,
            "trades": tradeslist,
            "reviews": reviewslist,
            "tradesc": tradecount,
            "reviewsc": reviewcount,
            "jjim_list": jjim_list,
            "jjimsc": jjimsc,
            "like_list": like_list,
            "likesc": likesc,
        }
    return render(request, "accounts/detail.html", context)


# 프로필 수정
@login_required
def edit_profile(request, pk):
    user = User.objects.get(pk=pk)
    if request.user == user:
        if request.method == "POST":
            form = CustomUserChangeForm(
                request.POST, request.FILES, instance=request.user
            )
            print(2)
            if form.is_valid():
                print(1)
                form.save()
                # try:
                #     user.image = request.FILES["image"]
                #     user.save()
                # except:
                #     print("error")
                return redirect("accounts:detail", user.pk)
        else:
            form = CustomUserChangeForm()
        context = {
            "form": form,
        }
        return render(request, "accounts/edit_profile.html", context)
    else:
        return redirect("articles:main")


@login_required
def change_password(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.user == user:
        if request.method == "POST":
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, "Your password was successfully updated!")
                return redirect("accounts:edit_profile", user.pk)
            else:
                messages.error(request, "Please correct the error below.")
        else:
            form = PasswordChangeForm(request.user)

        context = {
            "form": form,
        }

        return render(request, "accounts/change_password.html", context)
    else:
        return render(request, "accounts/index.html")


# follow
# @login_required
# def follow(request, pk):
#     user = get_user_model().objects.get(pk=pk)

#     if request.user != user:
#         if request.user not in user.followers.all():
#             user.followers.add(request.user)
#             is_following = True
#         else:
#             user.followers.remove(request.user)
#             is_following = False
#     data = {
#         "isFollowing": is_following,
#         "followers": user.followers.all().count(),
#         "followings": user.followings.all().count(),
#     }
#     return JsonResponse(data)


def message(request, pk):
    noti = Notification.objects.get(pk=pk)
    noti.check = True
    noti.save()
    id = noti.nid
    if noti.category == "거래":
        print(1)
        return redirect("trade:detail", id)

    elif noti.category == "리뷰":
        return redirect("reviews:detail", id)
    elif noti.category == "채팅":
        print(2)
        return redirect("chat:room", id)


@login_required
def follow(request, pk):
    if request.user.is_authenticated:
        user = get_user_model().objects.get(pk=pk)
        if request.user != user:
            if user.followers.filter(pk=request.user.pk).exists():
                user.followers.remove(request.user)
                is_followed = False
                # 상대방이 나를 팔로우
            else:
                user.followers.add(request.user)
                is_followed = True
                # 상대방이 나를 팔로우
            followers = user.followers.all()
            f_datas = []
            for follower in followers:
                f_datas.append(
                    {
                        "follower_pk": follower.pk,
                        "follower_img": str(follower.image),
                        "follower_name": follower.username,
                    }
                )
            print(f_datas)
            data = {
                "is_followed": is_followed,
                "followers_count": user.followers.count(),
                "followings_count": user.followings.count(),
                "f_datas": f_datas,
            }
            return JsonResponse(data)
        return redirect("accounts:detail", user.username)
    return redirect("accounts:login")


import secrets

state_token = secrets.token_urlsafe(16)


def naver_request(request):
    naver_api = "https://nid.naver.com/oauth2.0/authorize?response_type=code"
    client_id = "pon_1iQapAZ1p8AUXrcY"  # 배포시 보안적용 해야함
    redirect_uri = "http://keyboardwarriorbean-env.eba-uzmimep3.ap-northeast-2.elasticbeanstalk.com/accounts/login/naver/callback/"
    state_token = secrets.token_urlsafe(16)
    return redirect(
        f"{naver_api}&client_id={client_id}&redirect_uri={redirect_uri}&state={state_token}"
    )


def naver_callback(request):
    data = {
        "grant_type": "authorization_code",
        "client_id": "pon_1iQapAZ1p8AUXrcY",  # 배포시 보안적용 해야함
        "client_secret": "WqiKwwjuJa",
        "code": request.GET.get("code"),
        "state": request.GET.get("state"),
        "redirect_uri": "http://keyboardwarriorbean-env.eba-uzmimep3.ap-northeast-2.elasticbeanstalk.com/accounts/login/naver/callback/",
    }
    naver_token_request_url = "https://nid.naver.com/oauth2.0/token"
    access_token = requests.post(naver_token_request_url, data=data).json()[
        "access_token"
    ]

    headers = {"Authorization": f"bearer {access_token}"}
    naver_call_user_api = "https://openapi.naver.com/v1/nid/me"
    naver_user_information = requests.get(naver_call_user_api, headers=headers).json()

    naver_id = naver_user_information["response"]["id"]
    naver_nickname = naver_user_information["response"]["nickname"]
    naver_email = naver_user_information["response"]["email"]
    naver_img = naver_user_information["response"]["profile_image"]
    if get_user_model().objects.filter(naver_id=naver_id).exists():
        naver_user = get_user_model().objects.get(naver_id=naver_id)
        my_login(request, naver_user)
        return redirect(request.GET.get("next") or "articles:main")
    else:
        naver_login_user = get_user_model()()
        naver_login_user.username = naver_nickname
        naver_login_user.naver_id = naver_id
        naver_login_user.set_password(str(state_token))
        naver_login_user.email = naver_email
        naver_login_user.image = naver_img
        naver_login_user.is_social = 2
        naver_login_user.save()
        naver_user = get_user_model().objects.get(naver_id=naver_id)
        my_login(request, naver_user)
        pk = naver_user.pk
        return redirect("accounts:social_form", pk)


def google_request(request):
    google_api = "https://accounts.google.com/o/oauth2/v2/auth"
    client_id = "598608554936-g6vpds53d1qcmaagquvb54mcb69ce54v.apps.googleusercontent.com"  # 배포시 보안적용 해야함
    redirect_uri = "http://keyboardwarriorbean-env.eba-uzmimep3.ap-northeast-2.elasticbeanstalk.com/accounts/login/google/callback"
    google_base_url = "https://www.googleapis.com/auth"
    google_email = "/userinfo.email"
    google_myinfo = "/userinfo.profile"
    scope = f"{google_base_url}{google_email}+{google_base_url}{google_myinfo}"
    return redirect(
        f"{google_api}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
    )


def google_callback(request):
    data = {
        "code": request.GET.get("code"),
        "state": request.GET.get("state"),
        "grant_type": "authorization_code",
        "client_id": "598608554936-g6vpds53d1qcmaagquvb54mcb69ce54v.apps.googleusercontent.com",  # 배포시 보안적용 해야함
        "client_secret": "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",
        "redirect_uri": "http://keyboardwarriorbean-env.eba-uzmimep3.ap-northeast-2.elasticbeanstalk.com/accounts/login/google/callback",
    }
    google_token_request_url = "https://oauth2.googleapis.com/token"
    access_token = requests.post(google_token_request_url, data=data).json()[
        "access_token"
    ]
    params = {
        "access_token": f"{access_token}",
    }
    google_call_user_api = "https://www.googleapis.com/oauth2/v3/userinfo"
    google_user_information = requests.get(google_call_user_api, params=params).json()

    g_id = google_user_information["sub"]
    g_name = google_user_information["name"]
    g_email = google_user_information["email"]
    g_img = google_user_information["picture"]

    if get_user_model().objects.filter(goo_id=g_id).exists():
        google_user = get_user_model().objects.get(goo_id=g_id)
        my_login(request, google_user)
        return redirect(request.GET.get("next") or "articles:main")
    else:
        google_login_user = get_user_model()()
        google_login_user.username = g_name
        google_login_user.email = g_email
        google_login_user.goo_id = g_id
        google_login_user.image = g_img
        google_login_user.is_social = 1
        google_login_user.set_password(str(state_token))
        google_login_user.save()
        google_user = get_user_model().objects.get(goo_id=g_id)
        pk = google_user.pk
        my_login(request, google_user)
        return redirect("accounts:social_form", pk)


# 소셜유저 로그인 후 개인정보 입력창 이동
@login_required
def social_form(request, pk):
    user = get_user_model().objects.get(pk=pk)
    print("유저정보확인")
    if request.user == user:
        print("로긴 확인")
        if request.method == "POST":
            print("포스트확인")
            form = SocialUserForm(request.POST, instance=request.user)
            print("폼에 데이터넣기")
            print(form)
            if form.is_valid():
                form.save()
                return render(request, "articles/main.html")
        else:
            form = SocialUserForm(instance=request.user)
        context = {
            "form": form,
        }
        return render(request, "accounts/social_form.html", context)
    else:
        return render(request, "articles/main.html")


# @login_required
# def first_message(request, trade_pk, user_pk):
#     send_user = request.user
#     trade = Trades.objects.get(pk=trade_pk)
#     reception_user = User.objects.get(pk=user_pk)
#     user = request.user
#     if Room.objects.filter(
#         trade=trade, send_user=send_user, reception_user=reception_user
#     ).exists():
#         select_room = Room.objects.filter(
#             trade=trade, send_user=send_user, reception_user=reception_user
#         )
#         old_room = select_room[0]
#         all_room = Room.objects.filter(
#             Q(send_user=request.user) | Q(reception_user=request.user)
#         )
#         room_message = Message.objects.filter(room=old_room)
#         context = {
#             "room": old_room,
#             "user": user,
#             "all_room": all_room,
#             "room_message": room_message,
#         }
#         return render(request, "accounts/messageCheck.html", context)
#     else:  # 첫 메세지 전송이라면
#         new_room = Room.objects.create(
#             trade=trade,
#             reception_user=reception_user,
#             send_user=send_user,
#         )
#         all_room = Room.objects.filter(
#             Q(send_user=request.user) | Q(reception_user=request.user)
#         )

#         room_message = Message.objects.filter(room=new_room)

#         context = {
#             "room": new_room,
#             "user": user,
#             "all_room": all_room,
#             "room_message": room_message,
#         }

#         return render(request, "accounts/messageCheck.html", context)


# def fill_message(request):

#     return redirect("accounts:messageCheck", context)


# def message(request, room_pk):
#     user = request.user
#     room = Room.objects.get(pk=room_pk)
#     all_room = Room.objects.filter(
#         Q(send_user=request.user) | Q(reception_user=request.user)
#     )
#     if request.method == "POST":
#         print("포스트확인")
#         form = MessageForm(request.POST)
#         print(form)
#         if form.is_valid():
#             print("유효성")
#             message = form.save(commit=False)
#             message.user = user
#             message.room = room
#             message.save()
#             room_message = Message.objects.filter(room=room)
#             context = {
#                 "all_room": all_room,
#                 "room": room,
#                 "room_message": room_message,
#             }
#             return render(request, "accounts/messageCheck.html", context)
#     else:
#         form = MessageForm()
#         room = Room.objects.get(pk=room_pk)
#         room_message = Message.objects.filter(room=room)
#     context = {
#         "form": form,
#         "room": room,
#         "room_message": room_message,
#         "all_room": all_room,
#     }
#     return render(request, "accounts/messageCheck.html", context)


# def messageCheck(request):
#     user = request.user
#     all_message = Message.objects.all()
#     send_message = Message.objects.filter(send_user=user)
#     reception_message = Message.objects.filter(reception_user=user)
#     context = {
#         "all_message": all_message,
#         "send_message": send_message,
#         "reception_message": reception_message,
#     }
#     return render(request, "accounts/messageCheck.html", context)


# def messageRoom(request, trade_pk):
#     user = request.user
#     trade = Trades.objects.get(pk=trade_pk)
#     all_room = Room.objects.filter(Q(send_user=user) | Q(reception_user=user))
#     room = all_room[0]
#     room_list = []
#     if len(all_room) > 0:
#         room_list.append(room_list)
#     context = {"all_room": all_room, "room": room}
#     return render(request, "accounts/messageCheck.html", context )#
