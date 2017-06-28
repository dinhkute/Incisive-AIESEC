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
                     RegisterEvent)
from nested_inline.admin import (NestedStackedInline,
                                 NestedModelAdmin,
                                 NestedTabularInline)
from django.db.models import Sum
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class BookResource(resources.ModelResource):

    class Meta:
        model = RecruitmentForm

# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3

class CreatiaInline(NestedTabularInline):
    model = Creatia
    extra = 0
    #def sum_each_round(self):
    #    return self.model.objects.values('round').annotate(sum = Sum('point'))
    #list_display = ('point_sum')



class FormInline2(NestedTabularInline):
    model = Questionnaire
    extra = 0
    inlines = [CreatiaInline]
    readonly_fields = ['answer']


class FormInline(NestedTabularInline):
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
class RecruitmentCompaint(NestedModelAdmin):
    fieldsets = [
        (None, {'fields':['name']}),
        ('Date Information', {'fields': ['pub_date']}),
        ('Description',{'fields':['content']})
    ]
    list_display = ('name', 'pub_date')
    #inlines = [FormInline]

class RecruitmentFormCompaint(NestedModelAdmin,ImportExportModelAdmin):
    fieldsets = [
        (None, {'fields':['student_name']}),
        ('University',{'fields':['university']}),
        ('Skill',{'fields':['skill']}),
    ]


    list_filter = ['recruiment_id','recruiment_id__pub_date','year_program',]

    list_per_page = 20
    inlines = [FormInline2]
    search_fields = ['student_name', 'university', 'year_program']
    readonly_fields = ['university','skill','student_name']
    list_display = ('student_name', 'university', 'year_program', 'recruiment_id',)
    resource_class = BookResource
    list_select_related = ['recruiment_id']

'''Task for each user'''
class TaskForUser(admin.ModelAdmin):
    list_display = ['task_name','due_date','project',]
    list_per_page = 20
    list_filter = ['due_date','project']

    '''return list task belong user'''
    def get_queryset(self, request):
        qs = super(TaskForUser, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(staff = request.user)

    '''save edit task belong user'''
    def save_model(self, request, obj, form, change):
        obj.staff = request.user
        obj.save()

    '''check permission to edit'''
    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser or obj.staff == request.user:
            return True
        else:
            return False

    has_delete_permission = has_change_permission

'''Inline SubProject'''
class InlineSubProject(admin.TabularInline):
    model = SubProject

'''Inline Published Project'''
class InlinePublishedProject(admin.TabularInline):
    model = PublishedEvent

'''Create Main Project'''
class MainProject(admin.ModelAdmin):
    list_display = ['project_name', 'local_committee']
    list_filter = ['local_committee']
    list_per_page = 20
    inlines = [InlineSubProject,]

'''Inline Task'''
class InlineTask(admin.TabularInline):
    model = Task

'''Maintain SubProject'''
class SubProjectAssignTask(admin.ModelAdmin):
    list_display = ['subproject_name',
                    'create_date','closed_date','project']
    list_filter = ['project',
                   'create_date','closed_date',]
    list_per_page = 20
    inlines = [InlinePublishedProject,InlineTask,]

'''List of customer'''
class ListOfCustomer(admin.ModelAdmin):
    list_display = ['customer_name','customer_phone','customer_email','event']
    list_filter = ['event']
    list_per_page = 20


# admin.site.register(Question, QuestionAdmin)
admin.site.register(UserProfile)
admin.site.register(Recruitment, RecruitmentCompaint)
admin.site.register(RecruitmentForm, RecruitmentFormCompaint)
admin.site.register(Task, TaskForUser)
admin.site.register(Project, MainProject)
admin.site.register(SubProject, SubProjectAssignTask)
admin.site.register(RegisterEvent, ListOfCustomer)
