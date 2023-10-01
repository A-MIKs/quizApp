from django.shortcuts import render
from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Question, Answer
from results.models import Result

class QuizListView(ListView):
    model = Quiz
    template_name = "quizes/main.html"

def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, "quizes/quiz.html", {"obj": quiz})

def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})

    return JsonResponse({
        "data":questions,
        "time": quiz.time,
    })

def save_quiz_view(request, pk):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data = dict(data.lists())
        data.pop("csrfmiddlewaretoken")
        
    for k in data.keys():
        question = Question.objects.get(text=k)
        questions.append(question)
    user = request.user
    quiz = Quiz.objects.get(pk=pk)
    score =0
    multiplier = 100 / quiz.num_of_questions
    results = []
    correct_answer = None

    for q in questions:
        ans = request.POST.get(q.text)
        if ans != "":
            question_answers = Answer.objects.filter(question=q)
            for a in question_answers:
                if ans == a.text:
                    if a.correct:
                        score +=1
                        correct_answer = a.text
                else:
                    if a.correct:
                        correct_answer = a.text
            results.append({str(q): {"correct_answer": correct_answer, "answered": ans}})
        else:
            results.append({str(q): "not answered"})

    score_ = score * multiplier
    pass_mark = quiz.pass_mark
    passed = True if score_ >= pass_mark else False
    Result.objects.create(quiz=quiz, user=user, score=score_)
    if score_ >= quiz.pass_mark:
        return JsonResponse({"passed":passed, "score": score_, "results": results})
    else:
        return JsonResponse({"passed":passed, "score": score_, "results": results})  