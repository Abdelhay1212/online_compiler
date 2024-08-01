import io
import sys
import queue
import multiprocessing

from flask_socketio import emit
from .exstensions import socketio
from .safe_builtins import is_code_allowed

input_queue = queue.Queue()


@socketio.on('connection')
def handle_connection(data: dict) -> None:
    emit('connected', {'data': data['data']})


class OutputStream(io.StringIO):
    def write(self, s):
        super().write(s)
        emit('code_output', {'output': s})


def _input_(prompt: str = '') -> str:
    # print the prompt of the input function
    print(prompt, end='')
    # get the input from the user
    emit('get_input')
    # wait for the input value
    # get the value from the queue
    user_input = input_queue.get(block=True)
    return user_input


@socketio.on('code_submitted')
def execute_code(data: dict) -> None:
    code = data.get('code', '')
    # redirect stdout to capture it
    old_stdout = sys.stdout
    sys.stdout = captured_output = OutputStream()

    try:
        # checkes if the code includes unallowed
        # function or module then it throughs an exception
        is_allowed = is_code_allowed(code)
        if not is_allowed[0]:
            raise Exception(is_allowed[1])

        # compile the code
        byte_code = compile(
            code, filename='<inline code>', mode='exec')

        # execute the code using exec
        exec(byte_code, {'input': _input_})

        # the end of the execution
        emit(
            'code_execution_complete',
            {'status': 'Code Execution Successful'}
        )
    except Exception as e:
        # execution fail
        # print the errors
        emit('code_output', {'output': f"Error: {e}\n"})
        emit(
            'code_execution_complete',
            {'status': 'Code Exited With Errors'}
        )
    finally:
        sys.stdout = old_stdout
        captured_output.close()
        with input_queue.mutex:
            input_queue.queue.clear()


@socketio.on('input_value')
def get_value(data: dict) -> None:
    value = data.get('value', '')
    # store the value in the queue
    input_queue.put(value)
