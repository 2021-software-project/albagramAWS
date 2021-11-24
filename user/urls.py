from django.urls import include, path


from .views import PasswordTokenCheckAPI, RequestPasswordResetEmail, SetNewPasswordAPIView, \
    UserRatingVIEW, UserPostingClickVIEW, \
    ratingDetails, UserPostingLikeVIEW, UserPostingLikeDetails, UserPostingLikeWithPosting, \
    UserDetailVIEW, mbtiRcm, persRcm, postings, resultSatisfyView, resultSatisfyDetails
from .views import SignupView, LoginView
from rest_auth.views import LogoutView, PasswordChangeView

from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('password/change/', PasswordChangeView.as_view()),
    # path('auth/signup/', include('rest_auth.registration.urls')),
    # path('auth/signup/', csrf_exempt(include('rest_auth.registration.urls'))),
    path('auth/signup/', SignupView.as_view(), name='rest-auth.registration.urls'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset-api/<uidb64>/<token>',PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),


    # path('auth/password/reset/', PasswordResetView.as_view()),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    # path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),


    # path('admin/', admin.site.urls),

    path('detail/<str:email>', UserDetailVIEW.as_view()),
    path('detail/change/', UserDetailVIEW.as_view()),
    path('userrating/', UserRatingVIEW.as_view()),
    path('userrating/<int:ratingId>', ratingDetails.as_view()),
    path('userpostingclick/', UserPostingClickVIEW.as_view()),
    path('userpostinglike/', UserPostingLikeVIEW.as_view()),
    path('userpostinglike/<str:email>/<int:post_id>', UserPostingLikeDetails.as_view()),
    path('userpostinglike/withposting/<str:email>',UserPostingLikeWithPosting.as_view()),
    path('resultsatisfy/', resultSatisfyView.as_view()),
    path('resultsatisfy/<int:id>', resultSatisfyDetails.as_view()),
    path('mbtircm/', mbtiRcm.as_view(), name='mbtircm'),
    path('persrcm/', persRcm.as_view(), name='persrcm'),
    path('postings/', postings, name='postings'),
]