from flask import Flask, render_template_string, request

app = Flask(__name__)

def analyze_sentiment(text):
    # Dictionary-based logic (Zero-dependency for Cloud stability)
    positive_words = {'good', 'great', 'excellent', 'happy', 'love', 'amazing', 'best', 'working', 'success', 'cloud', 'awesome', 'smart', 'fast'}
    negative_words = {'bad', 'error', 'failed', 'sad', 'wrong', 'difficult', 'slow', 'hate', 'terrible', 'worst', 'poor', 'broken'}
    
    words = text.lower().split()
    score = 0
    for word in words:
        if word in positive_words: score += 1
        if word in negative_words: score -= 1
    
    if score > 0: return "Positive 😊", score
    elif score < 0: return "Negative ☹️", score
    else: return "Neutral 😐", score

@app.route('/', methods=['GET', 'POST'])
def home():
    analysis = None
    if request.method == 'POST':
        user_text = request.form.get('text_input')
        if user_text:
            sentiment, raw_score = analyze_sentiment(user_text)
            words = user_text.split()
            word_count = len(words)
            
            analysis = {
                "sentiment": sentiment,
                "score": f"{abs(raw_score)} pts",
                "count": word_count,
                "complexity": f"{round(sum(len(w) for w in words)/word_count, 1)} avg" if word_count > 0 else "0"
            }

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Serverless NLP Engine</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: #0f172a; color: #f8fafc; font-family: 'Inter', sans-serif; padding-top: 80px; }
            .main-card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 40px; }
            .stat-card { background: #0f172a; border: 1px solid #334155; padding: 15px; border-radius: 8px; text-align: center; }
            .label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; font-weight: 600; }
            .value { font-size: 1.1rem; color: #38bdf8; font-weight: 600; display: block; margin-top: 5px; }
            textarea { background: #0f172a !important; color: white !important; border: 1px solid #475569 !important; border-radius: 8px !important; }
            textarea:focus { border-color: #38bdf8 !important; box-shadow: none !important; }
            .btn-cloud { background: #1d4ed8; color: white; font-weight: 600; border: none; border-radius: 8px; transition: 0.2s; }
            .btn-cloud:hover { background: #1e40af; transform: translateY(-1px); }
        </style>
    </head>
    <body>
        <div class="container" style="max-width: 750px;">
            <div class="main-card shadow-lg">
                <h2 class="text-center mb-4">☁️ Serverless NLP Engine</h2>
                
                <form method="POST">
                    <textarea name="text_input" class="form-control mb-3" rows="5" placeholder="Enter text for deep cloud analysis..." required></textarea>
                    <button class="btn btn-cloud w-100 py-3">RUN CLOUD INFERENCE</button>
                </form>
                
                {% if analysis %}
                <div class="mt-5 pt-4 border-top border-secondary">
                    <div class="row g-3">
                        <div class="col-3">
                            <div class="stat-card">
                                <span class="label">Sentiment</span>
                                <span class="value">{{ analysis.sentiment }}</span>
                            </div>
                        </div>
                        <div class="col-3">
                            <div class="stat-card">
                                <span class="label">Intensity</span>
                                <span class="value">{{ analysis.score }}</span>
                            </div>
                        </div>
                        <div class="col-3">
                            <div class="stat-card">
                                <span class="label">Words</span>
                                <span class="value">{{ analysis.count }}</span>
                            </div>
                        </div>
                        <div class="col-3">
                            <div class="stat-card">
                                <span class="label">Avg Len</span>
                                <span class="value">{{ analysis.complexity }}</span>
                            </div>
                        </div>
                    </div>
                </div>
                {% endif %}
            </div>
        </div>
    </body>
    </html>
    ''', analysis=analysis)
