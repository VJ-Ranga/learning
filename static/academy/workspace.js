(() => {
  'use strict';
  const mission = JSON.parse(document.getElementById('mission-data').textContent);
  const learner = JSON.parse(document.getElementById('learner-id').textContent);
  const $ = (id) => document.getElementById(id);
  const editor = $('code'), input = $('program-input'), output = $('output');
  const iframe = $('python-sandbox');
  const legacyKey = `python-quest:${learner}:${mission.slug}:v${mission.version}`;
  const initialInput = input.value;
  const initialCode = editor.value;
  let mode = 'learn';
  let activeJob = null, sandboxReady = false, checkingCheckpoint = false;
  let resolveReady;
  const ready = new Promise((resolve) => { resolveReady = resolve; });
  const states = {
    learn: {code:mission.example, input:initialInput, output:'Run the example, change it, and see what happens.'},
    challenge: {code:initialCode === mission.example ? mission.starter : initialCode, input:initialInput, output:'Write your own program. Expected output describes the goal.'}
  };
  try {
    const legacy = localStorage.getItem(legacyKey);
    const challengeDraft = localStorage.getItem(legacyKey + ':challenge');
    const practiceDraft = localStorage.getItem(legacyKey + ':learn');
    if (challengeDraft !== null) states.challenge.code = challengeDraft;
    else if (legacy !== null && legacy !== mission.example) states.challenge.code = legacy;
    if (practiceDraft !== null) states.learn.code = practiceDraft;
    else if (legacy === mission.example) states.learn.code = legacy;
  } catch {}
  function notify(message, success, summary = null) {
    states[mode].feedback = {message, success, summary};
    const box = $('feedback'); box.hidden = false; box.className = `feedback${success ? '' : ' needs-work'}`;
    box.replaceChildren();
    if (summary) {
      const heading = document.createElement('h3');
      heading.textContent = `${summary.complete ? '✓ Mission complete' : 'Not complete yet'} — ${summary.score}/100`;
      box.append(heading);
      const list = document.createElement('ul');
      for (const text of [`Program: ${summary.programPassed}/${summary.programTotal} checks passed`, `Checkpoint: ${summary.quizCorrect ? 'correct ✓' : 'incorrect — review it below'}`]) {
        const item = document.createElement('li'); item.textContent = text; list.append(item);
      }
      box.append(list);
    }
    const p = document.createElement('p'); p.textContent = message; box.append(p);
    if (summary?.complete) {
      const next = $('next-mission-card');
      const action = document.createElement('a'); action.className = 'button primary large-action';
      action.href = next.href; action.textContent = next.querySelector('strong').textContent + ' →';
      box.append(action);
      $('next-action-hint').textContent = 'Mission saved. You are ready for the next step.';
    }
  }
  function showCheckpointFeedback(result) {
    const box = $('checkpoint-feedback'); box.hidden = false;
    box.className = `checkpoint-feedback ${result.correct ? 'is-correct' : 'is-incorrect'}`;
    box.replaceChildren();
    const title = document.createElement('strong'); title.textContent = result.correct ? '✓ Correct — well done!' : '✗ Not quite — try tracing it again.';
    const explanation = document.createElement('p'); explanation.textContent = result.explanation;
    box.append(title, explanation);
    for (const option of document.querySelectorAll('.quiz-option')) {
      option.classList.remove('answer-correct', 'answer-wrong');
      option.querySelector('.answer-badge')?.remove();
      const radio = option.querySelector('input');
      if (radio.value === result.correct_option || radio.checked) {
        const correct = radio.value === result.correct_option;
        option.classList.add(correct ? 'answer-correct' : 'answer-wrong');
        const badge = document.createElement('small'); badge.className = 'answer-badge';
        badge.textContent = correct ? (radio.checked ? 'Your choice · correct' : 'Correct answer') : 'Your choice · incorrect';
        option.append(badge);
      }
    }
  }
  function clearCheckpointFeedback() {
    if (states.challenge.feedback?.summary) {
      states.challenge.feedback = null;
      if (mode === 'challenge') $('feedback').hidden = true;
      $('next-action-hint').textContent = 'Answer changed. Check and save again to verify this attempt.';
    }
    $('checkpoint-feedback').hidden = true;
    for (const option of document.querySelectorAll('.quiz-option')) {
      option.classList.remove('answer-correct','answer-wrong'); option.querySelector('.answer-badge')?.remove();
    }
  }
  document.querySelectorAll('[name=quiz]').forEach(radio => radio.addEventListener('change', clearCheckpointFeedback));
  $('check-question').onclick = async () => {
    if (activeJob || checkingCheckpoint) return;
    const answer = document.querySelector('[name=quiz]:checked')?.value;
    if (!answer) {
      const box = $('checkpoint-feedback'); box.hidden = false; box.className = 'checkpoint-feedback is-incorrect'; box.textContent = 'Choose one answer first, then press Check my answer.'; return;
    }
    checkingCheckpoint = true; busy(true); $('stop-code').hidden = true;
    $('check-question').textContent = 'Checking…';
    try {
      const response = await fetch(`/api/missions/${mission.slug}/checkpoint/`, {method:'POST', headers:{'Content-Type':'application/json','X-CSRFToken':document.querySelector('[name=csrfmiddlewaretoken]').value}, body:JSON.stringify({answer})});
      if (response.redirected) throw new Error('Please log in again, then check your answer.');
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || 'The answer could not be checked. Try again.');
      showCheckpointFeedback(result);
      $('checkpoint-feedback').focus({preventScroll:true});
      $('checkpoint-feedback').scrollIntoView({block:'nearest'});
    } catch (error) {
      const box = $('checkpoint-feedback'); box.hidden = false; box.className = 'checkpoint-feedback is-incorrect'; box.textContent = error.message;
    } finally { checkingCheckpoint = false; busy(false); $('check-question').textContent = 'Check my answer ✓'; }
  };
  function explanationPrompt(button) {
    const intro = `I am a Python beginner with general IT knowledge, learning Python Quest: "${mission.title}". Explain in simple English, step by step. Define new terms and use a small everyday example.`;
    const kind = button.dataset.promptKind;
    let context;
    if (kind === 'section') {
      const [heading, text] = mission.sections[Number(button.dataset.step)];
      context = `Lesson step: ${heading}\nExplanation I am studying: ${text}\nRelated example:\n${mission.example}`;
    } else if (kind === 'example') context = `Explain each line of this example, then trace how its values and output change:\n${mission.example}`;
    else if (kind === 'trace') context = `Help me understand this execution trace:\n${mission.trace.join('\n')}\nCode:\n${mission.example}`;
    else if (kind === 'checkpoint') {
      const choice = document.querySelector('[name=quiz]:checked');
      const label = choice ? mission.options.find(([value]) => value === choice.value)?.[1] : 'not chosen yet';
      context = `Checkpoint: ${mission.question}\nCode:\n${mission.question_code}\nChoices: ${mission.options.map(([,label]) => label).join('; ')}\nMy choice: ${label}`;
      if (!$('checkpoint-feedback').hidden) context += `\nFeedback I received: ${$('checkpoint-feedback').textContent}`;
    } else context = `Challenge requirements: ${mission.challenge}\nMy current challenge code:\n${mode === 'challenge' ? editor.value : states.challenge.code}\nMy last challenge output:\n${mode === 'challenge' ? output.textContent : states.challenge.output}`;
    return `${intro}\n\n${context}\n\nHelp me reason about why the code works or fails. Ask me one small question to check understanding, and give a similar practice exercise. Guide me with hints first; do not immediately write the full solution to my challenge.`;
  }
  document.querySelectorAll('[data-prompt-kind]').forEach(button => button.addEventListener('click', async () => {
    const text = explanationPrompt(button);
    try {
      await navigator.clipboard.writeText(text);
      const label = button.dataset.originalLabel || button.textContent; button.dataset.originalLabel = label; button.textContent = 'Copied ✓ — paste into any AI';
      setTimeout(() => { button.textContent = label; }, 2500);
    } catch {
      $('ai-prompt-text').value = text; $('ai-prompt-dialog').showModal(); $('ai-prompt-text').focus(); $('ai-prompt-text').select();
    }
  }));
  $('close-ai-prompt').onclick = () => $('ai-prompt-dialog').close();
  function showPane(id) {
    if (activeJob || checkingCheckpoint) return;
    states[mode].code = editor.value;
    states[mode].input = input.value;
    states[mode].output = output.textContent;
    mode = id === 'challenge-pane' ? 'challenge' : 'learn';
    for (const tab of document.querySelectorAll('[data-pane]')) {
      const selected = tab.dataset.pane === id;
      tab.classList.toggle('active', selected);
      tab.setAttribute('aria-selected', String(selected));
      $(tab.dataset.pane).hidden = !selected;
    }
    editor.value = states[mode].code;
    input.value = states[mode].input;
    output.textContent = states[mode].output;
    $('editor-filename').textContent = mode === 'learn' ? 'practice.py' : 'mission.py';
    $('editor-purpose').textContent = mode === 'learn' ? 'Lesson practice is separate from your challenge work.' : 'This is your independent challenge draft.';
    $('draft-status').textContent = mode === 'learn' ? 'Lesson practice draft' : 'Your challenge draft';
    $('check-code').hidden = mode !== 'challenge';
    $('feedback').hidden = true;
    if (states[mode].feedback) notify(states[mode].feedback.message, states[mode].feedback.success, states[mode].feedback.summary);
    $('workflow-title').textContent = mode === 'learn' ? 'Step 1: Learn and practise' : 'Step 2: Complete your mission';
    $('workflow-description').textContent = mode === 'learn' ? 'Read the explanations, run the example, then press Next: try your mission.' : 'Write your program → check your checkpoint answer → check and save the program. Look for Mission complete before moving on.';
  }
  document.querySelectorAll('[data-pane]').forEach(tab => tab.addEventListener('click', () => showPane(tab.dataset.pane)));
  $('go-challenge').onclick = () => { showPane('challenge-pane'); $('challenge-tab').focus(); };
  function saveDraft() {
    states[mode].code = editor.value;
    states[mode].feedback = null; $('feedback').hidden = true;
    if (mode === 'challenge') $('next-action-hint').textContent = 'Code changed. Check and save again to verify this draft.';
    try { localStorage.setItem(legacyKey + ':' + mode, editor.value); $('draft-status').textContent = `${mode === 'learn' ? 'Practice' : 'Challenge'} draft saved on this device`; }
    catch { $('draft-status').textContent = 'Device draft storage unavailable'; }
  }
  // Initialize without copying the server's challenge draft into the practice buffer.
  editor.value = states.learn.code;
  output.textContent = states.learn.output;
  showPane('learn-pane');
  editor.addEventListener('input', saveDraft);
  editor.addEventListener('keydown', (event) => {
    if (event.key === 'Tab') {
      event.preventDefault();
      editor.setRangeText('    ', editor.selectionStart, editor.selectionEnd, 'end');
      saveDraft();
    }
    if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) { event.preventDefault(); run(false); }
  });
  $('load-example').onclick = () => {
    if (editor.value !== mission.example && !confirm('Replace this practice draft with the lesson example? Your challenge draft stays separate.')) return;
    editor.value = mission.example; saveDraft(); editor.focus();
  };
  $('reset-code').onclick = () => {
    if (!confirm(mode === 'learn' ? 'Reset your practice draft to the lesson example? Your challenge work stays separate.' : 'Reset your challenge draft to its starter? Submitted attempts remain saved.')) return;
    editor.value = mode === 'learn' ? mission.example : mission.starter; saveDraft();
  };
  $('download-code').onclick = () => {
    const url = URL.createObjectURL(new Blob([editor.value], {type:'text/x-python'}));
    const anchor = document.createElement('a'); anchor.href = url; anchor.download = `${mission.slug}-${mode === 'learn' ? 'practice' : 'challenge'}.py`; anchor.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };
  $('show-solution').onclick = async () => {
    try {
      const response = await fetch(`/api/missions/${mission.slug}/solution/`);
      if (!response.ok || response.redirected) throw new Error('Please log in again to view the solution.');
      const data = await response.json(); $('solution-code').textContent = data.solution; $('solution-code').hidden = false; $('show-solution').hidden = true;
    } catch (error) { notify(error.message, false); }
  };
  function busy(value) {
    for (const id of ['run-code', 'check-code', 'reset-code', 'load-example', 'learn-tab', 'challenge-tab', 'go-challenge', 'check-question']) $(id).disabled = value;
    document.querySelectorAll('[name=quiz]').forEach(radio => { radio.disabled = value; });
    editor.readOnly = value;
    $('stop-code').hidden = !value;
  }
  function finish() { states[mode].output = output.textContent; activeJob = null; busy(false); $('runner-state').textContent = 'Ready to run'; }
  window.addEventListener('message', async (event) => {
    if (event.source !== iframe.contentWindow || event.data?.channel !== 'python-quest') return;
    const data = event.data;
    if (data.type === 'sandbox-ready') { sandboxReady = true; resolveReady(); return; }
    if (!activeJob || data.id !== activeJob.id) return;
    if (data.type === 'status') { $('runner-state').textContent = data.status; return; }
    if (data.type === 'error') { output.textContent = String(data.error); notify('The program could not finish. Nothing was submitted. Fix the issue and try again.', false); finish(); return; }
    if (data.type !== 'result' || !Array.isArray(data.results)) return;
    const job = activeJob;
    if (!job.check) {
      output.textContent = data.results.map(result => result.output + (result.error ? `\n${result.error}` : '')).join('\n') || '(Program finished with no output.)';
      const hasError = data.results.some(result => result.error);
      notify(hasError ? 'Your program hit an error. Read the terminal message and correct the indicated line.' : (mode === 'learn' ? '✓ Your practice program ran successfully. When ready, press Next: try your mission on the left.' : '✓ Your program ran. To find out whether it meets the challenge, use Check program & save.'), !hasError);
      finish(); return;
    }
    const results = data.results;
    output.textContent = results.map((result, i) => {
      const expected = mission.cases[i]?.expected || '';
      const pass = !result.error && result.output.replace(/\r\n/g, '\n').trim() === expected.trim();
      return `${pass ? '✓' : '✗'} Check ${i + 1}\nInput: ${mission.cases[i].inputs.join(' | ') || '(none)'}\nExpected:\n${expected}\nYour output:\n${result.output || '(no output)'}${result.error ? `\n${result.error}` : ''}`;
    }).join('\n\n');
    try {
      $('runner-state').textContent = 'Saving your attempt…';
      $('stop-code').hidden = true;
      const response = await fetch(`/api/missions/${mission.slug}/attempt/`, {
        method:'POST', headers:{'Content-Type':'application/json','X-CSRFToken':document.querySelector('[name=csrfmiddlewaretoken]').value},
        body:JSON.stringify({code:job.code, quiz_answer:job.answer, results})
      });
      if (response.redirected) throw new Error('Your session has ended. Your device draft is kept; log in and run the checks again.');
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || 'Could not save your attempt.');
      showCheckpointFeedback({correct:result.quiz_correct,correct_option:result.correct_option,explanation:result.quiz_explanation});
      notify(`${result.passed ? 'Saved! Continue with the next mission below.' : 'Your attempt is saved. Fix the failed checks or review your checkpoint, then try again.'} ${result.quiz_explanation} Best practice marks: ${result.progress.xp} XP.`, result.passed, {complete:result.passed,score:result.score,programPassed:result.details.filter(detail=>detail.passed).length,programTotal:result.details.length,quizCorrect:result.quiz_correct});
      $('feedback').focus({preventScroll:true}); $('feedback').scrollIntoView({block:'nearest'});
      $('draft-status').textContent = 'Attempt saved to your account';
    } catch (error) { notify(`${error.message} Your code is still here; you can retry.`, false); }
    finish();
  });
  async function run(check) {
    if (activeJob || checkingCheckpoint) return;
    if (check && mode !== 'challenge') { showPane('challenge-pane'); return; }
    if (!editor.value.trim()) { notify('Write a line of Python first, then run it.', false); return; }
    if (editor.value.length > 20000) { notify('Keep this beginner program under 20,000 characters.', false); return; }
    const answer = document.querySelector('[name=quiz]:checked')?.value;
    if (check && !answer) { showPane('challenge-pane'); notify('Choose your checkpoint answer, then press Check program & save again.', false); return; }
    states[mode].feedback = null;
    busy(true); $('feedback').hidden = true; output.textContent = 'Preparing Python…';
    const id = crypto.randomUUID();
    activeJob = {id,check,code:editor.value,answer};
    if (!sandboxReady) {
      let timer;
      try { await Promise.race([ready, new Promise((_, reject) => { timer = setTimeout(() => reject(new Error('The coding workspace could not load. Refresh the page and try again.')), 10000); })]); }
      catch (error) { output.textContent = error.message; finish(); return; }
      finally { clearTimeout(timer); }
    }
    if (!activeJob || activeJob.id !== id) return;
    const cases = check ? mission.cases.map(test => test.inputs) : [input.value === '' ? [] : input.value.replace(/\r\n/g,'\n').split('\n')];
    iframe.contentWindow.postMessage({channel:'python-quest',type:'run',id,code:activeJob.code,cases}, '*');
  }
  const ping = () => iframe.contentWindow.postMessage({channel:'python-quest',type:'ping'}, '*');
  iframe.addEventListener('load', ping);
  ping();
  $('run-code').onclick = () => run(false);
  $('check-code').onclick = () => run(true);
  $('stop-code').onclick = () => {
    iframe.contentWindow.postMessage({channel:'python-quest',type:'stop'}, '*');
    output.textContent = 'Program stopped. Nothing was submitted.'; finish();
  };
})();
