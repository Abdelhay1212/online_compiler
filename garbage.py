import threading
import time

# Condition variable
condition = threading.Condition()


def pause_resume():
    with condition:
        print("Running... Press Enter to pause.")
        condition.wait()  # Pauses here until notified
        print("Resumed.")


thread = threading.Thread(target=pause_resume)
thread.start()

input("Press Enter to resume execution...")  # User input to resume
with condition:
    condition.notify()  # Notifies the thread to resume

thread.join()
