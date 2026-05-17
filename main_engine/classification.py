# from concurrent.futures import ThreadPoolExecutor, as_completed  
from collections import defaultdict
import re

def is_worth_scanning(sentence):
    s = sentence.strip()
    if len(s) < 10:
        return False
    if s.startswith(("import ", "export ", "const ", "let ", "var ", "//", "/*", "*", "}")):
        return False
    symbol_ratio = len(re.findall(r'[{}()\[\]<>:;=]', s)) / len(s)
    if symbol_ratio > 0.3:
        return False
    return True

def analyze_content(embedder, text, models, patterns):
    print("=== ANALYSIS STARTED ===", flush=True)
    sentences = [s for s in text.split("\n") if is_worth_scanning(s)][:300]

    if not sentences:
        return defaultdict(lambda: defaultdict(int))

    # step 1 — batch encode all sentences at once
    embeddings = embedder.encode(sentences, batch_size=128, show_progress_bar=False)

    # step 2 — batch predict all at once
    dt_preds = None
    sens_preds = None
    # child_preds = None

    for name, model in models.items():
        lname = name.lower()

        if "datatype" in lname:
            dt_preds = model.predict(embeddings)

        elif "sens" in lname:
            sens_preds = model.predict(embeddings)

        # elif "child" in lname:
        #     child_preds = model.predict(embeddings)

    detection_counts = defaultdict(lambda: defaultdict(int))

    # step 3 — count per sentence
    for sentence, datatype, sensitivity in zip(sentences, dt_preds, sens_preds):
        if datatype == "none":
            continue

        # regex for accurate instance counting
        if datatype in patterns:
            matches = re.findall(patterns[datatype], sentence)
            count   = len(matches) if matches else 1
        else:
            count = 1

        detection_counts[datatype][sensitivity] += count
        print("=== ANALYSIS END ===", flush=True)

    return detection_counts
