from pathlib import Path
import re, json
ROOT = Path(__file__).resolve().parents[1]
p = ROOT / 'manuscript' / 'joi_letter_draft.md'
s = p.read_text()
body = s.split('**Main text:**', 1)[-1].split('**Declarations**', 1)[0]
words = re.findall(r"\b[\w’'-]+\b", body)
result = {
    'main_text_words': len(words),
    'internal_target_max': 1000,
    'internal_target_nominal': 980,
    'status': 'pass' if len(words) <= 1000 else 'fail'
}
(ROOT / 'reports').mkdir(parents=True, exist_ok=True)
(ROOT / 'reports' / 'word_count.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
