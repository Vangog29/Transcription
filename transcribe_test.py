import torch
from transformers import pipeline
import time
import os

def main():
    model_id = "artyomboyko/whisper-small-ru-v2"

    # Проверка доступности GPU (CUDA)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    
    print(f"--- Инициализация на устройстве: {device} ---")
    
    # Загрузка пайплайна
    # При первом запуске он скачает около 1ГБ весов модели
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model_id,
        torch_dtype=torch_dtype,
        device=device,
    )

    # Путь к аудиофайлу (измените на свой или положите файл рядом)
    audio_file = "test.wav" 
    
    if not os.path.exists(audio_file):
        print(f"Ошибка: Файл '{audio_file}' не найден. Пожалуйста, положите аудиофайл в папку со скриптом.")
        return

    print(f"Начинаю транскрибацию файла: {audio_file}...")
    
    start_time = time.time()
    
    # Запуск распознавания
    result = pipe(
        audio_file, 
        chunk_length_s=30, 
        batch_size=8, 
        generate_kwargs={"language": "russian"}
    )
    
    end_time = time.time()
    
    print("\n--- Результат ---")
    print(result["text"])
    print(f"\nВремя выполнения: {end_time - start_time:.2f} сек.")

if __name__ == "__main__":
    main()
