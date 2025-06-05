from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Answer, QuizTaker

from .models import Quiz, Question, Choice, QuizTaker, Answer, Result, UserResponse
from .forms import QuizForm, QuestionForm, ChoiceFormSet


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

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('choices')

    if request.method == 'POST':
        quiz_taker = QuizTaker.objects.create(quiz=quiz, user=request.user)
        score = 0

        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                selected_choice = Choice.objects.get(id=selected_choice_id)
                Answer.objects.create(
                    quiz_taker=quiz_taker,
                    question=question,
                    selected_choice=selected_choice
                )
                if selected_choice.is_correct:
                    score += 1

        Result.objects.create(user=request.user, score=score)
        return redirect('quiz_results', quiz_id=quiz.id)

    return render(request, 'quiz/take_quiz.html', {
        'quiz': quiz,
        'questions': questions
    })

@login_required
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz_taker = QuizTaker.objects.filter(quiz=quiz, user=request.user).first()
    print(f"Quiz taker: {quiz_taker}")
    answers = Answer.objects.filter(quiz_taker=quiz_taker)
    print(f"Answers count: {answers.count()}")
    for a in answers:
        print(f"Question: {a.question}, Selected: {a.selected_choice}") 
    score = 0
    total_questions = quiz.questions.count()

    
    question_results = []

    for answer in answers:
        is_correct = answer.selected_choice.is_correct
        if is_correct:
            score += 1

        question_results.append({
            'question_text': answer.question.text,
            'selected_choice_text': answer.selected_choice.text,
            'is_correct': is_correct,
            'correct_choice_text': answer.question.choices.filter(is_correct=True).first().text if answer.question.choices.filter(is_correct=True).exists() else "No correct answer set"
        })

    Result.objects.create(
        user=request.user,
        score=score,
    )

    return render(request, 'quiz/quiz_results.html', {
        'quiz': quiz,
        'score': score,
        'total': total_questions,
        'question_results': question_results,  
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
