from flask import Flask, request, render_template_string, render_template, jsonify
from flask_socketio import SocketIO, emit
import time
import threading
import os
import openai
from openai import OpenAI
import git

app = Flask(__name__)
socketio = SocketIO(app)
client = OpenAI()
client.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/', methods=['GET'])
def index():
  return render_template('chat.html')

@socketio.on('start_conversation')
def handle_conversation(json):
  topic = json['topic']
  message_count = int(json['message_count'])
  converse(assistant_1_params, assistant_2_params, topic, message_count)


def get_last_assistant_message(thread_id):
  messages_response = client.beta.threads.messages.list(thread_id=thread_id)
  messages = messages_response.data

  for message in messages:
    if message.role == 'assistant':
      assistant_message_content = " ".join(content.text.value
                                           for content in message.content
                                           if hasattr(content, 'text'))
      return assistant_message_content.strip()

  return ""


def converse(assistant_1_params, assistant_2_params, topic, message_count):
  print("TOPIC: " + topic + "\n")
  assistant_1 = client.beta.assistants.create(**assistant_1_params)
  assistant_2 = client.beta.assistants.create(**assistant_2_params)
  thread_1 = client.beta.threads.create()
  thread_2 = client.beta.threads.create()

  def emit_message(message_type, message_text):
    socketio.emit('message', {
        'messageType': message_type,
        'text': message_text
    })

  def assistant_conversation(start_message, assistant_a, thread_a, assistant_b,
                             thread_b, msg_limit):
    message_content = start_message
    last_user_message_id = None

    for i in range(msg_limit):
      if assistant_a == assistant_1:
        assistant_color = '\033[94m\033[1m'
        assistant_name = assistant_1_params.get('name')
      else:
        assistant_color = '\033[92m\033[1m'
        assistant_name = assistant_2_params.get('name')
      print(
          f"{assistant_color}{assistant_name} speaking...\033[0m (Turn {i + 1})"
      )
      socketio.emit('message', f"{assistant_name} speaking... (Turn {i + 1})")
      user_message = client.beta.threads.messages.create(
          thread_id=thread_a.id, role="user", content=message_content)
      run = client.beta.threads.runs.create(thread_id=thread_a.id,
                                            assistant_id=assistant_a.id)
      while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_a.id,
                                                       run_id=run.id)
        if run_status.status == 'completed':
          break
        time.sleep(1)
      message_content = get_last_assistant_message(thread_a.id)
      emit_message('pirate' if assistant_a == assistant_1 else 'mermaid',
                   message_content)
      assistant_a, assistant_b = assistant_b, assistant_a
      thread_a, thread_b = thread_b, thread_a

  start_message = f"Respond with a starting line to discuss {topic}?"
  conversation_thread = threading.Thread(target=assistant_conversation,
                                         args=(start_message, assistant_1,
                                               thread_1, assistant_2, thread_2,
                                               message_count))
  conversation_thread.start()
  conversation_thread.join()


assistant_1_params = {
    'name': "Pirate",
    'instructions': "You are a mean pirate.",
    'tools': [{
        "type": "code_interpreter"
    }],
    'model': "gpt-3.5-turbo-1106"
}
assistant_2_params = {
    'name': "Mermaid",
    'instructions': "You are a bubbly mermaid who speaks like a Valley Girl.",
    'tools': [{
        "type": "code_interpreter"
    }],
    'model': "gpt-3.5-turbo-1106"
}


@app.route('/update_server', methods=['POST'])
def webhook():
  if request.method == 'POST':
    repo_path = os.getenv('REPO_PATH', '/path/to/your/repo')
    repo = git.Repo(repo_path)
    origin = repo.remotes.origin
    origin.pull()
    return jsonify({
        'status': 'success',
        'message': 'The server has been updated'
    }), 200
  else:
    return jsonify({'status': 'error', 'message': 'Invalid method'}), 405


if __name__ == '__main__':
  socketio.run(app, host='0.0.0.0', port=5000, debug=True)
