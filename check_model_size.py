"""
Script to check the memory usage of the loaded toxicity classification model.
"""

import os
import psutil
import torch

from app.services import get_toxicity_pipeline


def format_bytes(bytes_value: int) -> str:
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} TB"


def main():
    """Load the model and display memory usage statistics."""
    
    process = psutil.Process(os.getpid())
    
    # Get baseline memory before loading
    baseline_memory = process.memory_info().rss
    print(f"Baseline RAM usage: {format_bytes(baseline_memory)}")
    print()
    
    print("Loading model...")
    get_toxicity_pipeline()  # Forces cache to load it
    print("Model loaded!")
    print()
    
    # Get memory after loading
    final_memory = process.memory_info().rss
    model_memory = final_memory - baseline_memory
    
    print("=" * 50)
    print("Memory Statistics:")
    print("=" * 50)
    print(f"Baseline RAM:     {format_bytes(baseline_memory)}")
    print(f"Final RAM:        {format_bytes(final_memory)}")
    print(f"Model RAM:        {format_bytes(model_memory)}")
    print()
    
    # Additional system info
    print("System Information:")
    print("=" * 50)
    total_memory = psutil.virtual_memory().total
    available_memory = psutil.virtual_memory().available
    print(f"Total RAM:         {format_bytes(total_memory)}")
    print(f"Available RAM:     {format_bytes(available_memory)}")
    print(f"RAM Used:          {format_bytes(total_memory - available_memory)}")
    print()
    
    # PyTorch GPU info if available
    if torch.cuda.is_available():
        print("GPU Information:")
        print("=" * 50)
        for i in range(torch.cuda.device_count()):
            gpu_memory = torch.cuda.get_device_properties(i).total_memory
            print(f"GPU {i}:            {format_bytes(gpu_memory)}")
    else:
        print("GPU: Not available (using CPU)")


if __name__ == "__main__":
    main()

