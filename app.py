from flask import Flask, request, render_template, render_template_string, jsonify, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# HTML content for the feedback page
feedback_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Arecanut Leaf Disease Detection</title>
  <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background-color: #f0f0f0; color: #000; }
    .container { margin-top: 50px; }
    .navbar-brand img { border-radius: 50%; width: 70px; }
    .navbar-nav { margin-left: auto; }
    .nav-link { color: #fff !important; transition: color 0.3s; }
    .nav-link:hover { color: #28a745 !important; text-decoration: underline; }
    .active .nav-link { color: #28a745 !important; text-decoration: underline; }
    .jumbotron { background-color: rgba(255, 255, 255, 0.7); padding: 50px; border-radius: 20px; }
    .jumbotron h1 { font-size: 2.5rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .jumbotron p { font-size: 1.25rem; }
    .btn-get-started { background-color: #007bff; border-color: #007bff; font-weight: bold; }
    .btn-get-started:hover { background-color: #0056b3; border-color: #0056b3; }
    .form-group textarea { resize: none; height: 100px; max-height: 100px; }
    #feedbackMessage { margin-top: 20px; }
  </style>
</head>
<body>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <a class="navbar-brand" href="{{ url_for('home') }}"><img src="{{ url_for('static', filename='areca seed.jfif') }}" alt="Arecanut Disease Detection Logo"></a>
      <ul class="navbar-nav">
        <li class="nav-item"><a class="nav-link" href="{{ url_for('home') }}">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="{{ url_for('help') }}">Help</a></li>
        <li class="nav-item"><a class="nav-link" href="{{ url_for('contact') }}">Contact</a></li>
        <li class="nav-item active"><a class="nav-link" href="{{ url_for('feedback_form') }}">Feedback</a></li>
      </ul>
    </div>
  </nav>
  <div class="container">
    <div class="jumbotron text-center">
      <h1 class="display-4">We'd Love to Hear Your Feedback</h1>
      <p class="lead">Please provide your valuable feedback below:</p>
      <hr class="my-4">
      <form id="feedbackForm" method="post">
        <div class="form-group">
          <label for="emailInput">Your Email:</label>
          <input type="email" class="form-control" id="emailInput" name="email" placeholder="Enter your email" required>
        </div>
        <div class="form-group">
          <label for="feedbackTextarea">Your Feedback:</label>
          <textarea class="form-control" id="feedbackTextarea" name="feedback" rows="3" placeholder="Please enter your Feedback" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary btn-lg">Submit</button>
      </form>
      <div id="feedbackMessage" style="display: none;" class="alert alert-success"></div>
    </div>
  </div>
  <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
  <script>
    $(document).ready(function() {
      $('#feedbackForm').on('submit', function(event) {
        event.preventDefault(); // Prevent form from submitting the default way
        $.ajax({
          type: 'POST',
          url: '{{ url_for("submit_feedback") }}',
          data: $(this).serialize(),
          success: function(response) {
            $('#feedbackMessage').text(response).show();
            $('#feedbackForm')[0].reset(); // Clear form fields
          },
          error: function() {
            $('#feedbackMessage').text('Failed to send feedback. Please try again later.').show();
          }
        });
      });
    });
  </script>
</body>
</html>
'''

@app.route('/')
def home():
   return render_template('home.html')


@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/feedback')
def feedback_form():
    return render_template('feedback.html')

@app.route('/login_signup')
def login_signup():
    return render_template('login_signup.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    user_email = request.form['email']
    user_feedback = request.form['feedback']
    
    # Email details
    sender_email = "arecanutofficialsite08@gmail.com"
    receiver_email = "varshithshetty8@gmail.com"
    subject = "New Feedback from Your Website"
    body = f"User Email: {user_email}\nFeedback: {user_feedback}"

    # Create email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, "xkon xkkr tdca pxwv")  # Use the generated app password here
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.close()
        return jsonify("Thank you for your feedback!")
    except Exception as e:
        print(e)
        return jsonify("Failed to send feedback. Please try again later."), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
