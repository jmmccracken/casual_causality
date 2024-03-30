"""casual_causality.py

Quick wrapper and prompt injector for using LLMs
to "answer" questions about causality.
"""
# libraries
import yaml as ylib
import click
import pathlib as pl
from loguru import logger
import sys
from fastapi import FastAPI, HTTPException
from openai import OpenAI, OpenAIError

# globals
description = """
CASUAL CAUSALITY!! ❓🚀😶‍🌫️

Let's let the AI explain causality to us.
"""
app = FastAPI(
    title="casual_causality",
    description=description,
    summary="The experiments have already been done. Just tell me the results."
)
requested_effects = {}
DEFAULT_CONFIG_YAML = "causal_config.yml"

# LLM interface class
class CauseFinderLOL:
    def __init__(self):
        # Read config
        llm_config = load_config(DEFAULT_CONFIG_YAML)
        self.configured = True
        if not llm_config:
            logger.error(f"Failed to load LLM configuration.")
            self.configured = False
            self.connected = False
        if self.configured:
            # Setting the API key to use the OpenAI API
            self.client = OpenAI(
                base_url = llm_config['base_url'],
                api_key = llm_config['api_key']
            )
            self.model = llm_config['model']
            logger.info(f"Connected to {self.model} at {llm_config['base_url']}.")
        self.user_spec = "You are a physics professor who studies causality. "
        self.user_spec += "You provide references and sources for everything you say. "
        self.user_spec += "Your favorite references are textbooks and articles from academic journals."
        self.user_spec += "You never say anything without providing justification of your statement's truth."
        self._requested_effect = None
        self.messages = [{
            "role": "system",
            "content": self.user_spec
        }]

    def _chat(self, message):
        self.messages.append({"role": "user", "content": message})
        response = self.client.chat.completions.create(
            model = self.model,
            messages = self.messages
        )
        self.messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })
        return response.choices[0].message.content

    def provide_causes(self, effect_string):
        self._requested_effect = effect_string
        try:
            m_response = self._chat(f"What causes {self._requested_effect}?")
            self.connected = True
        except OpenAIError as e:
            logger.error(f"Failed to connect to LLM: {e}")
            self.connected = False
            m_response = None
        return m_response

    def elaborate(self):
        if not self.connected:
            return None
        tell_me_more = "How? Elaborate on your response. "
        tell_me_more += f"Why exactly does this cause {self._requested_effect}?"
        return self._chat(tell_me_more)

    def explain_better(self):
        if not self.connected:
            return None
        what_now = "I am confused. Explain your answer as if I was a 5th grade science student."
        return self._chat(what_now)

    def wtf(self):
        if not self.connected:
            return None
        you_seem_confused = "This answer seems wrong to me. "
        you_seem_confused += "Provide more examples and/or references to convince me you are correct."
        return self._chat(you_seem_confused)
    
    def sat_form(self):
        if not self.connected:
            return None
        try_again = f"If the effect is {self._requested_effect}, then the cause is what?"
        return self._chat(try_again)

# defs
def load_config(yaml):
    """Get the LLM connection info from the YAML."""
    m_path = pl.Path(yaml)
    if not m_path.exists():
        logger.error(f"Cannot load {yaml}. Did you misspell the filename?")
        return None
    try:
        config = ylib.safe_load(m_path.open('r'))
    except ylib.YAMLError as exc:
        logger.error(f"Error in configuration file: {exc}")
        return None
    req_fields = [
        'model', 'api_key', 'base_url'
    ]
    for rf in req_fields:
        if rf not in list(config.keys()):
            logger.error(f"Configuration file is missing field {rf}. Cannot connect to LLM.")
            return None
        else:
            logger.info(f"Using {rf}: {config[rf]}")
    return config

@click.command()
@click.option(
    '-y',
    '--yaml',
    default=DEFAULT_CONFIG_YAML,
    help="YAML configuration file for LLM connections")
def main(yaml):
    """Casual Causality.

    Quick wrapper and prompt injector service for using LLMs
    to "answer" questions about causality. This script is 
    intended to be run with a server, e.g.

    uvicorn casual_causality:app --reload

    """
    logger.info(f"Starting CASUAL CAUSALITY!! ❓🚀😶‍🌫️")
    logger.info(f"Using {yaml} for configuration.")
    llm_config = load_config(yaml)
    if not llm_config:
        logger.error(f"Failed to load LLM configuration. Exiting.")
        sys.exit(1)
    logger.info("Service must be started using a server. Try --help.")

# routes
@app.get("/")
def read_root():
    available_effects = list(requested_effects.keys())
    return {"available effects": available_effects}

@app.get("/causes/{effect_string}")
def r_provide_causes(effect_string: str):
    requested_effects[effect_string] = CauseFinderLOL()
    m_response = requested_effects[effect_string].provide_causes(effect_string)
    if not requested_effects[effect_string].connected:
        raise HTTPException(status_code=404, detail="Problem connecting to LLM. Check log for errors.")
    return m_response

@app.get("/causes/{effect_string}/elaborate")
def r_elaborate(effect_string: str):
    if effect_string not in requested_effects:
        raise HTTPException(status_code=404, detail="You must request causes _before_ you request more info.")
    m_response = requested_effects[effect_string].elaborate()
    return m_response

@app.get("/causes/{effect_string}/explain_better")
def r_explain_better(effect_string: str):
    if effect_string not in requested_effects:
        raise HTTPException(status_code=404, detail="You must request causes _before_ you request more info.")
    m_response = requested_effects[effect_string].explain_better()
    return m_response

@app.get("/causes/{effect_string}/wtf")
def r_wtf(effect_string: str):
    if effect_string not in requested_effects:
        raise HTTPException(status_code=404, detail="You must request causes _before_ you request more info.")
    m_response = requested_effects[effect_string].wtf()
    return m_response

@app.get("/causes/{effect_string}/full_history")
def r_full_history(effect_string: str):
    if effect_string not in requested_effects:
        m_response = []
    else:
        m_response = requested_effects[effect_string].messages
    return m_response

if __name__ == '__main__':
    main()

