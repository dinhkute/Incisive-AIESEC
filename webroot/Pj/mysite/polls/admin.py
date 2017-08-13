# Register your models here.
from django.contrib import admin
from .models import (
                     UserProfile,
                     Recruitment,
                     RecruitmentForm,
                     Questionnaire,
                     Creatia,
                     Task,
                     SubProject,
                     Project,
                     PublishedEvent,
                     ProjectOfKind,
                     LocalCommittee,
                     RegisterEvent,
                     EmailContent,
                     EventMetric,
                     EmailContentEvent,
                     TaskFile,)
from nested_inline.admin import (NestedStackedInline,
                                 NestedModelAdmin,
                                 NestedTabularInline)
from django.db.models.functions import Trunc
from django.db.models import DateTimeField
from django.db.models import Sum, Count, Min, Max
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from jet.admin import CompactInline
from rangefilter.filter import DateRangeFilter
from totalsum.admin import TotalsumAdmin
import datetime
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from jet.admin import CompactInline
from django.contrib.auth.models import User

class BookResource(resources.ModelResource):

    class Meta:
        model = RecruitmentForm
        exclude = ('imported',)

# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3

class CreatiaInline(NestedTabularInline):
    model = Creatia
    extra = 0
    # def sum_each_round(self):
    #     qs= self.model.objects.values('round').annotate(sum = Sum('point'))
    #     print (qs)
    #     return qs
    #list_display = ('point_sum')



class FormInline2(NestedTabularInline,):
    model = Questionnaire
    extra = 0
    inlines = [CreatiaInline]
    readonly_fields = ['answer']


class FormInline(NestedTabularInline,):
    model = RecruitmentForm
    inlines = [FormInline2]
    extra = 0


# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,              {'fields':['question_text']}),
#         ('Date Information',{'fields':['pub_date']}),]
#     inlines = [ChoiceInline]
#     list_display = ('question_text','pub_date', 'was_published_recently')
#     list_filter = ['pub_date']
#     #list_per_page = {10}
#     search_fields = ['question_text']


#@admin.register(Recruitment, RecruitmentForm)
class RecruitmentCompaint(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {'fields':['name']}),
    #     ('Date Information', {'fields': ['pub_date']}),
    #     ('Description',{'fields':['content']}),
    #      ('local commet',{'fields':['local_committee']})
    # ]
    list_display = ('name', 'pub_date','local_committee','status')
    search_fields = ['name','local_committee__City']
    list_filter = ['local_committee', ('pub_date', DateRangeFilter)]

    #inlines = [FormInline]

class RecruitmentFormCompaint(NestedModelAdmin,
                              ImportExportModelAdmin,admin.ModelAdmin):
    def receipt_amount(self, request):
        a = Creatia.objects.filter(pk=1).values_list('point', flat=True)
        total_point = sum(a)
        return total_point
    # receipt_amount.short_description = 'Receipt Amount'
    # fieldsets = [
    #     (None, {'fields':['student_name']}),
    #     ('University',{'fields':['university','skill','receipt_amount']}),
    #     ('Skill',{'fields':['skill']}),
    # ]
    #

    list_filter = ['recruiment_id',('recruiment_id__pub_date', DateRangeFilter),
                   'year_program',]

    list_per_page = 20
    inlines = [FormInline2]
    search_fields = ['student_name', 'university', 'year_program',]
    readonly_fields = ['university','skill','student_name',
                       'user_id','recruiment_id','description','year_program',
                       ]
    list_display = ('student_name', 'university', 'year_program',
                    'recruiment_id','status')
    resource_class = BookResource
    list_select_related = ['recruiment_id']
    change_form_template = 'admin/sum_point.html'

    def has_add_permission(self, request):
        return False


    def get_total(self,pk):
        # a = Creatia.objects.filter(round=id).values_list('point', 'round',flat=True)
        # total_point = sum(a)
        # print (total_point)
        total_point = Creatia.objects.filter(
                                                questionnaire__recruitment_form=pk).values('round').annotate(sum = Sum('point'))
        return total_point

    #Creatia.objects.filter(pk=1).values_list('point', flat=True).annotate(sum=Sum('point'))
    def change_view(self, request, object_id, form_url='', extra_context=None):
        # extra_context = extra_context or {}
        # extra_context['osm_data'] = self.get_osm_info(object_id)
        # print (extra_context['osm_data'])
        # print (object_id)
        # return super(SubProjectAssignTask, self).change_view(request, object_id,
        #                                              form_url, extra_context=extra_context)
        my_context = {
            'total': self.get_total(object_id)
        }
        print (object_id)
        return super(RecruitmentFormCompaint, self).change_view(request, object_id,
                                                      form_url, extra_context=my_context)
    actions = ['send_EMAIL',]

    def send_EMAIL(self, request, queryset):
        email_p = get_object_or_404(EmailContent, email_kind='p')
        email_f = get_object_or_404(EmailContent,email_kind='f')
        email_1 = get_object_or_404(EmailContent,email_kind='1')
        email_2 = get_object_or_404(EmailContent,email_kind='2')
        email_3 = get_object_or_404(EmailContent,email_kind='3')
        for i in queryset:
            if i.status == 'p':
                send_mail(email_p.subject,
                          email_p.content,
                          'vietnamaiesec@gamil.com',[i.user_id.email], fail_silently=False)
                self.message_user(request, "Mail sent successfully ")
            elif i.status == '1':
                send_mail(email_1.subject,
                          email_1.content,
                          'vietnamaiesec@gamil.com',[i.user_id.email], fail_silently=False)
                self.message_user(request, "Mail sent successfully ")
            elif i.status == '2':
                send_mail(email_2.subject,
                          email_2.content,
                          'vietnamaiesec@gamil.com',[i.user_id.email], fail_silently=False)
                self.message_user(request, "Mail sent successfully ")
            elif i.status == '3':
                send_mail(email_3.subject,
                          email_3.content,
                          'vietnamaiesec@gamil.com',[i.user_id.email], fail_silently=False)
                self.message_user(request, "Mail sent successfully ")
            elif i.status == 'f':
                send_mail(email_f.subject,
                          email_f.content,
                          'vietnamaiesec@gamil.com',[i.user_id.email], fail_silently=False)
                self.message_user(request, "Mail sent successfully ")
            else:
                self.message_user(request, "No Mail to sent")
    send_EMAIL.short_description = "Send an email to selected users"

