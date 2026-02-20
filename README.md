# :robot: What can this bot do? 
I made this bot for **personal use** to manage my Telegram groups. Actually, I felt like I needed someone to delete off-topic chats that people do in the public group. So the main idea came up from here! :nerd_face: 

<br>
<br>

## :hammer_and_wrench: This bot can :
- :broom: Delete a section of chats
- :memo: Take notes from people's messages 
- :pushpin: Pin a text
- 😈 And have a little naughty conversation!


These features make the bot perfectly useful and simple for daily usage and groups with few members! 
<br>
<br>

# :warning: Warning
This bot has a bit of an attitude!
It might sound rude or sarcastic, but trust me — it's just joking!😆<br>
Don't take it too seriously! It's meant to keep things fun!

<br>
<br>

# :speech_balloon: How does it work?
You can simply **call its name** if you want to have a conversation with it!
There is also a start command which is just for showing that how much the bot is ready to serve!
You can simply start the bot by sending `/start` in the group. It doesn't need these type of commands though. The bot doesn’t rely heavily on commands — you can interact with it naturally, like a real group member.

<br>

## 🧠 AI-powered replies (New Feature)
It's powered by AI using **OpenRouter** and It generates human-like replies instead of relying on static responses.


<br> 

### 🔄 Fallback logic
Free AI models often return errors such as rate limits or client errors.
To handle this, the bot uses **multiple AI models**.  
If one model fails for *any reason*, the bot automatically switches to the next available model.

Models are tried in priority order until one succeeds.

This is the block which handles this logic:
```python
    # List of AI models
    AI_MODELS = [
        "openrouter/free",
        "meta-llama/llama-3-8b-instruct",
    ]

    def send_request(model: str) -> str | None:
        logger.info(f"Trying model: {model}")

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 220
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=60
            )
        except Exception as e:
            logger.error(f"Request error for model {model}: {e}")
            return None

        status = response.status_code

        try:
            data = response.json()
        except Exception:
            logger.error(f"Model {model} returned non-JSON | HTTP {status}")
            return None

        if (
            isinstance(data, dict)
            and data.get("choices")
            and data["choices"][0].get("message", {}).get("content")
        ):
            if status >= 400:
                logger.warning(
                    f"Model {model} returned content with HTTP {status}"
                )
            else:
                logger.info(f"Model {model} succeeded with HTTP {status}")

            return data["choices"][0]["message"]["content"]

        logger.error(
            f"Model {model} failed | HTTP {status} | Body: {data}"
        )
        return None

    # Switching the model in case
    for model in AI_MODELS:
        result = send_request(model)
        if result:
            return result

    # Fallback
    logger.critical("ALL MODELS FAILED")
    return "قهرم بای"

```

<br>
<br>

This is just a **prototype** of a Telegram group-managing bot. I'm pretty sure I can add more incredible features such as:

- 🔇 Mute members for a few seconds or minutes  
- ⛔ Temporarily or permanently ban members  
- 🧩 Automatically decide on moderation actions based on chat behavior  

These features will make group management even easier, letting Somayeh act more like a real moderator!