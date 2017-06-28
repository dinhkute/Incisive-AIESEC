# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseRedirect,
# from django.template import loader
from .models import (Question,
                     Choice,
                     UserProfile,
                     Recruitment,
                     RecruitmentForm,
                     Round,
                     Questionnaire,
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
    AuthorForm
)
from    django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.forms import (inlineformset_factory,
                          modelformset_factory,)

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


def register(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/polls')
    else:
        form = RegisterForm()

        args = {'form':form}
        return render(request, 'polls/register.html', args)


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
            form.save()
            form1.save()
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

