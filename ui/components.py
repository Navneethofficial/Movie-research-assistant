import tkinter as tk
from tkinter import scrolledtext, ttk
import webbrowser
import re
from ui.styles import apply_text_styles, ThemeManager


class ConversationDisplay(ttk.LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="Conversation History", padding=10, **kwargs)

        container = ttk.Frame(self, padding=5)
        container.pack(fill=tk.BOTH, expand=True)

        header_frame = ttk.Frame(container)
        header_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(
            header_frame,
            text="🔍 Movie Assistant Chat",
            font=("Segoe UI", 12, "bold"),
            foreground=ThemeManager.COLORS["primary"]
        ).pack(side=tk.LEFT)

        self.history_text = scrolledtext.ScrolledText(
            container,
            wrap=tk.WORD,
            width=80,
            height=20
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)

        apply_text_styles(self.history_text)

        self.history_text.config(state=tk.DISABLED)

    # --------------------------------------------------------
    # UPDATE HISTORY
    # --------------------------------------------------------
    def update_history(self, conversation_history):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)

        for entry in conversation_history:
            if entry["role"] == "user":
                self.history_text.insert(tk.END, "You: ", "user")
                self.history_text.insert(tk.END, f"{entry['content']}\n\n", "user")

            elif entry["role"] == "assistant":
                self.history_text.insert(tk.END, "Assistant: ", "assistant")
                self.history_text.insert(tk.END, f"{entry['content']}\n\n", "assistant")

            elif entry["role"] == "tool":
                self.history_text.insert(tk.END, "─" * 80 + "\n", "tool_header")
                tool_name = entry["tool"]

                # Display tool name with emoji
                if tool_name == "YouTube Search":
                    self.history_text.insert(tk.END, f"🎬 Trailer Search: '{entry['query']}'\n", "tool_header")
                else:
                    self.history_text.insert(tk.END, f"{tool_name}: '{entry['query']}'\n", "tool_header")

                # Show results based on tool type
                results = entry["results"].get("results", [])
                if results:
                    if tool_name == "DuckDuckGo Search":
                        self._insert_duckduckgo_results(results)
                    elif tool_name == "OMDB Search":
                        self._insert_omdb_results(results)
                    elif tool_name == "YouTube Search":
                        self._insert_youtube_results(results)
                    elif tool_name == "Google Search":
                        self._insert_google_results(results)     # <── NEW LINE (required)
                else:
                    error = entry["results"].get("error", "No results found")
                    self.history_text.insert(tk.END, f"⚠️ No results: {error}\n", "tool_error")

                self.history_text.insert(tk.END, "─" * 80 + "\n\n", "tool_header")

        self.history_text.config(state=tk.DISABLED)
        self.history_text.see(tk.END)

    # --------------------------------------------------------
    # GOOGLE SEARCH (NEW)
    # --------------------------------------------------------
    def _insert_google_results(self, results):
        self.history_text.insert(tk.END, "🌐 Google Search Results:\n", "tool_section")

        for i, r in enumerate(results, 1):
            title = r.get("title", "")
            snippet = r.get("snippet", "")
            link = r.get("link", "")

            self.history_text.insert(tk.END, f"{i}. {title}\n", "tool_item")
            self.history_text.insert(tk.END, f"{snippet}\n", "tool_detail")
            self.history_text.insert(tk.END, "Source: ", "tool_link_label")

            # clickable link
            start = self.history_text.index(tk.INSERT)
            self.history_text.insert(tk.END, f"{link}\n\n", "tool_link")
            end = self.history_text.index(tk.INSERT)

            tag = f"google_{i}_{hash(link)}"
            self.history_text.tag_add(tag, start, end)
            self.history_text.tag_config(tag, foreground=ThemeManager.COLORS["link"], underline=1)
            self.history_text.tag_bind(tag, "<Button-1>", lambda e, url=link: webbrowser.open(url))

    # --------------------------------------------------------
    # DUCKDUCKGO RESULTS
    # --------------------------------------------------------
    def _insert_duckduckgo_results(self, results):
        self.history_text.insert(tk.END, "📊 IMDB Information:\n", "tool_section")

        movie_info = {}
        for result in results:
            title = result.get("title", "")
            snippet = result.get("snippet", "")

            if "rating" in snippet.lower() and "rating" not in movie_info:
                m = re.search(r"(\d+(\.\d+)?)/10", snippet)
                if m:
                    movie_info["rating"] = m.group(0)

            if "release" in snippet.lower() and "release_date" not in movie_info:
                d = re.search(r"released on ([A-Za-z]+ \d+, \d{4})", snippet)
                if d:
                    movie_info["release_date"] = d.group(0)

        if movie_info:
            main_title = results[0].get("title", "Movie")
            self.history_text.insert(tk.END, f"🎬 {main_title}\n", "movie_title")

            if "rating" in movie_info:
                self.history_text.insert(tk.END, f"Rating: ⭐ {movie_info['rating']}\n", "info_value_bold")

            if "release_date" in movie_info:
                self.history_text.insert(tk.END, f"Released: {movie_info['release_date']}\n", "info_value")

            self.history_text.insert(tk.END, "\n", "tool_detail")

        # Normal results
        self.history_text.insert(tk.END, "🔍 Search Results:\n", "results_header")

        for i, r in enumerate(results, 1):
            title = r.get("title", "")
            snippet = r.get("snippet", "")
            link = r.get("link", "")

            self.history_text.insert(tk.END, f"{i}. {title}\n", "tool_item")
            self.history_text.insert(tk.END, f"{snippet}\n", "tool_detail")
            self._insert_clickable_link(link, prefix=i)

    # --------------------------------------------------------
    # OMDB RESULTS
    # --------------------------------------------------------
    def _insert_omdb_results(self, results):
        self.history_text.insert(tk.END, "🎬 Movie Details:\n", "tool_section")

        for i, r in enumerate(results, 1):
            title = r.get("title")
            year = r.get("year")
            rating = r.get("rating")
            genre = r.get("genre")
            director = r.get("director")
            actors = r.get("actors")
            plot = r.get("plot")
            imdb = r.get("imdbLink")

            self.history_text.insert(tk.END, f"{i}. {title} ({year})\n", "tool_item")
            self.history_text.insert(tk.END, f"Rating: ⭐ {rating}/10\n", "tool_detail")
            self.history_text.insert(tk.END, f"Genre: {genre}\n", "tool_detail")
            self.history_text.insert(tk.END, f"Director: {director}\n", "tool_detail")
            self.history_text.insert(tk.END, f"Cast: {actors}\n", "tool_detail")
            self.history_text.insert(tk.END, f"Plot: {plot}\n", "tool_detail")

            self._insert_clickable_link(imdb)

            self.history_text.insert(tk.END, "\n")

    # --------------------------------------------------------
    # YOUTUBE RESULTS
    # --------------------------------------------------------
    def _insert_youtube_results(self, results):
        self.history_text.insert(tk.END, "🎥 Trailer:\n", "tool_section")

        for i, r in enumerate(results, 1):
            title = r.get("title")
            link = r.get("link")

            self.history_text.insert(tk.END, f"🎬 {title}\n", "tool_item")
            self._insert_clickable_link(link)
            self.history_text.insert(tk.END, "\n")

    # --------------------------------------------------------
    # HELPER: clickable link
    # --------------------------------------------------------
    def _insert_clickable_link(self, link, prefix=""):
        self.history_text.insert(tk.END, "Source: ", "tool_link_label")

        start = self.history_text.index(tk.INSERT)
        self.history_text.insert(tk.END, f"{link}\n", "tool_link")
        end = self.history_text.index(tk.INSERT)

        tag = f"link_{prefix}_{hash(link)}"
        self.history_text.tag_add(tag, start, end)
        self.history_text.tag_config(tag, foreground=ThemeManager.COLORS["link"], underline=1)
        self.history_text.tag_bind(tag, "<Button-1>", lambda e, url=link: webbrowser.open(url))



