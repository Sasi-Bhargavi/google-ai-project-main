import torch
from transformers import pipeline

# Global variable to hold our pipeline in-memory so it only loads once (Lazy Loading)
_lamini_pipeline = None

def get_lamini_pipeline():
    """Initializes and caches the local LaMini-Flan-T5 text-to-text pipeline."""
    global _lamini_pipeline
    if _lamini_pipeline is None:
        # Check for GPU hardware acceleration availability, fallback to CPU
        device = 0 if torch.cuda.is_available() else -1
        
        # Loading 'MBZUAI/LaMini-Flan-T5-248M' - highly optimized for consumer hardware
        _lamini_pipeline = pipeline(
            "text2text-generation", 
            model="MBZUAI/LaMini-Flan-T5-248M", 
            device=device
        )
    return _lamini_pipeline

def query_lamini(prompt: str, max_length: int = 256) -> str:
    """Executes safe, localized text inference using LaMini on your hardware."""
    try:
        pipe = get_lamini_pipeline()
        result = pipe(prompt, max_length=max_length, num_return_sequences=1)
        return result[0]['generated_text']
    except Exception as e:
        return f"Local Model Inference Error: {str(e)}"