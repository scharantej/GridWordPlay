
from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

grid = [[' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ']]

words = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_grid', methods=['POST'])
def generate_grid():
    global words
    words = request.form.getlist('words')

    for word in words:
        # Randomly select a starting position for the word in the grid
        x = random.randint(0, 3)
        y = random.randint(0, 3)

        # Determine the direction in which the word will be placed
        direction = random.choice(['horizontal', 'vertical'])

        # Check if the word fits in the grid in the selected direction
        if direction == 'horizontal':
            if x + len(word) <= 4:
                # Place the word in the grid horizontally
                for i in range(len(word)):
                    grid[x][y + i] = word[i]
            else:
                # The word doesn't fit horizontally, so try vertically
                if y + len(word) <= 4:
                    for i in range(len(word)):
                        grid[x + i][y] = word[i]
        else:
            if y + len(word) <= 4:
                # Place the word in the grid vertically
                for i in range(len(word)):
                    grid[x + i][y] = word[i]
            else:
                # The word doesn't fit vertically, so try horizontally
                if x + len(word) <= 4:
                    for i in range(len(word)):
                        grid[x][y + i] = word[i]

    # Fill the remaining empty spaces in the grid with random letters
    for i in range(4):
        for j in range(4):
            if grid[i][j] == ' ':
                grid[i][j] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    # Prepare the HTML response with the generated grid
    html = '<table>'
    for row in grid:
        html += '<tr>'
        for cell in row:
            html += f'<td>{cell}</td>'
        html += '</tr>'
    html += '</table>'

    return html

@app.route('/check_answers', methods=['POST'])
def check_answers():
    global words

    # Get the user's answers from the request
    answers = request.form.getlist('answers')

    # Check if the user's answers match the hidden words
    correct_answers = []
    for answer in answers:
        if answer in words:
            correct_answers.append(answer)

    # Prepare the HTML response with the results
    html = '<h1>Results</h1>'
    html += '<h2>Correct Answers:</h2>'
    html += '<ul>'
    for answer in correct_answers:
        html += f'<li>{answer}</li>'
    html += '</ul>'
    html += '<h2>Incorrect Answers:</h2>'
    html += '<ul>'
    for answer in answers:
        if answer not in correct_answers:
            html += f'<li>{answer}</li>'
    html += '</ul>'

    return html

if __name__ == '__main__':
    app.run(debug=True)
