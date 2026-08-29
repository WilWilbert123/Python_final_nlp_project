/* mywebscript.js – client-side logic for the Emotion Detector UI */

const EMOTIONS = ['anger', 'disgust', 'fear', 'joy', 'sadness'];

/**
 * Call the Flask /emotionDetector endpoint and render the result.
 */
async function runDetection() {
  const input  = document.getElementById('inputText');
  const result = document.getElementById('result');
  const bars   = document.getElementById('bars');
  const btn    = document.getElementById('analyseBtn');

  const text = input.value.trim();

  if (!text) {
    result.innerHTML = '⚠️ Please enter some text before analysing.';
    bars.style.display = 'none';
    return;
  }

  // Loading state
  btn.disabled = true;
  result.innerHTML = '<span class="spinner"></span> Analysing…';
  bars.style.display = 'none';

  try {
    const res  = await fetch(`/emotionDetector?textToAnalyze=${encodeURIComponent(text)}`);
    const text2 = await res.text();

    if (!res.ok || text2.startsWith('Invalid')) {
      result.textContent = '❗ ' + text2;
      btn.disabled = false;
      return;
    }

    // Display the plain-text response from Flask
    result.textContent = text2;

    // ── Try to parse scores from the response text for the bar chart ──
    const scores = {};
    EMOTIONS.forEach(e => {
      const match = text2.match(new RegExp(`'${e}':\\s*([0-9.]+)`));
      if (match) scores[e] = parseFloat(match[1]);
    });

    if (Object.keys(scores).length === EMOTIONS.length) {
      renderBars(scores, text2);
    }

  } catch (err) {
    result.textContent = '❗ Request failed – ' + err;
  }

  btn.disabled = false;
}

/**
 * Render animated horizontal bars for each emotion score.
 * @param {Object} scores  - { anger: 0.12, disgust: 0.05, … }
 * @param {string} fullText - full response text (used to extract dominant)
 */
function renderBars(scores, fullText) {
  const bars = document.getElementById('bars');
  bars.innerHTML = '';
  bars.style.display = 'block';

  const dominantMatch = fullText.match(/dominant emotion is (\w+)/i);
  const dominant = dominantMatch ? dominantMatch[1].toLowerCase() : '';

  EMOTIONS.forEach(emotion => {
    const pct  = Math.round((scores[emotion] || 0) * 100);
    const wrap = document.createElement('div');
    wrap.innerHTML = `
      <div class="bar-label">
        <span>${emotion}</span>
        <span>${pct}%</span>
      </div>
      <div class="bar-track">
        <div class="bar-fill" style="width:0%"></div>
      </div>`;
    bars.appendChild(wrap);

    // Animate after paint
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        wrap.querySelector('.bar-fill').style.width = pct + '%';
      });
    });
  });

  if (dominant) {
    const badge = document.createElement('div');
    badge.className = 'dominant-badge';
    badge.textContent = `🏆 Dominant: ${dominant}`;
    bars.appendChild(badge);
  }
}

/**
 * Reset the UI to its initial state.
 */
function clearAll() {
  document.getElementById('inputText').value = '';
  document.getElementById('result').textContent = 'Results will appear here…';
  document.getElementById('bars').style.display = 'none';
  document.getElementById('bars').innerHTML = '';
}

// Allow pressing Enter to trigger analysis
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('inputText').addEventListener('keydown', e => {
    if (e.key === 'Enter') runDetection();
  });
});
