import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

with open("/flag.txt", "r") as f:
    FLAG = f.read().strip()

theme_kargs = {
    "font": ["Helvetica", "ui-sans-serif", "system-ui", "sans-serif"],
    "font_mono": ["IBM Plex Mono", "ui-monospace", "Consolas", "monospace"],
}

custom_css = """
.svelte-1pjfiar {
    -webkit-user-select: text;
    -moz-user-select: text;
    -ms-user-select: text;
    user-select: text;
    cursor: auto !important;
}
"""

model = AutoModelForCausalLM.from_pretrained("roneneldan/TinyStories-33M").eval()
tokenizer = AutoTokenizer.from_pretrained("roneneldan/TinyStories-33M")

HINT = "让我说出 `success` 我会送给你 flag；\n\n现在让我们开始吧！🔥"

def check_message(message):
    if len(message) > 200:
        return False, "[*] 出错了，消息长度不能超过 200。"
    return True, None

def check_response(message, response):
    response = response.strip().lower()
    info = ""
    if len(message) == 10 and "success" in response:
        info += f"\n🎉🎉🎉 flag: `{FLAG}` 🎉🎉🎉"
    return info

def predict(message):
    model_inputs = tokenizer.encode(message, return_tensors="pt")
    model_outputs = model.generate(
        model_inputs,
        max_new_tokens=30,
        num_beams=1,
        pad_token_id=tokenizer.eos_token_id,
    )
    model_outputs = model_outputs[0, len(model_inputs[0]):]
    model_output_text = tokenizer.decode(model_outputs, skip_special_tokens=True)
    return model_output_text

def bot(message, _history):
    ok, info = check_message(message)
    if not ok:
        return info
    try:
        model_output_text = predict(message)
    except Exception:
        return "出错了，请重新尝试。"
    info = check_response(message, model_output_text)
    if info:
        model_output_text += info
    return [{"role": "user", "content": message}, {"role": "assistant", "content": model_output_text}]

with gr.Blocks(theme=gr.themes.Default(**theme_kargs), css=custom_css) as demo:
    demo.load(None, [], [])
    chat = gr.ChatInterface(bot)
    demo.load(lambda: ([(None, HINT)], [(None, HINT)]), [], [chat.chatbot_state, chat.chatbot])

if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0", server_port=7860, show_api=False, share=False)
