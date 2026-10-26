import json
from django.contrib.auth.models import User
from django.test import TestCase, override_settings


@override_settings(ENROLLMENT_CODE='test-invite')
class QuestTests(TestCase):
    def setUp(self):
        self.learner = User.objects.create_user('learner', password='Safe-password-123')
        self.friend = User.objects.create_user('friend', password='Other-password-123')

    def submit(self, **changes):
        payload = {'code': 'print("Hello, Python!")', 'quiz_answer': 'print',
                   'results': [{'output': 'Hello, Python!\n', 'error': ''}]}
        payload.update(changes)
        return self.client.post('/api/missions/hello/attempt/', json.dumps(payload), content_type='application/json')

    def test_dashboard_requires_login(self):
        self.assertEqual(self.client.get('/').status_code, 302)

    def test_invite_is_required_for_registration(self):
        response = self.client.post('/join/', {'username': 'third', 'password1': 'Third-password-123',
                                             'password2': 'Third-password-123', 'invite_code': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='third').exists())

    def test_correct_invite_creates_learner_not_staff(self):
        response = self.client.post('/join/', {'username': 'third', 'password1': 'Third-password-123',
                                             'password2': 'Third-password-123', 'invite_code': 'test-invite'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.get(username='third').is_staff)

    def test_submission_requires_authentication(self):
        self.assertEqual(self.submit().status_code, 302)

    def test_best_score_does_not_farm_xp_and_belongs_to_logged_in_user(self):
        from academy.models import Attempt
        self.client.force_login(self.learner)
        self.assertEqual(self.submit().json()['score'], 100)
        self.submit(user_id=self.friend.pk, score=999999)
        self.assertEqual(Attempt.objects.filter(user=self.learner).count(), 2)
        self.assertEqual(Attempt.objects.filter(user=self.friend).count(), 0)
        stats = self.client.get('/api/progress/').json()
        self.assertEqual(stats['xp'], 100)
        self.assertEqual(stats['completed'], 1)
        self.assertEqual(stats['leaderboard'][0]['username'], 'learner')

    def test_wrong_output_and_answer_do_not_pass(self):
        self.client.force_login(self.learner)
        data = self.submit(results=[{'output': 'wrong', 'error': ''}], quiz_answer='input').json()
        self.assertEqual(data['score'], 0)
        self.assertFalse(data['passed'])

    def test_runtime_error_never_earns_code_marks(self):
        self.client.force_login(self.learner)
        data = self.submit(results=[{'output': 'Hello, Python!', 'error': 'SyntaxError'}]).json()
        self.assertEqual(data['score'], 20)
        self.assertFalse(data['passed'])

    def test_invalid_payloads_do_not_create_attempts(self):
        from academy.models import Attempt
        self.client.force_login(self.learner)
        for changes in [{'results': []}, {'results': 'bad'}, {'code': 'x' * 20001},
                        {'results': [{'output': [], 'error': ''}]}, {'quiz_answer': []}]:
            self.assertEqual(self.submit(**changes).status_code, 400)
        self.assertEqual(Attempt.objects.count(), 0)
        self.assertEqual(self.client.post('/api/missions/hello/attempt/', '[1]', content_type='application/json').status_code, 400)

    def test_all_missions_render_and_local_programs_download(self):
        from academy.curriculum import MISSIONS
        self.client.force_login(self.learner)
        self.assertGreaterEqual(len(MISSIONS), 10)
        for mission in MISSIONS:
            self.assertTrue(mission['sections'])
            self.assertTrue(mission['cases'])
            self.assertEqual(self.client.get(f'/missions/{mission["slug"]}/').status_code, 200)
        response = self.client.get('/downloads/terminal-programs.zip')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/zip')

    def test_lower_retry_does_not_erase_best_mark_or_previous_draft(self):
        self.client.force_login(self.learner)
        self.submit()
        self.submit(results=[{'output': 'wrong', 'error': ''}], quiz_answer='input', code='print("wrong")')
        self.assertEqual(self.client.get('/api/progress/').json()['xp'], 100)
        self.assertContains(self.client.get('/missions/hello/'), 'print(&quot;wrong&quot;)')

    def test_unknown_mission_and_csrf(self):
        from django.test import Client
        self.client.force_login(self.learner)
        self.assertEqual(self.client.get('/missions/missing/').status_code, 404)
        protected = Client(enforce_csrf_checks=True)
        protected.force_login(self.learner)
        self.assertEqual(protected.post('/api/missions/hello/attempt/', '{}', content_type='application/json').status_code, 403)

    def test_unicode_invites_validate_without_crashing(self):
        payload = {'username': 'third', 'password1': 'Third-password-123', 'password2': 'Third-password-123', 'invite_code': 'ආයුබෝවන්'}
        self.assertEqual(self.client.post('/join/', payload).status_code, 200)
        self.assertFalse(User.objects.filter(username='third').exists())
        with self.settings(ENROLLMENT_CODE='ආයුබෝවන්'):
            self.assertEqual(self.client.post('/join/', payload).status_code, 302)
            self.assertTrue(User.objects.filter(username='third').exists())

    def test_closed_enrollment_and_auth_throttle(self):
        with self.settings(ENROLLMENT_CODE=''):
            response = self.client.post('/join/', {'username': 'third', 'password1': 'Third-password-123', 'password2': 'Third-password-123', 'invite_code': 'test-invite'})
            self.assertEqual(response.status_code, 200)
            self.assertFalse(User.objects.filter(username='third').exists())
        for _ in range(20):
            response = self.client.post('/login/', {'username':'nobody', 'password':'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.post('/login/', {'username':'nobody','password':'wrong'}).status_code, 429)

    def test_friend_cannot_view_my_draft_and_logout_is_post_only(self):
        self.client.force_login(self.learner)
        self.submit(code='print("unique-private-draft")')
        self.client.force_login(self.friend)
        self.assertNotContains(self.client.get('/missions/hello/'), 'unique-private-draft')
        self.assertEqual(self.client.get('/logout/').status_code, 405)

    def test_trusted_terminal_examples_match_all_hand_checked_cases(self):
        import subprocess
        import sys
        from pathlib import Path
        from django.conf import settings
        from academy.curriculum import MISSIONS
        for index, mission in enumerate(MISSIONS, 1):
            file = settings.BASE_DIR / 'terminal-programs' / f'{index:02d}_{mission["slug"].replace("-", "_")}.py'
            for case in mission['cases']:
                result = subprocess.run([sys.executable, str(file)], input='\n'.join(case['inputs']) + '\n', text=True, capture_output=True, timeout=3)
                self.assertEqual(result.returncode, 0, f'{mission["slug"]}: {result.stderr}')
                self.assertEqual(result.stdout.strip(), case['expected'], mission['slug'])


class DeploymentSettingsTests(TestCase):
    def settings_process(self, **changes):
        import os
        import subprocess
        import sys
        env = {**os.environ, 'DJANGO_DEBUG':'0', 'VERCEL':'1', 'DJANGO_SECRET_KEY':'x' * 70, 'DATABASE_URL':'postgresql://example:example@localhost/quest?sslmode=require', **changes}
        return subprocess.run([sys.executable, '-c', 'import questgame.settings'], env=env, capture_output=True, text=True, timeout=10)

    def test_hosted_environment_rejects_debug(self):
        result = self.settings_process(DJANGO_DEBUG='1')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('DEBUG', result.stderr)

    def test_hosted_environment_rejects_sqlite(self):
        result = self.settings_process(DATABASE_URL='sqlite:////tmp/quest-forbidden.sqlite3')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('PostgreSQL', result.stderr)

    def test_hosted_environment_requires_database(self):
        result = self.settings_process(DATABASE_URL='')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('DATABASE_URL', result.stderr)

    def test_hosted_environment_requires_secret(self):
        result = self.settings_process(DJANGO_SECRET_KEY='')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('DJANGO_SECRET_KEY', result.stderr)
