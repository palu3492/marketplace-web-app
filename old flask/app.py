from flask import Flask, request, Response, render_template
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Regexp, ValidationError
import re


def pattern_equal_to_length(form, field):
    length = form.length.data
    pattern = form.pattern.data
    if length != '' and pattern != '':
        if len(pattern) != int(length):
            raise ValidationError('If length chosen and pattern supplied then pattern length must equal chosen length')

def pattern_required_no_letters(form, field):
    letters = form.avail_letters.data
    pattern = form.pattern.data
    if len(letters) == 0 and len(pattern) == 0:
        raise ValidationError('If no letters are provided then a pattern is required')

class WordForm(FlaskForm):
    avail_letters = StringField("Letters", validators= [
        Regexp(r'^[a-zA-Z]*$', message="Must contain letters only"),
        pattern_required_no_letters
    ])

    # [ ('3', '3'), ('4', '4'), ... ]
    possible_lengths = [("", "")] + [(str(i), str(i)) for i in range(3, 11)]
    # length select (drop down) input field
    length = SelectField("Length of words", choices=possible_lengths, validators=[
        pattern_equal_to_length
     ])

    # RegEx pattern input field
    pattern = StringField("Pattern", validators=[
        Regexp(r'^[\.a-zA-Z]*$', message="Must contain letters or . only")
    ])

    submit = SubmitField("Go")


csrf = CSRFProtect()
app = Flask(__name__)
app.config["SECRET_KEY"] = "row the boat"
csrf.init_app(app)

@app.route('/')
@app.route('/index')
def index():
    form = WordForm()
    return render_template("index.html", form=form, name="CS4131")


@app.route('/words', methods=['POST','GET'])
def letters_2_words():

    form = WordForm()
    if form.validate_on_submit():
        letters = form.avail_letters.data
        length = form.length.data  # possibilities: 3 - 10
        pattern = form.pattern.data  # letters or periods
    else:
        return render_template("index.html", form=form)

    with open('sowpods.txt') as f:
        good_words = set(x.strip().lower() for x in f.readlines())

    word_set = set()

    if letters:
        if length == '':
            # permutations of letters to words of any length
            # for loop here
            for l in range(3, len(letters) + 1):
                word_set.update(words_from_length(letters, l, good_words))
        else:
            # permutations of letters to words of specific length
            word_set.update(words_from_length(letters, int(length), good_words))
    else:
        # all words
        if length == '':
            word_set.update(good_words)
        else:
            for word in good_words:
                if len(word) == int(length):
                    word_set.add(word)

    if pattern:
        if length == '':
            word_set = words_from_pattern(pattern, word_set)
        else:
            if len(pattern) == int(length):
                word_set = words_from_pattern(pattern, word_set)

    no_words = ''
    if len(word_set) == 0:
        no_words = 'No words found for letters ['+','.join(letters)+"] at length '"+length+"' with pattern '"+pattern+"'"

    # Sort words by length (shortest ot longest) then sort alphabetically
    return render_template(
        'wordlist.html',
        wordlist=sorted(word_set, key=lambda item: (len(item), item)),
        name="CS4131",
        nowords=no_words
    )


# Returns words made from supplied letters that are of supplied length
def words_from_length(letters, length, good_words):
    words = set()
    for word in itertools.permutations(letters, length):
        w = "".join(word)
        # check if permutation of letters is a word in our acceptable list of words
        if w in good_words:
            words.add(w)
    return words


# Returns words that match supplied RegEx pattern
def words_from_pattern(pattern, word_set):
    words = set()
    for word in word_set:
        match = re.search(r'^' + pattern + r'$', word)
        if match:
            words.add(word)
    return words


@app.route('/proxy')
def proxy():
    result = requests.get(request.args['url'])
    resp = Response(result.text)
    resp.headers['Content-Type'] = 'application/json'
    print(resp)
    return resp


@app.route('/definition')
def definition():
    word = request.args['word']
    key = 'b61a76f9-8580-4107-96e6-83c93eb5f3d6'
    api = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/'
    url = api + word + '?key=' + key
    result = requests.get(url)

    response_string = api_result_to_response(result.json(), word)

    response = Response(response_string)
    response.headers['Content-Type'] = 'text/plain'
    return response


def api_result_to_response(def_dict, word):
    response_string = 'Definition of ' + word + ' not found'
    for i in def_dict:
        # tmp_word = i['meta']['id'].split(':')[0]
        # print(tmp_word)
        # print(word)
        # if tmp_word == word:
        tmp_defs = i['shortdef']
        if len(tmp_defs) > 0:
            response_string = ''
            n = 0
            for tmp_def in tmp_defs:
                response_string += '<p>' + str(n+1) + '. ' + tmp_def + '</p>'
                n += 1
            break
    return response_string