# ====================================================================
# QUERY INPUT UI
# ====================================================================
class QueryInput(ttk.Frame):
    def __init__(self, parent, submit_callback, model_change_callback, **kwargs):
        super().__init__(parent, padding=10, **kwargs)

        self.submit_callback = submit_callback

        ttk.Label(
            self,
            text="💬 Ask about a movie or show:",
            font=("Segoe UI", 11, "bold"),
            foreground=ThemeManager.COLORS["primary"]
        ).pack(anchor=tk.W, pady=(0, 5))

        row = ttk.Frame(self)
        row.pack(fill=tk.X, pady=(0, 10))

        self.query_entry = ttk.Entry(row, width=70)
        self.query_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.query_entry.bind("<Return>", self.on_submit)

        ttk.Button(
            row,
            text="Search",
            style="Main.TButton",
            command=self.on_submit
        ).pack(side=tk.RIGHT)

        # Model selection
        model_row = ttk.Frame(self, padding=5)
        model_row.pack(fill=tk.X)

        ttk.Label(
            model_row,
            text="🤖 Model:",
            foreground=ThemeManager.COLORS["secondary"]
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.model_var = tk.StringVar(value="llama-3.1-8b-instant")
        model_box = ttk.Combobox(
            model_row,
            textvariable=self.model_var,
            state="readonly",
            width=30
        )
        model_box["values"] = (
            "llama-3.1-8b-instant",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "meta-llama/llama-4-maverick-17b-128e-instruct",
        )
        model_box.pack(side=tk.LEFT)
        model_box.bind("<<ComboboxSelected>>", lambda e: model_change_callback(self.model_var.get()))

        ttk.Label(
            self,
            text="Try: 'Tell me about The Batman' or 'Show me info about Oppenheimer'",
            font=("Segoe UI", 9, "italic"),
            foreground=ThemeManager.COLORS["text_light"]
        ).pack(anchor=tk.W)

        self.query_entry.focus_set()

    def on_submit(self, event=None):
        text = self.query_entry.get().strip()
        if text:
            self.submit_callback(text)
            self.query_entry.delete(0, tk.END)

    def set_state(self, state):
        self.query_entry.config(state=state)
