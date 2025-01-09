FROM python:3.12
LABEL authors="simonhardt"

# set the working directory
WORKDIR /app

# install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install gunicorn

#copy the scripts to the folder
COPY ./backend ./backend
COPY ./frontend ./frontend
# Expose the port your application will run on
EXPOSE 5000

# Define environment variable (if needed)
# for development I use .env files

# Run gunicorn when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "backend.app:create_app()"]