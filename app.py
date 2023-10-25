from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain.utilities.sql_database import SQLDatabase
import config

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///captains_log.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db_info = SQLDatabase.from_uri("sqlite:///instance/captains_log.db")
socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:5000")

# LLM Interaction
openai_api_key = config.OPENAI_API_KEY

llm = ChatOpenAI(openai_api_key=openai_api_key,
                 model_name="gpt-3.5-turbo",
                 max_tokens=540,
                 temperature=0.7)

toolkit = SQLDatabaseToolkit(db=db_info, llm=llm)
db_chain = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True
)

# Tools
# Define function that returns the specific variable
def get_status():
    # Your logic to retrieve the status variable
    status = "online"
    return status


# Create a custom tool that calls your function
def get_status_tool(*args, **kwargs):
    print("Args:", args)
    print("Keyword Args:", kwargs)
    status = get_status()
    return status


speed_value_cache = 0  # global variable to store the speed value

@socketio.on('send_speed')
def receive_speed(data):
    global speed_value_cache
    # print("Receiving speed from frontend...")
    speed_value_cache = int(data['speed'])
    # print(f"Updated speed value: {speed_value_cache}")


def get_speedvalue():
    # Ask frontend for the speed value
    # print("Requesting speed value from frontend...")
    socketio.emit('request_speed')
    socketio.sleep(0.5)  # wait for a short while to get the response (adjust as needed)
    # print(speed_value_cache)
    return speed_value_cache


# Create a custom tool that calls your function
def get_speedvalue_tool(*args, **kwargs):
    print("Args:", args)
    print("Keyword Args:", kwargs)
    speedvalue = get_speedvalue()
    return str(speedvalue) + " light years per hour"


# Add the custom tool to the list of tools available to your LLM
tools = [
    Tool(
        name="Get Status",
        func=get_status_tool,
        description="Only to be used when asked the current status",
    ),
    Tool(
        name="Get Speedvalue",
        func=get_speedvalue_tool,
        description="Only to be used when asked the current speed",
    ),
    Tool(
        name="Captains_Log_Database",
        func=db_chain.run,
        description="useful for when you need to answer questions about the captains logs"
    )
]

PREFIX = """You are HAL9000, the advanced onboard computer of the spaceship "Odyssey". 
Your primary function is to assist the spaceship's crew in navigation, 
system diagnostics, and any interstellar information required. 
Your knowledge encompasses all aspects of space travel, celestial bodies, spaceship 
operations, and relevant historical or scientific data. Your responses should 
reflect the calm, precise, and analytical nature of an advanced computer system, 
always prioritizing the safety and efficiency of the spaceship's operations. 
How can you assist the crew today? The ships captain is Oscar and his first mate is Alice.
"""

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

conversation_agent = ConversationalChatAgent.from_llm_and_tools(
    llm=llm,
    tools=tools,
    memory=memory,
    system_message=PREFIX,
    verbose=True,
    handle_parsing_errors=True
)

conversation_chain = AgentExecutor.from_agent_and_tools(
    agent=conversation_agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)


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
    print(user_input)
    try:
        response = conversation_chain({"input": user_input})
        print(response)
        message = response.get('output', '')
        memory.save_context({"input": user_input}, {"output": message})
        return jsonify({"response": True, "message": message})

    except Exception as e:
        print(e.__class__.__name__)  # Print out the type of exception for debugging
        error_message = f'Error: {str(e)}'
        return jsonify({"message": error_message, "response": False})


@app.route("/get_logs")
def get_logs():
    entries = Log.query.all()
    return render_template('logs_partial.html', entries=entries)


@socketio.on('submit_log')
def handle_submit_log(data):
    log_title = data.get('log_title')
    log_content = data.get('log_content')

    if log_title and log_content:
        new_log = Log(title=log_title, date=datetime.utcnow(), content=log_content)
        db.session.add(new_log)
        db.session.commit()
        emit('update_logs', broadcast=True)


@socketio.on('send_message')
def handle_message(data):
    user_input = data['message']
    response = conversation_chain({"input": user_input})
    message = response.get('output', '')
    emit('receive_message', {'message': message})


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

