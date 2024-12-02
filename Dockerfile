FROM python:3.12-slim

WORKDIR /app

# Copy content of the git repo in the image
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# I think this is the standard port for Streamlit
EXPOSE 8501

# RUN adduser --disabled-password --gecos "" streamlituser \
#     && chown -R streamlituser:streamlituser /app
# USER streamlituser




# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]