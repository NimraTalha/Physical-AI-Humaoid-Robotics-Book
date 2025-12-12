---
description: Generates text content using the Gemini Pro model based on a given prompt.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

Goal: Utilize the Gemini Pro model to generate text content based on the provided prompt.

Execution steps:

1.  Extract the prompt from `$ARGUMENTS`.
2.  Make a POST request to the `/api/gemini/generate` endpoint of the backend service.
    *   **Method**: `POST`
    *   **URL**: `http://localhost:8000/api/gemini/generate` (or the appropriate backend URL)
    *   **Headers**: `Content-Type: application/json`
    *   **Body**:
        ```json
        {
          "prompt": "Extracted prompt from $ARGUMENTS"
        }
        ```
3.  Parse the JSON response from the backend. Expected format:
    ```json
    {
      "response_text": "Generated content from Gemini"
    }
    ```
4.  Output the `response_text` to the user.

## Example Usage

To generate a short story:
`sp gemini_generate "Write a short story about a robot discovering art."`

## Expected Output

The generated short story from the Gemini model.
