# Casual Causality (casual_causality)

This repository contains a simple API wrapper for exploring the use of LLMs in explaining causes of effects. The API has no frontend and all of the exploration explained below was done directly with the API calls (e.g., in a Jupyter notebook).

## Wait, is this a serious research tool or a toy?

Yes. If you're a causality researcher, then `casual_causality` should be probably be considered a toy. If you're an LLM researcher, then the prompts (and maybe the discussion below) might generate ideas for more subtle tests of these AI systems.

## Installation

You need the following libraries:
```bash
pip install fastapi
pip install "uvicorn[standard]"
pip install loguru
pip install openai
```

## Running the API

One way to start the API is
```bash
uvicorn casual_causality:app --reload
```
The [FastAPI](https://fastapi.tiangolo.com/) documentation provides more details and other options.

## Connecting to an LLM

The `causal_config.yml` file supplies all the information the app needs to connect to your LLM. It contains three key-value pairs:
* *model* names the model being used
* *base_url* is the OpenAI-compliant endpoint (see the official [OpenAI documentation](https://github.com/openai/openai-python) for more details)
* *api_key* provides the API key

The config file provided on the `master` branch of this repo, i.e.,
```yaml
model: LLaMA_CPP
base_url: http://localhost:8080/v1
api_key: sk-no-key-required
```
shows the configuration needed to connect to a local LLM provided by a [llamafile](https://github.com/Mozilla-Ocho/llamafile?tab=readme-ov-file). 

## Available routes

`casual_causality` provides four "working" endpoints and two "service" endpoints. The service endpoints are
* root ("/") which lists all the effects that have been requested in the current session
* conversation history ("/causes/{effect_string}/full_history") which provides the full LLM conversation for a specific requested `effect_string`

The working endpoints (i.e., the endpoints related to finding causes) can be grouped into two categories. The first is just asking for an initial guess at the cause of a requested effect; i.e.,
* cause ("/causes/{effect_string}")

The other three routes can be grouped into a help-me-understand-what-you-mean category; i.e.,
* elaborate ("/causes/{effect_string}/elaborate")
* explain better ("/causes/{effect_string}/explain_better")
* try harder ("/causes/{effect_string}/wtf")

These routes can sometimes help explain why an LLM is providing a seemingly confusing answer to your requested effect. The routes technically just represent various prompt rewording and extensions of the original provide-cause-for-requested-effect prompt, so they may provide exactly zero help in understanding some LLM's confusing response. It's all very dependent on the LLM you're using.

All the routes are `GET` methods that can be explored using an API testing tool like [Postman](https://www.postman.com/), standard Python libraries like [requests](https://requests.readthedocs.io/en/latest/), or even directly in a web browser. `casual_causality` is built with FastAPI which [automatically generates API documentation](https://fastapi.tiangolo.com/features/#automatic-docs) at the "docs" endpoint. If, e.g., you started the API with the default settings, then the SwaggerUI is available at

* http://localhost:8000/docs

You can use the SwaggerUI's "Try It Out" feature to explore the API without any additional tools.

## Walkthrough example: What causes rain?

As an example, let's use the [TinyLlama](https://github.com/jzhang38/TinyLlama) LLM. Grab the TinyLlama llamafile (e.g., from [HuggingFace](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0) or the [llamafile examples table](https://github.com/Mozilla-Ocho/llamafile?tab=readme-ov-file)) and start the LLM following the instructions on the box; e.g.,
```bash
./TinyLlama-1.1B-Chat-v1.0.Q5_K_M.llamafile --nobrowser
```
Start `casual_causality` with the default settings (as shown above), which will provide the endpoints at http://localhost:8000. Now we can ask TinyLlama what causes rain with

* http://localhost:8000/causes/rain

The response is
> "Rain is caused by the interaction between the Earth's atmosphere and the sun. The sun heats up the Earth's surface, causing water vapor to rise into the atmosphere. As the water vapor cools and condenses into droplets, they fall as rain. The process of rain formation is a complex one that involves several factors, including temperature, humidity, wind, and atmospheric pressure. However, the basic mechanism behind rain formation is the same for all types of precipitation: water vapor in the atmosphere condenses into droplets when it comes into contact with warm, moist air."

This response is not specific but, thankfully, not obviously wrong. Perhaps your curiosity is satisfied and you're willing to stop here. Just for fun, let's explore the "tell me more" routes:
1. Elaborate -- http://localhost:8000/causes/rain/elaborate. The response is
> "The interaction between the Earth's atmosphere and the sun causes water vapor in the atmosphere to rise into the troposphere, where it is condensed into droplets by the cooling effect of the sun. This process is called \"precipitation,\" and it is what causes rain. The warm air that rises from the ground and meets with the cooler air above creates a gradient in temperature, which leads to the formation of water vapor. As the water vapor rises into the troposphere, it cools and condenses into droplets, forming clouds and precipitation. This process is called \"rain formation,\" and it is what causes rain to fall from the sky."

2. Explain better -- http://localhost:8000/causes/rain/explain_better. The response is
> "Sure, I'd be happy to explain! Rain is caused by the interaction between the Earth's atmosphere and the sun. The sun heats up the Earth's surface, causing water vapor to rise into the atmosphere. As the water vapor cools and condenses into droplets, they fall as rain. This process is called \"precipitation,\" and it is what causes rain to fall from the sky. The warm air that rises from the ground and meets with the cooler air above creates a gradient in temperature, which leads to the formation of water vapor. As the water vapor rise into the troposphere, it cools and condenses into droplets, forming clouds and precipitation. This process is called \"rain formation,\" and it is what causes rain to fall from the sky. I hope that helps! Let me know if you have any further questions."

3. Try harder -- http://localhost:8000/causes/rain/wtf. The response is
> "Sure, I'd be happy to provide more examples and references to help you understand the process of rain formation better. Here are a few:\n1. In the tropics, where the temperature is warmest, water vapor can rise into the atmosphere due to the presence of moist air. This moist air is called \"tropical convection,\" which is responsible for producing clouds and precipitation in the tropics. 2. When a drop of water vapor falls from the sky, it cools as it descends through the troposphere (the lowest layer of the atmosphere). As it cools, it condenses into droplets, forming clouds. These clouds can be seen on satellite imagery or in the form of precipitation on the ground. 3. The process of rain formation is not limited to just water vapor rising from the Earth's surface and falling back down. In fact, some types of precipitation, such as snow, are formed by a different process called \"precipitation.\" Snow falls when cold air meets warm air, creating a layer of ice that falls to the ground. This process is called \"freezing rain\" or \"snow showers,\" and it can be seen on satellite imagery or in the form of precipitation on the ground. 4. Finally, some types of precipitation, such as hail or thunderstorms, are formed by a different process called \"precipitation.\" These events involve the formation of droplets from water vapor that fall to the ground as rain, snow, sleet, or hail. I hope this helps you understand the process of rain formation better! Let me know if you have any further questions."


Interestingly, the additional responses seem to get a little more confusing (what exactly is the "cooling effect of the sun"?). But, for the most part, these responses are all reasonable and firmly within the realm of "not completely wrong".

## What's the point?

Causality is hard ([citation needed](https://en.wikipedia.org/wiki/Wikipedia:Citation_needed)). The promise of reliable causal information, even just semi-reliable causal information, is potentially invaluable for many researchers. In theory, modern LLMs have been trained on massive amounts of verifiable causal information from, e.g., online academic research and teaching materials. A quick-and-simple tool to grab this data, a kind of "causal lookup table" would be helpful. That's where this idea started. Unfortunately, I'm not sure LLMs are quite ready for this task yet.

## Hold on a minute. We just saw a perfectly fine answer to the question "What causes rain?" Why are you so down on LLMs all of a sudden?

Causality research can be subtle. It is beholden to ontology both [in theory](https://en.wikipedia.org/wiki/Ontology_(information_science)) and [in practice](https://en.wikipedia.org/wiki/Applied_ontology). Researchers often deal with this issue using [operational definitions of causality](https://en.wikipedia.org/wiki/Causal_analysis). Current LLM technology may not be helpful in research fields struggling with such issues. To be fair, I am not an LLM researcher, I am just speaking from experience. I will come back and update this code (perhaps even provide a frontend!) if/when I feel the situation improves.

As an example, let's consider a common human experience, the sunrise. Let's ask TinyLlama what causes sunrises.
* http://localhost:8000/causes/sunrise. Here's the response
> "The sun rises due to the Earth's rotation around its axis, which causes the Earth's gravity to pull on the Sun's surface, causing it to rotate and cause the Sun to rise. The process is called \"gravitational lensing\" because the Earth's mass bends the light from the Sun, creating a distorted image of the Sun in front of it."

Now this response is more than a little confused. Even someone unfamiliar with [gravitational lensing](https://en.wikipedia.org/wiki/Gravitational_lens) will probably recognize from this response that the LLM seems confused. Let's go ahead and ask for clarification with the other routes. Here's all the responses
* (elaborate)
> "The process of sunrise is caused by the Earth's rotation around its axis, which causes the Earth's gravity to pull on the Sun's surface. The Sun's position in relation to the Earth's equator at any given time is determined by the Earth's rotational motion. As the Earth rotates, it moves closer to the Sun and the Sun's position relative to the Earth's equator changes. This causes the Sun to rise earlier in the morning as it gets closer to the horizon. The process of sunrise is a result of the Earth's rotation around its axis, which creates a gravitational force that pulls on the Sun's surface and causes it to rise earlier in the morning."

* (explain_better)
> "Sure, I'd be happy to explain! The process of sunrises is caused by the Earth's rotation around its axis. As the Earth rotates, it moves closer to the Sun and the Sun's position relative to the Earth's equator changes. This causes the Sun to rise earlier in the morning as it gets closer to the horizon. The process of sunrises is a result of the Earth's rotation around its axis, which creates a gravitational force that pulls on the Sun's surface and causes it to rise earlier in the morning. In other words, the Earth's rotation causes the Sun to rise earlier in the morning due to the Earth's gravity pulling on the Sun's surface."

* (wtf)
> "Sure, I'd be happy to provide more examples and references to help you understand the process of sunrises better. Here are a few more examples:\n- During the summer months, when the Earth is closer to the Sun than it is during the winter months, the Sun rises earlier in the morning. This is because the Earth's rotation around its axis causes the Sun to rise earlier in the morning due to the Earth's gravity pulling on the Sun's surface. - During the summer months, when the Earth is closer to the Sun than it is during the winter months, the Sun sets later in the evening. This is because the Earth's rotation around its axis causes the Sun to set earlier in the evening due to the Earth's gravity pulling on the Sun's surface. - During the summer months, when the Earth is closer to the Sun than it is during the winter months, the Sun rises later in the evening. This is because the Earth's rotation around its axis causes the Sun to rise earlier in the evening due to the Earth's gravity pulling on the Sun's surface. - During the summer months, when the Earth is closer to the Sun than it is during the winter months, the Sun sets later in the evening. This is because the Earth's rotation around its axis causes the Sun to set earlier in the evening due to the Earth's gravity pulling on the Sun's surface. - During the summer months, when the Earth is closer to the Sun than it is during the winter months, the Sun rises later in the morning and sets later in the evening. This is because the Earth's rotation around its axis causes the Sun to rise earlier in the morning due to the Earth's gravity pulling on the Sun's surface, while the Earth's rotation around its axis causes the Sun to set earlier in the evening due to the Earth's gravity pulling on the Sun's surface. - During the summer months, when the Earth is closer to the Sun than it is during the winter months, the Sun rises later in the morning and sets earlier in the evening. This is because the Earth's rotation around its axis causes the Sun to rise earlier in the morning due to the Earth's gravity pulling on the Sun's surface, while the Earth's rotation around its axis causes the Sun to set earlier in the evening due to the Earth's gravity pulling on the Sun's surface. - During the summer months, when the Earth is closer to the Sun than it is during the winter months, the Sun rises later in the morning and sets earlier in the evening. This is because the Earth's rotation around its axis causes the Sun to rise later in the morning due to the Earth's gravity pulling on the Sun's surface, while the Earth's rotation around its axis causes the Sun to set later in the evening due to the Earth's gravity pulling on the Sun's surface. I hope this helps! Let me know if you have any further questions or need more examples."

It takes detailed prior knowledge to figure out exactly how and why these responses are wrong. The LLM presents seemingly **plausible** causes. Parts of the response might be considered correct under (very liberal) interpretation of the language it uses, but a statement such as "Earth's gravity pulls on the Sun and causes it to rise" is easy to misinterpret for someone who doesn't _already know what causes sunrises_. If the required prior knowledge for a tool to be useful is exactly the knowledge you expect the tool to provide, then the tool is not practical.

## Trust in your LLM

Perhaps you think using TinyLlama as an example is disingenuous. Let's try the sunrise explain again with [LLaVA](https://llava-vl.github.io/). The response is
> "Sunrise is caused by the Earth's rotation on its axis. The Earth rotates once every 24 hours, and as it does so, different parts of the planet face the sun at different times. This causes the appearance of sunrise, which occurs when the sun is below the horizon in the morning."

This response is much better than what we saw with TinyLlama. What about somethng a little more subtle, like acceleration (see [Frisch's discussion](https://philpapers.org/rec/FRICRI-2) on why this topic might be considered "subtle")? Here's the LLaVA response for the cause of acceleration
> "Acceleration is caused by a net force acting on an object. The magnitude of the acceleration is directly proportional to the net force and inversely proportional to the mass of the object. The direction of the acceleration is also determined by the direction of the net force."

This text is more or less a restatement of [Newton's 2nd law](https://en.wikipedia.org/wiki/Newton%27s_laws_of_motion). Do Newton's laws say anything about causality? That's up for debate. An equals sign is symmetric; causality is not. 

Of course, such concerns may be too philosophical for a conversation about the practicality of LLMs in causality research. What about something a little less theoretical-physics-y? Here's the LLaVA response for the cause of fire
> "Fire is caused by a combination of heat, fuel, and an oxidizing agent. Heat is the initial source of energy that ignites the fuel, while the oxidizing agent (usually oxygen) provides the necessary conditions for the fire to continue to grow and spread. In general, fires require three elements to occur: heat, fuel, and an oxidizing agent."

Like with saw with TinyLlama and rain, this response is not wrong but it could be more correct. "Heat" here means enough energy to increase the "temperature above the flash point for the fuel/oxidizer mix and sustain a rate of rapid oxidation that produces a chain reaction." (This quote, by the way, is taken from [Wikipedia's explanation of fire](https://en.wikipedia.org/wiki/Fire)--something LLaVA presumably trained on but did not provide as part of our causal explanation). There's also the more formal points of confusing "fire" with "combustion". When we ask for a cause of fire, why would the LLM not provide something like [FEMA's statistical analysis of fire causes](https://www.usfa.fema.gov/statistics/reports/fire-causes/)?

A natural point to be made in defense of the LLM is that "more complete" responses can probably be obtained with better and/or different prompts. Perhaps I could get LLaVA to return those statistical tables if I directly ask for them. But how would I know to ask for them without prior knowledge of what I expect the response to be? The subtle confusion that might arise from the LLM's use of language is never discussed within the LLM responses themselves, whereas such discussions are commonplace in the causality literature (Halpern's book [Actual Causality](https://mitpress.mit.edu/9780262537131/actual-causality/) is a good place to start if you're interested in this topic). 

The LLM provides responses without qualification or statements of uncertainty. A researcher using this tool, therefore, must trust both the LLM and their own interpretation of the LLM's use of language. **There is absolutely nothing wrong with that.** Such tools can be helpful in a variety of ways. The only point being made here is that in causality research such trust needs to be carefully accounted and, if possible, quantified. 

As stated before, it does not seem like modern LLM's are quite ready to provide discussions of their own use of ontology, trust, and uncertainty.

