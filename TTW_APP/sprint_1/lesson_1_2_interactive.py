import json
import os
import urllib.request
from urllib.error import HTTPError, URLError


# The URL where OpenRouter hosts its chat completion API endpoint.
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# The specific AI model we want to use. This is a free tier model available on OpenRouter.
MODEL_NAME = "poolside/laguna-m.1:free"


def _load_env_file():
    """Load environment variables from a local .env file if present."""
    # Try to use python-dotenv library if it's installed (easier method).
    try:
        from dotenv import load_dotenv
        # load_dotenv() reads the .env file and stores variables in os.environ automatically.
        load_dotenv()
        # Exit this function early since we successfully loaded the .env file.
        return
    except Exception:
        # If python-dotenv is not installed, continue to the fallback method below.
        pass

    # Fallback method: manually parse the .env file if it exists in the parent directory.
    # os.path.dirname(__file__) gets the directory where this script is located (sprint_1/).
    # ".." goes up one level to the TTW_APP root directory.
    # Then we look for a ".env" file in that root directory.
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
    
    # Check if the .env file actually exists before trying to read it.
    if os.path.exists(env_path):
        try:
            # Open and read the .env file with UTF-8 encoding to handle special characters.
            with open(env_path, "r", encoding="utf-8") as fh:
                # Process each line in the .env file one by one.
                for line in fh:
                    # Remove leading and trailing whitespace from the line.
                    line = line.strip()
                    # Skip empty lines and lines that start with # (comments in .env files).
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    # Split the line into key and value at the first "=" sign.
                    key, value = line.split("=", 1)
                    # Remove whitespace from the key name.
                    key = key.strip()
                    # Remove whitespace from the value and also strip quotes if present.
                    value = value.strip().strip('"').strip("'")
                    # Store the key-value pair in os.environ only if it's not already set.
                    os.environ.setdefault(key, value)
        except Exception:
            # If anything goes wrong reading the file, just continue silently.
            pass


# Call the load function when this module is imported, so credentials are ready.
_load_env_file()


def call_openrouter(prompt: str) -> str:
    """Send a single prompt to OpenRouter and return just the assistant's text response."""
    # Retrieve the API key from the environment variable.
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    # If no API key was found, raise an error to inform the user.
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Add it to your environment or .env file."
        )

    # Build the request payload as a Python dictionary with the required structure.
    payload = {
        # Specify which AI model to use (OpenRouter offers multiple models).
        "model": MODEL_NAME,
        # Include the user's prompt in a messages list with the "user" role.
        "messages": [{"role": "user", "content": prompt}],
    }

    # Create an HTTP request object with the proper headers and data.
    request = urllib.request.Request(
        # The destination URL for the API call.
        API_URL,
        # Convert the Python dictionary to JSON text and then to bytes for transmission.
        data=json.dumps(payload).encode("utf-8"),
        # Set the HTTP headers required by OpenRouter.
        headers={
            # Bearer token authentication: "Bearer " followed by our API key.
            "Authorization": f"Bearer {api_key}",
            # Tell the server we're sending JSON data.
            "Content-Type": "application/json",
        },
        # Specify this is a POST request (we're sending data, not retrieving).
        method="POST",
    )

    # Try to execute the HTTP request and handle any errors that occur.
    try:
        # urlopen() sends the request and waits for a response (60 second timeout to avoid hanging).
        with urllib.request.urlopen(request, timeout=60) as response:
            # Read the response body and decode it from bytes to a text string.
            raw_response = response.read().decode("utf-8")
    # If the server returns an HTTP error (4xx, 5xx), catch it here.
    except HTTPError as exc:
        # Convert the HTTP error into a more user-friendly error message.
        raise RuntimeError(f"OpenRouter request failed: {exc.code} {exc.reason}") from exc
    # If there's a network connection problem, catch it here.
    except URLError as exc:
        # Convert the network error into a more user-friendly error message.
        raise RuntimeError(f"OpenRouter connection failed: {exc.reason}") from exc

    # Parse the JSON response text back into a Python dictionary.
    response_data = json.loads(raw_response)
    
    # Try to extract the assistant's text response from the nested structure.
    try:
        # Navigate the response structure: choices[0] is the first result, 
        # message is the response content, and content is the actual text.
        return response_data["choices"][0]["message"]["content"]
    # If the response has an unexpected structure, catch the error.
    except (KeyError, IndexError, TypeError) as exc:
        # Raise a descriptive error showing the raw response to help with debugging.
        raise ValueError(f"Unexpected OpenRouter response format: {raw_response}") from exc


if __name__ == "__main__":
    # Print instructions for the user to understand how to interact with the chatbot.
    print("Interactive Chat Mode! Type 'exit' or 'quit' to end the conversation.")
    print("Each message is sent separately to the AI (no conversation memory).\n")

    # Start an infinite loop to keep accepting user input until they exit.
    while True:
        # Prompt the user to enter a message.
        user_input = input("You: ").strip()

        # Check if the user wants to exit the conversation.
        if user_input.lower() in ["exit", "quit"]:
            # Break out of the while loop to end the program.
            print("Goodbye!")
            break

        # Handle the case where the user entered an empty message.
        if not user_input:
            # Prompt them to enter something.
            print("Please enter a message.\n")
            # Skip to the next iteration of the loop.
            continue

        # Try to send the user's message to OpenRouter and get a response.
        try:
            # Call the OpenRouter API with the user's prompt.
            # Note: Each call is independent; the AI has no memory of previous messages.
            assistant_response = call_openrouter(user_input)

            # Print the assistant's response so the user can see it.
            print(f"Assistant: {assistant_response}\n")

        # If there's an error (API key missing, network problem, etc.), handle it gracefully.
        except Exception as exc:
            # Print the error message so the user knows what went wrong.
            print(f"Error: {exc}\n")
