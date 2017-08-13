# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseRedirect,
# from django.template import loader
from django.contrib.auth.models import User
from .models import (Question,
                     Choice,
                     UserProfile,
                     Recruitment,
                     RecruitmentForm,
                     Round,
                     Questionnaire,
                     PublishedEvent,
                     RegisterEvent,
                     EmailContentEvent
                     )

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from    django.utils import timezone
from django.contrib.auth.models import User
from .form import (
    RegisterForm,
    EditProfileForm,
    RecruitmentDataForm,
    Answer,
    AuthorForm,
    EventRegister
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.forms import (inlineformset_factory,
                          modelformset_factory,)

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.html import strip_tags

from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template

class IndexView(generic.ListView):

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            '-pub_date'
        )[:5]


class DetailView(generic.DetailView):
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/detail.html', {'question': question})
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    # question = get_object_or_404(Question, pk = question_id)
    # return render(request,'polls/results.html',{'question':question})
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

        # create views login
'''create token'''
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) +  six.text_type(user.is_active)

account_activation_token = AccountActivationTokenGenerator()

'''register user'''
def register(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('polls/confirm_create_user_via_email.html', {
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            # return redirect('home')
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            if request.user:
                return HttpResponse('Account already exist')
            else:
                return HttpResponse('Oops Error')
    else:
        form = RegisterForm()

        args = {'form':form}
        return render(request, 'polls/register.html', args)

'''Active user after confirm email'''
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print (uid)
        user = User.objects.get(pk=uid)
        print (user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # self.assertFalse(account_activation_token.check_token(user, token))
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. '
                            'Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def profile(request):
    args = {'user':request.user}
    return render(request, 'polls/profile.html',args)


def edit_profile(request):
    formcombine = inlineformset_factory(User,UserProfile, fields=('city',
                                                                  'university',
                                                                  'image',))
    if request.method == 'POST':

        form1 = EditProfileForm(request.POST, instance=request.user)
        form = formcombine(request.POST, request.FILES, instance=request.user)
        if form.is_valid() and form1.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            #save_image = UserProfile(image=request.FILES['image'])
            #save_image.save()
            #postimage = UserProfile(image = request.FILES['image'])
            #postimage.save()
            form1.save()
            form.save()
            #form.save()
            #form1.save()
            return redirect('/polls/profile')
    else:
        form =  formcombine(instance=request.user)
        form1 = EditProfileForm(instance=request.user)
        args = {'form':form,
                'form1':form1}
        return render(request, 'polls/edit_profile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) #keep session after change password
            return redirect('/polls/profile')
        else:
            return redirect('/profile/change_password')
    else:
        form =  PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request, 'polls/change_password.html', args)

class testTemplate(generic.ListView):
    template_name = 'polls/testTemplate.html'
    context_object_name = 'recruitment'

    def get_queryset(self):
        return Recruitment.objects.all()

'''Student register recruitment compain'''
def DetailForm(request, pk):
    if request.method =='POST':
        form = RecruitmentDataForm(request.POST)
        if form.is_valid():

            post = form.save(commit=False)
            post.user_id = request.user

            post.recruiment_id_id = pk
            post.save()
            return redirect('polls:test')
    else:
        form = RecruitmentDataForm()
        check_user_register = RecruitmentForm.objects.filter(user_id = request.user, pk = pk)
        args = {'form':form}
        if check_user_register:
            return HttpResponse("You already register")
        else:
            return render(request, 'polls/detailform.html', args)

class RegisterFormList(generic.ListView):
    template_name = 'polls/listform.html'
    context_object_name = 'listform'


    def get_queryset(self):
        """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5]
        #a =  Recruitment.objects.all()
        return RecruitmentForm.objects.all()

class QuestionForm(generic.DetailView):
    model = RecruitmentForm
    template_name = 'polls/question.html'


'''def AnswerForm(request,pk):
    a = Questionnaire.objects.filter(recruitment_form=pk)

    formalist = modelformset_factory(Questionnaire, fields=('answer',))

    if request.method == 'POST':
        formset = formalist(request.POST,
                            queryset = a)
        if formset.is_valid():
            formset.save()

            return redirect('polls:listform')
    else:
        formset = formalist(queryset = a)

        args = {'formset':formset}
        return render(request, 'polls/question.html', args)'''

def AnswerForm(request, pk):
    AuthorFormSet = modelformset_factory(Questionnaire, extra=0, form=AuthorForm)

    if request.method == "POST":
        formset = AuthorFormSet(
            request.POST,
            queryset=Questionnaire.objects.filter(recruitment_form=pk),
        )
        if formset.is_valid():

            formset.save()
            # Do something.
    else:

        formset = AuthorFormSet(queryset=Questionnaire.objects.filter(recruitment_form=pk))
    return render(request, 'polls/question.html', {'formset': formset,})


'''List of Event'''
class Event(generic.ListView):
    template_name = 'polls/event.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        '''Return List of event available'''
        return PublishedEvent.objects.all()
        # return PublishedEvent.objects.filter(
        #                                         pub_date__lte = timezone.now()).order_by(
        #                                         '-pub_date')


# """List Detail Event"""
# class DetailEvent(generic.DetailView):
#     model = PublishedEvent
#     template_name = 'polls/detailevent.html'
#
#     def get_queryset(self):
#         """Return detail event"""
#         return PublishedEvent.objects.filter(
#                                              pub_date__lte=timezone.now())
def DetailedEvent(request, pk):
    if request.method =='POST':
        form = EventRegister(request.POST)
        if form.is_valid():

            post = form.save(commit=False)
            post.customer = request.user
            email_e = get_object_or_404(EmailContentEvent, event_id = pk)
            # send_mail(email_e.subject, email_e.content, 'vietnamaiesec@gamil.com', [post.customer_email],
            #           fail_silently=False)
            # text_content = strip_tags(email_e.content)
            # msg = EmailMultiAlternatives(email_e.subject, text_content,
            #                              'vietnamaiesec@gamil.com', [post.customer_email])
            # msg.attach_alternative(email_e.content, "text/html")
            # msg.send()
            # template = get_template(email_e.content)
            # context = Context({'user': user, 'other_info': info})
            # content = template.render(context)
            # if not user.email:
            #     raise BadHeaderError('No email address given for {0}'.format(user))
            msg = EmailMessage(email_e.subject, email_e.content,
                               'vietnamaiesec@gamil.com', [post.customer_email])
            msg.content_subtype = "html"
            # msg.attach_file()
            # msg.mixed_subtype = 'related'
            msg.send()
            post.event_id = pk
            post.save()
            return redirect('polls:event')
    else:
        form = EventRegister()
        event = PublishedEvent.objects.get(pk = pk)
        print (event.event_description)
        check_user_register = RegisterEvent.objects.filter(customer = request.user, event_id = pk)
        args = {'form':form,'event':event}
        # if check_user_register:
        #     return HttpResponse("You already register")
        # else:
        return render(request, 'polls/detailevent.html', args)



def UserEvent(request, event_id):
    if  request.method == "POST":
        form = EventRegister(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.customer = request.user
            post.event = event_id
            post.save()
        return redirect('polls:event')
    else:
        form = EventRegister()
        check_user_register = RegisterEvent.objects.filter(
            customer = request.user, pk = event_id)
        args = {'form': form}
        if check_user_register:
            return HttpResponse("You already registered")
        else:
            return render(request, 'polls/registerevent.html', args)






