# Code Snippet Generator

## Prerequisites

- Python 3.8 or higher
- Docker

## Setup CodeLLama

1. **Install Ollama**:
   Use the documentation to download Ollama and install it here: [Install Ollama](https://github.com/ollama/ollama)

2. **Pull the CodeLLama model to use it locally:**
    ```bash
    ollama pull codellama

3. **Serve the model**
    ```bash
    ollama serve


Visit http://localhost:11434 (default) to confirm it's running.

## Running the Application with Docker

1. **Build the Docker image**:
   ```bash
   docker build -t code-snippet-generator .

2. **Run the application:**
    ```bash
   docker run -p 5000:5000 code-snippet-generator

Access the application at http://localhost:5000.

## Running the Application Locally with Python

1. **Install Dependencies**:
   Ensure all required Python packages are installed by running:
   ```bash
   pip install -r requirements.txt

2. **Start the Application:**
Run the Python application using:
    ```bash
    python main.py

3. **Access the Application:**
Open your web browser and visit http://localhost:5000 to interact with the application.

## Using the Application

1. **Generate Code:**
 Provide a description of your coding problem and click "Generate Code" to view the solution.

2. **Feedback:** Rate the generated code and provide feedback for improvements.

3. **Review and Delete Snippets:**
 Easily view, review, and delete previously generated snippets from the application interface.