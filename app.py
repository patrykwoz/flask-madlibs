from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from stories import Story

app = Flask(__name__)
app.config['SECRET_KEY'] = 'madlib-secret'

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    questions =  request.args.get('story-questions')
    story_text = request.args.get('story-text')

    if questions and story_text:
        story = Story(questions.split(', '), story_text)
    else:
        story = Story(
            ["place", "noun", "verb", "adjective", "plural_noun"],
            """Once upon a time in a {place}, there lived a
            large {adjective} {noun}. It loved to {verb} {plural_noun}."""
        )

        

    return render_template('home.html', story = story, questions=questions, story_text = story_text)

@app.route('/form')
def form_page():
    return render_template('form.html')

@app.route('/story')
def story_page():
    request_dict = request.args.to_dict()
    if 'st-template' in request_dict:
        del request_dict['st-template']
    questions = list(request_dict.keys())
    answers = list(request_dict.values())
    story_template= request.args.get('st-template')
    story = Story(questions, story_template)
    gen_story = story.generate(request_dict) 

    return render_template('story.html', story=story, gen_story=gen_story)