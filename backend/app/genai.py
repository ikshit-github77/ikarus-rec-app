from transformers import pipeline
from functools import lru_cache

@lru_cache(maxsize=1)
def _generator():
    # use your existing model; FLAN-T5 small is great if you installed it
    return pipeline("text2text-generation", model="google/flan-t5-small", max_new_tokens=80)

def generate_copy(title, brand="", material="", color="", categories="", user_prompt=""):
    prompt = (
        "Write a short, punchy, helpful product blurb (35–55 words). "
        "Lead with the benefit, then mention brand, material and color naturally. "
        "Avoid marketing fluff, keep it clear and specific.\n\n"
        f"Title: {title}\nBrand: {brand}\nMaterial: {material}\nColor: {color}\nCategories: {categories}\n"
        + (f"User context: {user_prompt}\n" if user_prompt else "")
        + "Blurb:"
    )
    out = _generator()(prompt, do_sample=False)[0]["generated_text"]
    return out.strip()