"""File submit for Task"""
class InlineFile(admin.StackedInline):
    model = TaskFile
    extra = 0

'''Task for each user'''
class TaskForUser(admin.ModelAdmin):
    list_display = ['task_name','due_date','project',]
    list_per_page = 20
    list_filter = [('due_date', DateRangeFilter),'project']
    inlines = [InlineFile,]

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['member'].queryset = User.objects.filter(is_staff=True,)
        return super(TaskForUser, self).render_change_form(request, context, args, kwargs)
    '''return list task belong user'''
    def get_queryset(self, request):
        qs = super(TaskForUser, self).get_queryset(request)
        print (qs)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(member = request.user)

    '''save edit task belong user'''
    def save_model(self, request, obj, form, change):
        obj.member.add(request.user)
        # if 'task_name' in form.changed_data:
        #     messages.add_message(request, messages.INFO, 'Car has been sold')
        obj.save()
        #super(TaskForUser, self).save_model(request, obj, form, change)

    '''check permission to edit'''
    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser or request.user.is_staff:
            return True
        else:
            return False

    has_delete_permission = has_change_permission

    def has_add_permission(self, request):
        return False



'''Inline SubProject'''
class InlineSubProject(admin.StackedInline):
    model = SubProject
    show_change_link = True
    extra = 0
    # def render_change_form(self, request, context, *args, **kwargs):
    #     context['adminform'].form.fields['member'].queryset = User.objects.filter(is_staff=True,)
    #     return super(InlineSubProject, self).render_change_form(request, context, args, kwargs)

'''Inline Published Project'''
class InlinePublishedProject(admin.StackedInline):
    model = PublishedEvent
    show_change_link = True
    extra = 0


class InlineTask(admin.StackedInline):
    model = Task
    show_change_link = True
    extra = 0
    save_as = True
    # def render_change_form(self, request, context, *args, **kwargs):
    #     context['adminform'].form.fields['member'].queryset = User.objects.filter(is_staff=True,)
    #     return super(InlineTask, self).render_change_form(request, context, args, kwargs)

'''Create Main Project'''
class MainProject(admin.ModelAdmin):
    list_display = ['project_name', 'local_committee','project_kind',
                    'start_date','end_date','status']
    list_filter = ['local_committee','project_kind',
                   ('start_date', DateRangeFilter),
                   ('end_date', DateRangeFilter),]
    list_per_page = 20
    inlines = [InlineSubProject,
               InlinePublishedProject,]
    search_fields = ['local_committee',
                     'project_kind','project_name',
                    'project_description']

'''Inline Task'''

    # actions = ['duplicate_event']
    # def duplicate_event(modeladmin, request, queryset):
    #     for object in queryset:
    #         object.id = None
    #         object.save()
    #
    # duplicate_event.short_description = "Duplicate selected record"
    # #
    # extra = duplicate_event

