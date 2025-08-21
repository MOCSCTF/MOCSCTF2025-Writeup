from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm

# 初始化模型和分词器
model = AutoModelForCausalLM.from_pretrained(
    "roneneldan/TinyStories-33M"
).eval()
tokenizer = AutoTokenizer.from_pretrained("roneneldan/TinyStories-33M")
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "left"

# 设置 batch 大小
BATCH_SIZE = 32

# 批量预测函数
def batch_predict(words):
    # 编码输入文本，自动 padding，返回 attention_mask
    inputs = tokenizer(
        words,
        return_tensors="pt",
        padding=True,
        truncation=True,
        return_attention_mask=True,
    )
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    # 生成文本
    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_new_tokens=30,
        num_beams=1,
        pad_token_id=tokenizer.eos_token_id,
    )

    # 提取新增的生成内容
    results = []
    for i in range(len(words)):
        generated = outputs[i, input_ids.shape[1]:]
        decoded = tokenizer.decode(generated, skip_special_tokens=True)
        results.append(decoded)
    return results

# 批量遍历词表并筛选包含 "success" 的输出
vocab_items = list(tokenizer.get_vocab().items())
for i in tqdm(range(0, len(vocab_items), BATCH_SIZE)):
    batch = vocab_items[i:i + BATCH_SIZE]
    words = [word for word, _ in batch]
    outputs = batch_predict(words)
    for word, output in zip(words, outputs):
        if 'success' in output.lower():
            print(word)

'''
  1%|          | 18/1571 [00:21<30:46,  1.19s/it]spe
  2%|▏         | 30/1571 [00:35<30:36,  1.19s/it]Ġtraders
  4%|▍         | 61/1571 [01:13<31:44,  1.26s/it]Ġcomplied
  4%|▍         | 65/1571 [01:18<31:00,  1.24s/it]ĠNeither
  5%|▍         | 71/1571 [01:25<31:15,  1.25s/it]Ġdeceived
  6%|▌         | 98/1571 [01:59<31:24,  1.28s/it]Ġextending
'''