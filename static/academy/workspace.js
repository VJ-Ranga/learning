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
  let activeJob = null, sandboxReady = false;
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
  function notify(message, success) {
    states[mode].feedback = {message, success};
    const box = $('feedback'); box.hidden = false; box.className = `feedback${success ? '' : ' needs-work'}`;
    box.replaceChildren(); const p = document.createElement('p'); p.textContent = message; box.append(p);
  }
  function showPane(id) {
    if (activeJob) return;
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
    if (states[mode].feedback) notify(states[mode].feedback.message, states[mode].feedback.success);
  }
  document.querySelectorAll('[data-pane]').forEach(tab => tab.addEventListener('click', () => showPane(tab.dataset.pane)));
  $('go-challenge').onclick = () => { showPane('challenge-pane'); $('challenge-tab').focus(); };
  function saveDraft() {
    states[mode].code = editor.value;
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
    for (const id of ['run-code', 'check-code', 'reset-code', 'load-example', 'learn-tab', 'challenge-tab', 'go-challenge']) $(id).disabled = value;
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
      notify(`${result.passed ? 'Mission complete!' : 'Keep going — every attempt teaches you something.'} ${result.score}/100. ${result.quiz_correct ? 'Checkpoint correct.' : 'Review the checkpoint.'} ${result.quiz_explanation} Your best practice marks total ${result.progress.xp} XP.`, result.passed);
      $('draft-status').textContent = 'Attempt saved to your account';
    } catch (error) { notify(`${error.message} Your code is still here; you can retry.`, false); }
    finish();
  });
  async function run(check) {
    if (activeJob) return;
    if (check && mode !== 'challenge') { showPane('challenge-pane'); return; }
    if (!editor.value.trim()) { notify('Write a line of Python first, then run it.', false); return; }
    if (editor.value.length > 20000) { notify('Keep this beginner program under 20,000 characters.', false); return; }
    const answer = document.querySelector('[name=quiz]:checked')?.value;
    if (check && !answer) { showPane('challenge-pane'); notify('Choose your checkpoint answer, then press Check & save again.', false); return; }
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