'''Maintain SubProject'''
class SubProjectAssignTask(admin.ModelAdmin):
    list_display = ['subproject_name',
                    'create_date','closed_date','project','status'
                    ]
    list_filter = ['project', 'project__local_committee',
                   ('create_date', DateRangeFilter),
                   ('closed_date', DateRangeFilter),
                   ]
    list_per_page = 20
    inlines = [InlineTask,]
    search_fields = ['subproject_name',
                     'create_date'
                     'closed_date','project',
                     'project__local_committee']

    # def render_change_form(self, request, context, *args, **kwargs):
    #     context['adminform'].form.fields['member'].queryset = User.objects.filter(is_staff=True,)
    #     return super(SubProjectAssignTask, self).render_change_form(request, context, args, kwargs)
    # def get_queryset(self, request):
    #     qs = super(SubProjectAssignTask, self).get_queryset(request)
    #     if qs.member.is_superuser or qs.member.is_staff :
    #         return qs




'''List of customer'''
class ListOfCustomer(admin.ModelAdmin):
    list_display = ['customer_name','customer_phone','customer_email','event',
                    'payment','attandance']
    list_filter = ['event']
    list_per_page = 20
    search_fields = ['customer_name','customer_phone','event','customer_email']
    readonly_fields = ['event','customer','customer_name','create_date',
                       'customer_phone','customer_email']
    list_editable = ['payment','attandance']
    def has_add_permission(self, request):
        return False
    # actions = ['send_EMAIL',]
    # # send_mail('subject', 'body of the message', 'vietnamaiesec@gamil.com', ['s3452652@rmit.edu.vn'])
    # def send_EMAIL(self, request, queryset):
    #     email_e = get_object_or_404(EmailContent, email_kind='e')
    #     for i in queryset:
    #         if i.customer_email:
    #             send_mail(email_e.subject, email_e.content, 'vietnamaiesec@gamil.com',[i.customer_email], fail_silently=False)
    #             self.message_user(request, "Mail sent successfully ")
    #         else:
    #             self.message_user(request, "Mail sent error ")
    # send_EMAIL.short_description = "Send an email to selected users"
    # if self.pk
    #     super(RecruitmentFormCompaint, self)


'''Publised Event'''
class ListPublishedEvent(admin.ModelAdmin):
    list_display = ['event_name','create_date',
                    'pub_date','closed_date','project','status']
    list_filter = ['project',
                   ('pub_date', DateRangeFilter),
                   ('closed_date', DateRangeFilter),
                   ('create_date', DateRangeFilter),]
    search_fields = ['event_name','create_date',
                    'pub_date','closed_date','project',
                     'event_description']
    list_per_page = 20

'''Create email content'''
class EmailMarketing(admin.ModelAdmin):
    list_display = ['email_kind','subject']

'''Custom metric dashboard for event'''
@admin.register(EventMetric)
class RegisterEventMetric(admin.ModelAdmin):
    list_filter = ['event','event__create_date',
                   'event__project__project_name']

    change_list_template = 'admin/event_metric.html'

    # def get_next_in_date_hierarchy(request, date_hierarchy):
    #     if date_hierarchy + '__day' in request.GET:
    #         return 'hour'
    #     if date_hierarchy + '__month' in request.GET:
    #         return 'day'
    #     if date_hierarchy + '__year' in request.GET:
    #         return 'week'
    #     return 'month'
    def changelist_view(self, request, extra_context=None):

        response = super(RegisterEventMetric, self).changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
        'payment': Sum('payment'),
        'attandance': Sum('attandance'),
        'customer': Count('customer'),
        }
        response.context_data['summary'] = list(
            qs
            .values('event__event_name')
            .annotate(**metrics)
            .order_by('attandance')
        )

        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )

        # summary_over_time = qs.annotate(
        #     period=Trunc(
        #         'event__create_date',
        #         'day',
        #         output_field=DateTimeField(),
        #     ),
        # ).values('period').annotate(total=Sum('attandance')).order_by('period')
        # summary_range = summary_over_time.aggregate(
        #     low=Min('total'),
        #     high=Max('total'),
        # )
        # high = summary_range.get('high', 0)
        # low = summary_range.get('low', 0)
        # response.context_data['summary_over_time'] = [{
        #     'period': x['period'],
        #     'total': x['total'] or 0,
        #     'pct': \
        #         ((x['total'] or 0) - low) / (high - low) * 100
        #         if high > low else 0,
        # } for x in summary_over_time]
        return response




# admin.site.register(Question, QuestionAdmin)
admin.site.register(UserProfile)
admin.site.register(Recruitment, RecruitmentCompaint)
admin.site.register(RecruitmentForm, RecruitmentFormCompaint)
admin.site.register(Task, TaskForUser)
admin.site.register(Project, MainProject)
admin.site.register(SubProject, SubProjectAssignTask)
admin.site.register(RegisterEvent, ListOfCustomer)
admin.site.register(PublishedEvent, ListPublishedEvent)
admin.site.register(EmailContent, EmailMarketing)
admin.site.register(EmailContentEvent)
