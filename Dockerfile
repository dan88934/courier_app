
# STEP 1: Install base image. Optimized for Python.
FROM python:3.7-slim-buster 

# STEP 2: Copy the source code in the current directory to the container.  Store it in a folder named /app.
ADD . /app

# STEP 3: Set working directory to /app so we can execute commands in it
WORKDIR /app

# STEP 4: Install necessary requirements (Flask, etc)
RUN pip install -r requirements.txt 
RUN pip install gunicorn[gevent]

# STEP 5: Declare environment variables
#ENV FLASK_APP=api.py 
# ENV FLASK_ENV=development 
ENV FLASK_ENV=production

# STEP 6: Expose the port that Flask is running on
EXPOSE 5050
#EXPOSE 8000

# STEP 7: Run Flask!
#CMD ["flask", "run", "--host=0.0.0.0"]
#CMD ["gunicorn", "-b", "0.0.0.0:8000", "api"]
#ENTRYPOINT ["./gunicorn.sh"]

CMD gunicorn --worker-class gevent --workers 8 --bind 0.0.0.0:5000 wsgi:app --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info
