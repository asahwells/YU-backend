FROM python:3.11-slim

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user . $HOME/app

# Install requirements
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Set the port to 7860 (required by Hugging Face Spaces)
ENV PORT=7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]