from django.contrib.auth.models import User
from django.db.models import Max, Count, Q
from .curriculum import MISSIONS
from .models import Attempt


def progress(user):
    best = {row['mission_slug']: row['best'] for row in Attempt.objects.filter(user=user, version=1).values('mission_slug').annotate(best=Max('score'))}
    completed = set(Attempt.objects.filter(user=user, version=1, passed=True).values_list('mission_slug', flat=True))
    leaderboard = []
    for learner in User.objects.filter(is_active=True, is_staff=False).order_by('username'):
        records = Attempt.objects.filter(user=learner, version=1).values('mission_slug').annotate(best=Max('score'))
        leaderboard.append({'username': learner.username, 'xp': sum(r['best'] for r in records), 'completed': Attempt.objects.filter(user=learner, version=1, passed=True).values('mission_slug').distinct().count(), 'is_you': learner.pk == user.pk})
    leaderboard.sort(key=lambda row: (-row['xp'], -row['completed'], row['username'].casefold()))
    return {'best': best, 'completed_slugs': list(completed), 'completed': len(completed), 'xp': sum(best.values()), 'total': len(MISSIONS), 'percent': round(len(completed) / len(MISSIONS) * 100), 'leaderboard': leaderboard}


def build_mission_navigation(user, current_slug):
    records = {row['mission_slug']: row for row in Attempt.objects.filter(user=user, version=1).values('mission_slug').annotate(best=Max('score'), passes=Count('pk', filter=Q(passed=True)))}
    navigation = []
    for number, mission in enumerate(MISSIONS, 1):
        record = records.get(mission['slug'])
        navigation.append({'slug': mission['slug'], 'title': mission['title'], 'number': number,
                           'current': mission['slug'] == current_slug,
                           'best': record['best'] if record else None,
                           'status': 'Completed' if record and record['passes'] else 'In progress' if record else 'Not started'})
    return navigation


def check_checkpoint(mission, payload):
    if not isinstance(payload, dict) or not isinstance(payload.get('answer'), str) or payload['answer'] not in {value for value, _ in mission['options']}:
        raise ValueError('Choose one checkpoint answer before checking it.')
    return {'correct': payload['answer'] == mission['answer'], 'correct_option': mission['answer'], 'explanation': mission['quiz_explanation']}


def assess(mission, payload):
    if not isinstance(payload, dict):
        raise ValueError('Send an object containing your code, answer and test results.')
    code, answer, results = (payload.get(k) for k in ('code', 'quiz_answer', 'results'))
    if not isinstance(code, str) or not code.strip() or len(code) > 20000:
        raise ValueError('Your program must contain between 1 and 20,000 characters.')
    checkpoint = check_checkpoint(mission, {'answer': answer})
    if not isinstance(results, list) or len(results) != len(mission['cases']):
        raise ValueError('Run all challenge checks before saving this attempt.')
    details = []
    for result, case in zip(results, mission['cases']):
        if not isinstance(result, dict) or not isinstance(result.get('output'), str) or not isinstance(result.get('error'), str) or len(result['output']) > 12000 or len(result['error']) > 4000:
            raise ValueError('The runner returned an invalid result. Please run the checks again.')
        passed = not result['error'] and result['output'].replace('\r\n', '\n').strip() == case['expected'].strip()
        details.append({'passed': passed, 'output': result['output'], 'error': result['error']})
    code_score = round(80 * sum(d['passed'] for d in details) / len(details))
    quiz_correct = checkpoint['correct']
    score = code_score + (20 if quiz_correct else 0)
    return {'score': score, 'passed': all(d['passed'] for d in details) and quiz_correct, 'details': details, 'quiz_correct': quiz_correct, 'quiz_explanation': mission['quiz_explanation'], 'correct_option': checkpoint['correct_option']}
