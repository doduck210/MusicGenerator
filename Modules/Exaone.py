import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def translator(text):
    model_name = "LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct"

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Choose your prompt
    prompt = text

    messages = [
        {"role": "system", "content": "You are an translator who translate the input to English."},
        {"role": "user", "content": prompt}
    ]
    input_ids = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt"
    )

    output = model.generate(
        input_ids.to("cuda"),
        eos_token_id=tokenizer.eos_token_id,
        max_new_tokens=128,
        do_sample=False,
    )
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response.split("[|assistant|]")[-1].split("[|endofturn|]")[0].strip()

if __name__ == "__main__":
    text = "섹소폰이 주 멜로디를 연주하는 120bpm의 melancholy한 비밥"
    print(translator(text))
