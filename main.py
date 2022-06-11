from program import Program
from os import environ

environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

app = Program()

try:
    app.run()
except Exception as err:
    print(err)
finally:
    # TODO: manage stopping all threads
    # since I have to stop all child threads
    # I might as well implement a notifications interface to stop all threads
    # on any error that might occur, that is if the error matters to me at all lmao
    # but that's not always the case
    app.cleanup()
