# Telegramify Markdown API

A FastAPI wrapper for the [telegramify-markdown](https://github.com/sudoskys/telegramify-markdown) Python library that converts text to Telegram-formatted markdown.

## API Endpoints

### POST /markdownify

Converts text to markdown format using the markdownify function.

**Request Body:**
```json
{
  "text": "Your text here"
}
```

**Response:**
```json
{
  "result": "Markdown formatted text"
}
```

### POST /telegramify

Splits long text into multiple chunks, converts format and can render code blocks to files/images. Returns a list of content items with different types (TEXT, PHOTO, FILE, etc.). Ideal for LLM bot developers who need advanced content processing.

**Request Body:**
```json
{
  "text": "Your text here"
}
```

**Response:**
```json
{
  "result": [
    {
      "type": "TEXT",
      "content": "Processed text content"
    },
    {
      "type": "PHOTO", 
      "content": "base64_image_data",
      "caption": "Image caption"
    }
  ]
}
```

### POST /standardize

Standardizes text formatting using the standardize function.

**Request Body:**
```json
{
  "text": "Your text here"
}
```

**Response:**
```json
{
  "result": "Standardized text"
}
```

### GET /

Health check endpoint.

## Quick Start

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Using Docker

1. Build the image:
```bash
docker build -t telegramify-markdown-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 telegramify-markdown-api
```

### Using pre-built image from GitHub Container Registry

```bash
docker run -p 8000:8000 ghcr.io/vladimish/telegramify-markdown-api:latest
```

## API Documentation

Once the application is running, you can access:
- OpenAPI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Example Usage

### Markdownify endpoint:
```bash
curl -X POST "http://localhost:8000/markdownify" \
     -H "Content-Type: application/json" \
     -d '{"text": "**Bold text** and *italic text*"}'
```

### Telegramify endpoint:
```bash
curl -X POST "http://localhost:8000/telegramify" \
     -H "Content-Type: application/json" \
     -d '{"text": "# Title\n**Bold text** with code:\n```python\nprint(\"Hello\")\n```"}'
```

Example response:
```json
{
  "result": [
    {
      "type": "TEXT",
      "content": "# Title\n*Bold text* with code:"
    },
    {
      "type": "FILE",
      "content": "print(\"Hello\")",
      "filename": "code.py"
    }
  ]
}
```

### Standardize endpoint:
```bash
curl -X POST "http://localhost:8000/standardize" \
     -H "Content-Type: application/json" \
     -d '{"text": "**Bold text** and *italic text*"}'
```

Example response:
```json
{
  "result": "Processed text output"
}
```

## License

This project is licensed under the MIT License.