import json
from django.contrib.auth.models import User
from django.test import TestCase


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

    def test_registration_is_disabled(self):
        self.assertEqual(self.client.get('/join/').status_code, 404)
        self.assertEqual(self.client.post('/join/', {'username':'third','password1':'Third-password-123','password2':'Third-password-123'}).status_code, 404)
        self.assertFalse(User.objects.filter(username='third').exists())
        self.assertNotContains(self.client.get('/login/'), 'Join your learning room')

    def test_password_change_requires_old_password_and_keeps_session(self):
        self.client.force_login(self.learner)
        response = self.client.post('/password/change/', {'old_password':'wrong','new_password1':'New-strong-password-2026','new_password2':'New-strong-password-2026'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/password/change/', {'old_password':'Safe-password-123','new_password1':'New-strong-password-2026','new_password2':'New-strong-password-2026'})
        self.assertEqual(response.status_code, 302)
        self.learner.refresh_from_db()
        self.assertTrue(self.learner.check_password('New-strong-password-2026'))
        self.assertEqual(self.client.get('/').status_code, 200)

    def test_checkpoint_feedback_is_immediate_without_awarding_marks(self):
        from academy.models import Attempt
        self.client.force_login(self.learner)
        response = self.client.post('/api/missions/hello/checkpoint/', json.dumps({'answer':'input'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['correct'])
        self.assertEqual(response.json()['correct_option'], 'print')
        response = self.client.post('/api/missions/hello/checkpoint/', json.dumps({'answer':'print'}), content_type='application/json')
        self.assertTrue(response.json()['correct'])
        self.assertTrue(response.json()['explanation'])
        self.assertEqual(Attempt.objects.count(), 0)
        self.assertEqual(self.client.get('/api/progress/').json()['xp'], 0)

    def test_checkpoint_rejects_anonymous_and_invalid_answers(self):
        self.assertEqual(self.client.post('/api/missions/hello/checkpoint/', '{}', content_type='application/json').status_code, 302)
        self.client.force_login(self.learner)
        for payload in ({}, {'answer':[]}, {'answer':'missing'}, []):
            response = self.client.post('/api/missions/hello/checkpoint/', json.dumps(payload), content_type='application/json')
            self.assertEqual(response.status_code, 400)

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

    def test_auth_throttle(self):
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


class LearnerProvisioningTests(TestCase):
    def test_creates_only_two_learners_with_random_passwords_and_preserves_changes(self):
        import io
        import tempfile
        from pathlib import Path
        from dotenv import dotenv_values
        from django.core.management import call_command
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / '.env.learners'
            output = io.StringIO()
            call_command('provision_learners', password_file=str(file), stdout=output)
            values = dotenv_values(file)
            self.assertEqual(set(User.objects.values_list('username', flat=True)), {'vjranga', 'shanesha'})
            self.assertNotEqual(values['VJRANGA_PASSWORD'], values['SHANESHA_PASSWORD'])
            for username in ('vjranga', 'shanesha'):
                password = values[username.upper() + '_PASSWORD']
                user = User.objects.get(username=username)
                self.assertGreaterEqual(len(password), 20)
                self.assertTrue(user.check_password(password))
                self.assertFalse(user.is_staff or user.is_superuser)
                self.assertNotIn(password, output.getvalue())
                self.assertTrue(self.client.login(username=username, password=password))
                self.client.logout()
            user = User.objects.get(username='vjranga')
            user.set_password('Changed-later-strong-password')
            user.save()
            call_command('provision_learners', password_file=str(file), stdout=output)
            user.refresh_from_db()
            self.assertTrue(user.check_password('Changed-later-strong-password'))
            self.assertEqual(User.objects.count(), 2)
