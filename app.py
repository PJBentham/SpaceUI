from datetime import datetime

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from llm_service import LLMServices

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///captains_log.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:5000")

# Initialize LLM Services
llm_services = LLMServices(socketio)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    entries = Log.query.all()
    return render_template('index.html', entries=entries)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data.get('message')
    try:
        message = llm_services.process_message(user_input)
        return jsonify({"response": True, "message": message})
    except Exception as e:
        print(e.__class__.__name__)
        error_message = f'Error: {str(e)}'
        return jsonify({"message": error_message, "response": False})

@app.route("/get_logs")
def get_logs():
    entries = Log.query.all()
    return render_template('logs_partial.html', entries=entries)

# Socket for updating logs
@socketio.on('submit_log')
def handle_submit_log(data):
    log_title = data.get('log_title')
    log_content = data.get('log_content')

    if log_title and log_content:
        new_log = Log(title=log_title, date=datetime.utcnow(), content=log_content)
        db.session.add(new_log)
        db.session.commit()
        socketio.emit('update_logs', broadcast=True)

# Socket for sending messages
@socketio.on('send_message')
def handle_message(data):
    user_input = data['message']
    message = llm_services.process_message(user_input)
    socketio.emit('receive_message', {'message': message})

if __name__ == '__main__':
    socketio.run(app)


# TODO: Voice Commands and Responses: Integrate voice recognition so users can speak to the onboard computer, and also have the computer's responses spoken out loud. This gives a more immersive and "futuristic" feel.
# TODO: Interactive Dashboard: The control panel on the left could show real-time or simulated data. For example, the engine power could fluctuate slightly, giving the illusion of real-time engine monitoring.
# TODO: System Alerts: Occasionally have the system generate "alerts" or "warnings" about various conditions, like a possible asteroid field ahead, low fuel, or a system malfunction. This could pop up as a flashing light or a special message in the communications panel.
# TODO: Star Map: An interactive map that shows the current location of the spaceship, its trajectory, and nearby points of interest like planets, stars, and other celestial objects.
# TODO: Crew Information: A panel that shows information about the crew on board. This could be a simple list of names, or more detailed profiles with pictures, roles (captain, engineer, scientist), and current tasks or statuses.
# TODO: Lighting Effects: Depending on certain commands or alerts, the UI could change its color scheme. For example, if there's an emergency, the control panel could glow red.
# TODO: Maintenance Logs & Reports: Users can access logs detailing system checks, any repair activities, and overall health of the spaceship systems.
# TODO: Entertainment Section: Since it's a long journey through space, maybe a section where crew members can access music, movies, or books stored in the spaceship's database.
# TODO: Virtual Assistant Personalization: Allow users to rename the onboard computer or choose from various "personalities" or themes.
# TODO: Outside View: Integrate a 'window' view that shows a simulation of what's outside the spaceship. This could be a dynamic background that changes depending on the ship's location or events.
# TODO: Science and Research Panel: Since the journey is also a scientific one, perhaps a section dedicated to experiments, observations, and research findings. Users can check the status or results of ongoing experiments.
# TODO: Mission Logs: A diary-like feature where users can document their journey, adding notes, images, and videos.
# TODO: Automated Tasks Scheduler: A panel where users can schedule tasks for the onboard computer to perform at specific times.
# TODO: Games & Simulations: Integrate some mini-games or simulations that users can play, related to space themes, of course.
# TODO: Integration with Real-world Data: Fetch real-time space data, like current positions of planets or known asteroids, and integrate them into the simulation.

