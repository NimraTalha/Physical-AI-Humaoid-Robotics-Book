---
description: Conducts a chat completion using the Gemini Pro model based on chat history and a new message.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

Goal: Engage in a chat conversation using the Gemini Pro model, maintaining context through chat history.

Execution steps:

1.  Parse `$ARGUMENTS` to extract `history` (JSON string or similar) and the `message` for the current turn.
    *   **Note**: The `$ARGUMENTS` format for history might need a specific structure (e.g., a base64 encoded JSON string, or a file path to a JSON file). For simplicity here, assume `$ARGUMENTS` contains the new message, and history management is external or via a predefined convention. A more robust implementation would involve a structured input for history.
    *   For this documentation, assume the user provides the *current message* as `$ARGUMENTS`, and `sp` is expected to manage the history internally or retrieve it from a context.
2.  Make a POST request to the `/api/gemini/chat` endpoint of the backend service.
    *   **Method**: `POST`
    *   **URL**: `http://localhost:8000/api/gemini/chat` (or the appropriate backend URL)
    *   **Headers**: `Content-Type: application/json`
    *   **Body**:
        ```json
        {
          "history": [
            {"role": "user", "parts": ["Previous user message."]},
            {"role": "model", "parts": ["Previous model response."]}
          ],
          "message": "Extracted message from $ARGUMENTS"
        }
        ```
        *   **Note**: The `history` array would be populated by the `sp` command's logic, likely storing previous interactions.
3.  Parse the JSON response from the backend. Expected format:
    ```json
    {
      "response_text": "Generated chat response from Gemini"
    }
    ```
4.  Output the `response_text` to the user.

## Example Usage

Assuming `sp` manages chat history:
`sp gemini_chat "What is the capital of France?"`

If history needs to be passed: (This is a simplified example, actual JSON parsing for history might be complex for CLI)
`sp gemini_chat --history '[{"role": "user", "parts": ["Hello."]}, {"role": "model", "parts": ["Hi there!"]}]' --message "How are you?"`

## Expected Output

The generated chat response from the Gemini model.
