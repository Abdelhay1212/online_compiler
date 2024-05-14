import io
import sys
import queue
import asyncio

from flask import request
from flask_socketio import emit
from .exstensions import socketio

input_queue = queue.Queue()


@socketio.on('connection')
def handle_connection(data: dict) -> None:
    print(data['data'])


class RealtimeOutput(io.StringIO):
    def write(self, s):
        super().write(s)
        emit('code_output', {'output': s})


def simulate_input(prompt: str = '') -> str:
    # print the prompt of the input function
    print(prompt, end='')
    # get the input from the user
    emit('get_input')
    # wait for the input value
    # get the value from the queue
    user_input = input_queue.get(block=True)
    return user_input


@socketio.on('code_submitted')
def execute_code(code: str) -> None:
    # redirect stdout to capture it
    old_stdout = sys.stdout
    sys.stdout = captured_output = RealtimeOutput()

    try:
        byte_code = compile(code, filename='<inline code>', mode='exec')
        # execute the code using exec
        exec(byte_code, {'input': simulate_input})
    except Exception as e:
        emit('code_output', {'output': f"Error: {e}\n"})
    finally:
        sys.stdout = old_stdout
        captured_output.close()
        with input_queue.mutex:
            input_queue.queue.clear()

    emit('code_execution_complete', {'status': 'Code Execution Successful'})


@socketio.on('input_value')
def get_value(data: str) -> None:
    # store the value in the queue
    input_queue.put(data)
