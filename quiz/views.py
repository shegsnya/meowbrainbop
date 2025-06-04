from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Quiz, Question
from .forms import QuizForm, QuestionForm
from django.contrib.auth.decorators import login_required
from .forms import ChoiceFormSet
from .models import Choice,Result, UserResponse



def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/home.html', {'quizzes': quizzes})

def list_quizzes(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/home.html', {'quizzes': quizzes})

@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.creator = request.user
            quiz.save()
            return redirect('home')
    else:
        form = QuizForm()
    return render(request, 'quiz/create_quiz.html', {'form': form})

def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST, queryset=Choice.objects.none())
        
        if question_form.is_valid() and formset.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            
            # Save choices and link to the question
            for choice_form in formset:
                choice = choice_form.save(commit=False)
                choice.question = question
                choice.save()
            
            return redirect('quiz_detail', quiz_id=quiz.id)
    else:
        question_form = QuestionForm()
        formset = ChoiceFormSet(queryset=Choice.objects.none())
    
    return render(request, 'quiz/add_question.html', {
        'quiz': quiz,
        'question_form': question_form,
        'formset': formset,
    })


from django.urls import reverse

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('choices').all()

    if request.method == 'POST':
        score = 0
        total = questions.count()

        for question in questions:
            selected = request.POST.get(str(question.id))
            correct_choice = question.choices.filter(is_correct=True).first()
            if selected and correct_choice and selected == correct_choice.text:
                score += 1

        return redirect(f"{reverse('quiz_results', args=[quiz.id])}?score={score}&total={total}")

    return render(request, 'quiz/take_quiz.html', {
        'quiz': quiz,
        'questions': questions
    })



@login_required
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    score = request.GET.get('score')
    total = request.GET.get('total')
    return render(request, 'quiz/quiz_results.html', {
        'quiz': quiz,
        'score': score,
        'total': total
    })


def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz, 'questions': questions})



def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        selected_choice = request.POST.get('choice')
        if not selected_choice:
            return HttpResponse("No choice selected!")

