import torch
from transformers import pipeline

# Global pipeline instance holder for in-memory caching
_lamini_pipeline = None

def get_lamini_pipeline():
    """
    Launches and caches the localized LaMini-Flan-T5 text-to-text pipeline 
    on local compute hardware.
    """
    global _lamini_pipeline
    if _lamini_pipeline is None:
        # Auto-detect CUDA GPU acceleration, else default to CPU execution threads
        device = 0 if torch.cuda.is_available() else -1
        
        # Pulls 'MBZUAI/LaMini-Flan-T5-248M' straight from Hugging Face Hub
        _lamini_pipeline = pipeline(
            "text2text-generation", 
            model="MBZUAI/LaMini-Flan-T5-248M", 
            device=device
        )
    return _lamini_pipeline

def query_lamini(prompt: str, max_length: int = 256) -> str:
    """
    Runs rapid local inference logic using your hardware, completely bypassing 
    external cloud API runtime fees.
    """
    try:
        pipe = get_lamini_pipeline()
        result = pipe(prompt, max_length=max_length, num_return_sequences=1)
        return result[0]['generated_text']
    except Exception as e:
        return f"Localized LaMini Pipeline Engine Internal Error: {str(e)}"