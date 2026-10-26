import hashlib
import io
import json
from random import SystemRandom
import zipfile
from datetime import timedelta
from pathlib import Path
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_GET, require_POST
from .curriculum import MISSIONS, BY_SLUG
from .models import Attempt, AuthWindow
from .services import assess, progress


def auth_limited(request, scope):
    key = hashlib.sha256(f'{scope}:{request.META.get("REMOTE_ADDR", "unknown")}'.encode()).hexdigest()
    with transaction.atomic():
        row, _ = AuthWindow.objects.select_for_update().get_or_create(key=key, defaults={'started_at': timezone.now()})
        if row.started_at < timezone.now() - timedelta(minutes=5):
            row.count = 0
            row.started_at = timezone.now()
        row.count += 1
        row.save()
        return row.count > 20


class QuestLoginView(LoginView):
    template_name = 'registration/login.html'

    def post(self, request, *args, **kwargs):
        if auth_limited(request, 'login'):
            return render(request, 'registration/limited.html', status=429)
        return super().post(request, *args, **kwargs)



@login_required
def dashboard(request):
    stats = progress(request.user)
    missions = [{**m, 'number': i + 1, 'best': stats['best'].get(m['slug']), 'completed': m['slug'] in stats['completed_slugs']} for i, m in enumerate(MISSIONS)]
    next_mission = next((m for m in missions if not m['completed']), missions[-1])
    return render(request, 'academy/dashboard.html', {'stats': stats, 'missions': missions, 'next_mission': next_mission})


@login_required
def mission_detail(request, slug):
    mission = BY_SLUG.get(slug)
    if not mission:
        raise Http404
    index = MISSIONS.index(mission)
    mission = {**mission, 'options': SystemRandom().sample(mission['options'], len(mission['options']))}
    latest = Attempt.objects.filter(user=request.user, mission_slug=slug).order_by('-created_at', '-pk').first()
    public = {k: v for k, v in mission.items() if k not in ('solution', 'answer', 'quiz_explanation')}
    return render(request, 'academy/mission.html', {'mission': mission, 'mission_data': public, 'number': index + 1, 'missions': MISSIONS, 'code': latest.code if latest else mission['starter'], 'latest': latest, 'next_mission': MISSIONS[index + 1] if index + 1 < len(MISSIONS) else None})


@login_required
@require_POST
def attempt(request, slug):
    mission = BY_SLUG.get(slug)
    if not mission:
        raise Http404
    try:
        if len(request.body) > 90000:
            raise ValueError('This attempt is too large. Shorten the program and try again.')
        payload = json.loads(request.body)
        result = assess(mission, payload)
    except (ValueError, UnicodeDecodeError) as error:
        return JsonResponse({'error': str(error)}, status=400)
    Attempt.objects.create(user=request.user, mission_slug=slug, version=mission['version'], code=payload['code'], quiz_answer=payload['quiz_answer'], score=result['score'], passed=result['passed'], details=result['details'])
    return JsonResponse({**result, 'progress': progress(request.user)})


@login_required
@require_GET
def progress_api(request):
    return JsonResponse(progress(request.user))


@login_required
@require_GET
def solution(request, slug):
    if slug not in BY_SLUG:
        raise Http404
    return JsonResponse({'solution': BY_SLUG[slug]['solution']})


@login_required
@require_GET
def downloads(request):
    content = io.BytesIO()
    with zipfile.ZipFile(content, 'w', zipfile.ZIP_DEFLATED) as archive:
        for file in sorted((settings.BASE_DIR / 'terminal-programs').glob('*')):
            if file.is_file():
                archive.write(file, f'terminal-programs/{file.name}')
    response = HttpResponse(content.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="python-quest-terminal-programs.zip"'
    return response


@xframe_options_exempt
@require_GET
def runner(request):
    response = render(request, 'academy/runner.html')
    response['Content-Security-Policy'] = "default-src 'none'; script-src 'unsafe-inline' 'wasm-unsafe-eval' https://cdn.jsdelivr.net; connect-src https://cdn.jsdelivr.net; worker-src blob:; frame-ancestors 'self'"
    response['Cache-Control'] = 'public, max-age=3600'
    return response


@require_GET
def setup_help(request):
    return render(request, 'academy/help.html')
