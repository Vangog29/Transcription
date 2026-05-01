import os
import threading
import sys
import json
import subprocess
import tempfile
import customtkinter as ctk
from tkinter import filedialog, messagebox
from groq import Groq

try:
    from google import genai
    LEGACY_SDK = False
except ImportError:
    try:
        import google.generativeai as genai
        LEGACY_SDK = True
    except ImportError:
        genai = None

# Настройка пути для локального FFmpeg
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in os.environ["PATH"]:
    os.environ["PATH"] = project_root + os.pathsep + os.environ["PATH"]

# Настройка темы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class UnifiedTranscriptionApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sales Intelligence Pro (Groq + Gemma 4)")
        self.geometry("1000x850")

        self.config_path = "config.json"
        self.groq_key_path = "api_kay_groc.md"
        self.google_key_path = "api_kay_google.md"
        self.prompt_path = "analytics_prompt.md"
        
        self.load_config()

        self.groq_client = None
        self.google_client = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.label_title = ctk.CTkLabel(self, text="Sales Transcription & Analytics PRO", font=ctk.CTkFont(size=26, weight="bold"))
        self.label_title.grid(row=0, column=0, padx=20, pady=20)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.tabview.add("1. Транскрибация")
        self.tabview.add("2. Аналитика LLM")
        self.tabview.add("Настройки")
        self.tabview.add("Логи")

        self.setup_transcription_tab()
        self.setup_analysis_tab()
        self.setup_settings_tab()
        self.setup_logs_tab()

        self.label_status = ctk.CTkLabel(self, text="Статус: Готов", font=ctk.CTkFont(size=12))
        self.label_status.grid(row=2, column=0, padx=20, pady=5)

        self.init_api()
        self.load_initial_prompt()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    self.groq_key_path = config.get("groq_key_path", self.groq_key_path)
                    self.google_key_path = config.get("google_key_path", self.google_key_path)
                    self.prompt_path = config.get("prompt_path", self.prompt_path)
            except: pass

    def save_config(self):
        config = {"groq_key_path": self.groq_key_path, "google_key_path": self.google_key_path, "prompt_path": self.prompt_path}
        with open(self.config_path, "w") as f: json.dump(config, f)

    def init_api(self):
        if os.path.exists(self.groq_key_path):
            try:
                with open(self.groq_key_path, "r") as f:
                    self.groq_client = Groq(api_key=f.read().strip())
                    self.log("Groq API загружен.")
            except Exception as e: self.log(f"Ошибка Groq: {e}")
        
        if os.path.exists(self.google_key_path):
            try:
                with open(self.google_key_path, "r") as f:
                    api_key = f.read().strip()
                    if not LEGACY_SDK:
                        self.google_client = genai.Client(api_key=api_key)
                        self.log("Gemma 4 готова.")
                    else:
                        genai.configure(api_key=api_key)
                        self.google_client = genai.GenerativeModel('gemma-4-31b-it')
                        self.log("Gemma 4 (Legacy) готова.")
            except Exception as e: self.log(f"Ошибка Google: {e}")

    def load_initial_prompt(self):
        if os.path.exists(self.prompt_path):
            try:
                with open(self.prompt_path, "r", encoding="utf-8") as f:
                    self.system_prompt.delete("1.0", "end")
                    self.system_prompt.insert("1.0", f.read())
                    self.log("Промпт загружен.")
            except Exception as e: self.log(f"Ошибка промпта: {e}")

    def setup_transcription_tab(self):
        tab = self.tabview.tab("1. Транскрибация")
        tab.grid_columnconfigure(0, weight=1)
        self.file_frame = ctk.CTkFrame(tab)
        self.file_frame.pack(fill="x", padx=10, pady=10)
        self.label_file = ctk.CTkLabel(self.file_frame, text="Аудио не выбрано", text_color="gray")
        self.label_file.pack(side="left", padx=10, fill="x", expand=True)
        ctk.CTkButton(self.file_frame, text="Выбрать файл", command=self.browse_file).pack(side="left", padx=10)

        self.action_frame = ctk.CTkFrame(tab, fg_color="transparent")
        self.action_frame.pack(fill="x", padx=10, pady=5)
        self.btn_start = ctk.CTkButton(self.action_frame, text="РАСШИФРОВАТЬ ЗВОНОК", height=45, state="disabled", command=self.start_transcription_thread)
        self.btn_start.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.btn_save_text = ctk.CTkButton(self.action_frame, text="СОХРАНИТЬ ТЕКСТ", height=45, command=self.save_text, fg_color="#2b719e")
        self.btn_save_text.pack(side="left", fill="x", expand=True, padx=(5, 0))

        self.text_output = ctk.CTkTextbox(tab, height=400)
        self.text_output.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_analysis_tab(self):
        tab = self.tabview.tab("2. Аналитика LLM")
        tab.grid_columnconfigure(0, weight=1)
        ctk.CTkButton(tab, text="ЗАГРУЗИТЬ ТЕКСТ ИЗ ФАЙЛА .TXT", command=self.load_text_file, fg_color="#2b719e").pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(tab, text="Промпт для Gemma 4:", font=ctk.CTkFont(weight="bold")).pack(padx=10, anchor="w")
        self.system_prompt = ctk.CTkTextbox(tab, height=150)
        self.system_prompt.pack(fill="x", padx=10, pady=5)
        self.btn_analyze = ctk.CTkButton(tab, text="ЗАПУСТИТЬ АНАЛИЗ GEMMA 4", height=50, fg_color="#4285F4", command=self.start_analysis_thread)
        self.btn_analyze.pack(fill="x", padx=10, pady=15)
        self.analysis_output = ctk.CTkTextbox(tab, height=350)
        self.analysis_output.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_settings_tab(self):
        tab = self.tabview.tab("Настройки")
        tab.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(tab, text="Пути файлов", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        self.create_setting_row(tab, "Ключ Groq:", "groq")
        self.create_setting_row(tab, "Ключ Google:", "google")
        self.create_setting_row(tab, "Промпт Анализа:", "prompt")
        ctk.CTkButton(tab, text="СОХРАНИТЬ И ПРИМЕНИТЬ", height=45, fg_color="green", command=self.apply_settings).pack(pady=40)

    def create_setting_row(self, parent, label, attr_type):
        frame = ctk.CTkFrame(parent); frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(frame, text=label, width=120).pack(side="left", padx=10)
        entry = ctk.CTkEntry(frame)
        val = getattr(self, f"{attr_type}_key_path") if attr_type != "prompt" else self.prompt_path
        entry.insert(0, val); entry.pack(side="left", fill="x", expand=True, padx=10)
        setattr(self, f"entry_{attr_type}_path", entry)
        ctk.CTkButton(frame, text="Обзор", width=80, command=lambda: self.browse_setting_file(attr_type)).pack(side="left", padx=10)

    def browse_setting_file(self, attr_type):
        path = filedialog.askopenfilename()
        if path:
            entry = getattr(self, f"entry_{attr_type}_path")
            entry.delete(0, "end"); entry.insert(0, path)

    def apply_settings(self):
        self.groq_key_path = self.entry_groq_path.get()
        self.google_key_path = self.entry_google_path.get()
        self.prompt_path = self.entry_prompt_path.get()
        self.save_config(); self.init_api(); self.load_initial_prompt()
        messagebox.showinfo("Инфо", "Настройки сохранены!")

    def setup_logs_tab(self):
        tab = self.tabview.tab("Логи")
        tab.grid_columnconfigure(0, weight=1); tab.grid_rowconfigure(0, weight=1)
        self.log_output = ctk.CTkTextbox(tab, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_output.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        ctk.CTkButton(tab, text="Копировать логи", command=self.copy_logs).grid(row=1, column=0, pady=5)

    def log(self, message):
        self.log_output.insert("end", f"{message}\n"); self.log_output.see("end")
        self.label_status.configure(text=f"Статус: {message[:40]}")
        self.update_idletasks()

    def browse_file(self):
        fn = filedialog.askopenfilename(filetypes=[("Audio", "*.wav *.mp3 *.m4a *.flac"), ("All", "*.*")])
        if fn:
            self.audio_path = fn
            self.label_file.configure(text=os.path.basename(fn), text_color="white")
            self.btn_start.configure(state="normal")

    def load_text_file(self):
        fn = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
        if fn:
            with open(fn, "r", encoding="utf-8") as f:
                self.text_output.delete("1.0", "end")
                self.text_output.insert("1.0", f.read())
                self.tabview.set("1. Транскрибация")

    def start_transcription_thread(self):
        if not self.groq_client: return
        self.btn_start.configure(state="disabled")
        self.tabview.set("Логи")
        threading.Thread(target=self.run_transcription).start()

    def run_transcription(self):
        temp_audio = None
        try:
            current_audio = self.audio_path
            file_size = os.path.getsize(self.audio_path) / (1024 * 1024)
            
            if file_size > 25:
                self.log(f"Файл {file_size:.1f}MB больше лимита. Сжимаю...")
                temp_audio = os.path.join(tempfile.gettempdir(), "compressed_audio.mp3")
                cmd = ["ffmpeg", "-y", "-i", self.audio_path, "-vn", "-ar", "16000", "-ac", "1", "-b:a", "64k", temp_audio]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                current_audio = temp_audio
                self.log(f"Сжато до {os.path.getsize(temp_audio)/(1024*1024):.1f}MB")

            self.log("Отправка в Groq Cloud...")
            with open(current_audio, "rb") as f:
                res = self.groq_client.audio.transcriptions.create(
                    file=(os.path.basename(current_audio), f.read()),
                    model="whisper-large-v3", response_format="text", language="ru"
                )
            self.text_output.delete("1.0", "end")
            self.text_output.insert("1.0", res)
            self.log("Транскрибация завершена!")
            self.tabview.set("1. Транскрибация")
        except Exception as e: self.log(f"Ошибка: {e}")
        finally:
            self.btn_start.configure(state="normal")
            if temp_audio and os.path.exists(temp_audio): os.remove(temp_audio)

    def start_analysis_thread(self):
        if not self.google_client: return
        text = self.text_output.get("1.0", "end").strip()
        if not text: return
        self.btn_analyze.configure(state="disabled")
        self.tabview.set("Логи")
        threading.Thread(target=self.run_analysis).start()

    def run_analysis(self):
        try:
            self.log("Gemma 4 анализирует...")
            full_prompt = f"{self.system_prompt.get('1.0', 'end').strip()}\n\nТЕКСТ:\n{self.text_output.get('1.0', 'end').strip()}"
            if not LEGACY_SDK:
                res = self.google_client.models.generate_content(model='gemma-4-31b-it', contents=full_prompt).text
            else:
                res = self.google_client.generate_content(full_prompt).text
            self.analysis_output.delete("1.0", "end")
            self.analysis_output.insert("1.0", res)
            self.log("Анализ завершен!")
            self.tabview.set("2. Аналитика LLM")
        except Exception as e: self.log(f"Ошибка LLM: {e}")
        finally: self.btn_analyze.configure(state="normal")

    def save_text(self):
        text = self.text_output.get("1.0", "end").strip()
        if not text: return
        fn = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")])
        if fn:
            with open(fn, "w", encoding="utf-8") as f: f.write(text)
            messagebox.showinfo("Успех", "Текст сохранен!")

    def copy_logs(self):
        self.clipboard_clear(); self.clipboard_append(self.log_output.get("1.0", "end"))

if __name__ == "__main__":
    app = UnifiedTranscriptionApp(); app.mainloop()
