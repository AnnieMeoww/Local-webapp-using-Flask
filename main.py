from flask import Flask, render_template, request, escape
from vsearch4web import search4letters

app = Flask(__name__)

def log_request(req, res):
  with open('vsearch.log', 'a') as log:
    print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')
  
@app.route('/search4', methods=['POST'])
def do_search() -> str:
 phrase = request.form['phrase']
 letters = request.form['letters']
 title = 'Here are your results: '
 results = str(search4letters(phrase, letters))
 log_request(request, results)
 return render_template('results.html', the_phrase = phrase, the_letters = letters, the_title = title, the_results = results)

@app.route('/')
@app.route('/entry')
def entry_page():
  return render_template('entry.html', the_title='Welcome to search4letters on the web!')

@app.route('/viewlog')
def view_the_log():
  contents = []
  with open('vsearch.log') as log:
    for line in log:
      contents.append([])
      for item in line.split('|'):
        contents[-1].append(escape(item))
  titles = ('Form data', 'Remote_addr', 'User_agent', 'Results')
  return render_template('viewlog.html', the_title='View Log', the_row_titles=titles, the_data=contents)
    
app.run(host='0.0.0.0', port=5000, debug=True)

