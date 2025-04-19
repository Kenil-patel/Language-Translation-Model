from googletrans import Translator
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

class TranslationModel:
    def __init__(self):
        # Initialize google translator
        self.translator = Translator()

        # Load Hugging Face model (M2M100) for perplexity calculation
        print("Loading multilingual model for Perplexity...")
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/m2m100_418M")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/m2m100_418M")
        self.model.eval()
        torch.set_grad_enabled(False)

        # BLEU smoothing function
        self.smoothie = SmoothingFunction().method4 

    def translate(self, text: str, src_lang: str = 'en', dest_lang: str = 'es') -> str:
        try:
            translated = self.translator.translate(text, src=src_lang, dest=dest_lang)
            print(f" Translation: {text} -> {translated.text}")
            return translated.text
        except Exception as e:
            print(f"Translation Error: {str(e)}")
            return f"Error: {str(e)}"

    def compute_bleu(self, reference: str, candidate: str) -> float:
        reference = [reference.lower().split()]
        candidate = candidate.lower().split()
        bleu_score = sentence_bleu(reference, candidate, smoothing_function=self.smoothie)
        print(f" BLEU Score: {bleu_score:.4f}")
        return bleu_score

    def compute_perplexity(self, text: str, lang: str = 'es') -> float:
        # M2M100 needs language token
        self.tokenizer.src_lang = lang
        encoded = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**encoded, labels=encoded["input_ids"])
        loss = outputs.loss
        perplexity = torch.exp(loss).item()
        print(f" Perplexity: {perplexity:.4f}")
        return perplexity

# --- Usage Example ---
if __name__ == "__main__":
    model = TranslationModel()

    while True:
        english = input("\nEnter English text (or 'quit' to exit): ")
        if english.lower() == 'quit':
            break

        reference = input("Enter reference Spanish translation (for BLEU): ")

        translated = model.translate(english, src_lang='en', dest_lang='es')
        bleu = model.compute_bleu(reference, translated)
        perplexity = model.compute_perplexity(translated, lang='es')
