from django.contrib import admin
from django.utils.text import slugify
from koica.models import Question, Answer, QAComment


class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('posted_by','reported_duplicated_url','is_duplicated')
    
    def save_model(self, request, obj, form, change):
        obj.posted_by = request.user
        #~ autoslug: necessary when a user posts from the site
        if not obj.slug:
            obj.slug=slugify(obj.title)[-25:]
        obj.save()
        
class AnswerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.posted_by = request.user
        obj.save()
        
class CommentAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.posted_by = request.user
        obj.save()


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QAComment, CommentAdmin)