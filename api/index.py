from flask import Flask, render_template_string, request

app = Flask(__name__)

def advanced_sentiment_logic(text):
    # Expanded Weighted Dictionary for B.Tech Level Analysis
    scores = {
        # Highly Positive (+3)
        'excellent': 3, 'amazing': 3, 'perfect': 3, 'extraordinary': 3, 'outstanding': 3, 'spectacular': 3, 'love': 3, 'flawless': 3,
        # Positive (+1 to +2)
        'good': 1, 'nice': 1, 'happy': 1, 'success': 2, 'working': 1, 'fast': 1, 'great': 2, 'awesome': 2, 'smart': 2, 'cool': 1,
        'efficient': 2, 'reliable': 2, 'stable': 2, 'helpful': 1, 'brilliant': 2, 'innovative': 2, 'satisfied': 2, 'smooth': 1,
        # Highly Negative (-3)
        'terrible': -3, 'worst': -3, 'horrible': -3, 'hate': -3, 'disaster': -3, 'useless': -3, 'awful': -3, 'catastrophic': -3,
        # Negative (-1 to -2)
        'bad': -1, 'slow': -1, 'error': -2, 'failed': -2, 'broken': -2, 'difficult': -1, 'poor': -1, 'wrong': -1, 'sad': -1,
        'buggy': -2, 'annoying': -1, 'expensive': -1, 'useless': -2, 'complex': -1, 'unstable': -2, 'crash': -2, 'delay': -1
    }
    
    words = text.lower().split()
    total_score = 0
    found_words = 0
    
    for word in words:
        clean_word = "".join(char for char in word if char.isalnum())
        if clean_word in scores:
            total_score += scores[clean_word]
            found_words += 1
    
    if total_score >= 3: return "Highly Positive 🌟"
    elif total_score >= 1: return "Positive 😊"
    elif total_score <= -3: return "Highly Negative 😡"
    elif total_score <= -1: return "Negative ☹️"
    else: return "Neutral 😐"

@app.route('/', methods=['GET', 'POST'])
def home():
    analysis = None
    if request.method == 'POST':
        user_text = request.form.get('text_input')
        if user_text:
            sentiment = advanced_sentiment_logic(user_text)
            words = user_text.split()
            word_count = len(words)
            
            analysis = {
                "sentiment": sentiment,
                "count": word_count,
                "complexity": f"{round(sum(len(w) for w in words)/word_count, 1)} avg" if word_count > 0 else "0"
            }

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>NLP Text Analyzer</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: #0f172a; color: #f8fafc; font-family: 'Inter', sans-serif; padding-top: 100px; }
            .main-card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 40px; }
            .stat-card { background: #0f172a; border: 1px solid #334155; padding: 20px; border-radius: 8px; text-align: center; height: 100%; }
            .label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; font-weight: 600; display: block; margin-bottom: 10px; }
            .value { font-size: 1.15rem; color: #38bdf8; font-weight: 600; }
            textarea { background: #0f172a !important; color: white !important; border: 1px solid #475569 !important; border-radius: 8px !important; }
            textarea:focus { border-color: #38bdf8 !important; box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important; }
            .btn-cloud { background: #2563eb; color: white; font-weight: 600; border: none; border-radius: 8px; transition: 0.2s; }
            .btn-cloud:hover { background: #1d4ed8; transform: translateY(-1px); }
        </style>
    </head>
    <body>
        <div class="container" style="max-width: 750px;">
            <div class="main-card shadow-lg">
                <h2 class="text-center mb-5 text-white">☁️ NLP Text Analyzer</h2>
                
                <form method="POST">
                    <textarea name="text_input" class="form-control mb-4" rows="5" placeholder="Enter text for deep cloud analysis..." required></textarea>
                    <button class="btn btn-cloud w-100 py-3">RUN CLOUD INFERENCE</button>
                </form>
                
                {% if analysis %}
                <div class="mt-5 pt-4 border-top border-secondary">
                    <div class="row g-4">
                        <div class="col-md-4">
                            <div class="stat-card">
                                <span class="label">Sentiment</span>
                                <span class="value">{{ analysis.sentiment }}</span>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="stat-card">
                                <span class="label">Word Count</span>
                                <span class="value">{{ analysis.count }}</span>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="stat-card">
                                <span class="label">Complexity</span>
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
