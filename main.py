from tetras import Tetra
import functions
from openai import OpenAI


def main():
    client = OpenAI().beta
    tetra = Tetra(
        client=client,
        tools=[
            {"type": "code_interpreter"},
            {
                "type": "function",
                "function": functions.d_get_current_weather,
            },
        ],
    )
    response = tetra.process_message("What is the weather in Shanghai today?")
    print(response)
    return


if __name__ == "__main__":
    main()
