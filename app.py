import os

import uvicorn

from WebApplication import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app=app, host='0.0.0.0', port=port)
# Uses uvicoirn server
# uvicorn main:app --reload
# Swagger at following links
#   http://127.0.0.1:8000/redoc
#   http://127.0.0.1:8000/doc
# Video to audio converter tutorial :https://youtu.be/u5x5RZNtOqE
# MoviePy fill tutorial : https://youtu.be/2t0I0URiS40
# Google Cloud Path : https://www.cloudskillsboost.google/paths
