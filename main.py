import requests
import json


def main():
    # Initial quote and relevant songs in the base
    user_input = "Oh, won't you kiss me on the mouth and love me like a sailor? And when you get a taste, can you tell me, what's my flavor?"
    relevant_document = "Sailor Song by Gigi Perez" # TODO - find it from vector base
    
    # Preparing a prompt
    prompt = """
    You are a bot that identifies title and artist of a song based on a quote. You answer in very short sentences and do not include extra information.
    This is the recommended song: {relevant_document}
    The quote is: {user_input}
    Find a song that matches a quote based on the recommended song and the quote.
    """
    
    # Connection with the LLM model
    url = 'http://localhost:11434/api/generate'
    data = {
        "model": "llama3",
        "prompt": prompt.format(user_input=user_input, relevant_document=relevant_document)
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)

    # Getting the full response
    full_response = []
    try:
        for line in response.iter_lines():
            if line:
                decoded_line = json.loads(line.decode('utf-8'))
                full_response.append(decoded_line['response'])
    finally:
        response.close()
    print(''.join(full_response))


if __name__ == "__main__":
    main()