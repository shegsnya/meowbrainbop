from django.contrib import admin
from .models import Quiz, Question, Choice, Answer, QuizTaker, Result, UserResponse

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(QuizTaker)
admin.site.register(Result)
admin.site.register(UserResponse)

