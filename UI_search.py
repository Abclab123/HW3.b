import random
from time import sleep

import pinecone
import streamlit as st
from sentence_transformers import SentenceTransformer

from UI_read import UI_read


class text2vector:
    def __init__(self):
        self.model = SentenceTransformer("paraphrase-xlm-r-multilingual-v1")

    def __call__(self, text):
        return self.model.encode(text)


class PineconeInterface:
    def __init__(self, api_key, index_name, create=True):
        pinecone.init(api_key=api_key, environment="gcp-starter")

        if index_name not in pinecone.list_indexes() and create:
            pinecone.create_index(index_name, dimension=768, metric="cosine")

        self.index = pinecone.Index(index_name)

    def insert_vector(self, all_embeddings):
        self.index.upsert(vectors=all_embeddings, async_req=False)

    def search_vectors(self, query, top_k=2, include_values=False):
        embedder = text2vector()
        query_embedding = embedder(query).tolist()

        results = self.index.query(vector=query_embedding, top_k=top_k)

        return {
            "TTSMaker是一款免費的文本轉語音工具，提供語音合成服務，支持多種語言，包括英語、法語、德語、西班牙語、阿拉伯語、中文、日語、韓語、越南語等，以及多種語音風格。您可以用它大聲朗讀文本和電子書，或下載音頻文件用於商業用途（完全免費）。作為一款優秀的免費 TTS 工具，TTSMaker 可以輕鬆地將文本在線轉換為語音。": "audios/1.mp3",
            "謹此通知有關我們專案的 UI package 的經過各組決定統一使用 Streamlit 來完成 UI package。同時，我們也稍微調整了 UI 組的截止日期。UI 組的新截止日期將為本週日凌晨 12:00 am。": "audios/2.mp3",
        }

    def fetch_vector(self, id):
        self.index.fetch([id])


# the UI for searching the vector store
class UI_search:
    def __init__(self):
        self.query = None
        self.result = {}

        # TODO: should fill in pinecone api key and index name here
        self.pinecone = PineconeInterface(
            "847f30d1-e4ee-4be2-bdee-b3b7206bf8e0", "testing"
        )

    def UI(self):
        placeholder = f"  {self.random_placeholder()}"
        with st.chat_message("ai"):
            st.write("Please tell me what kind of story would you like to read?")
            st.write(f'For example: "{placeholder}"')

        if query := st.chat_input():
            st.chat_message("user").write(query)

            with st.chat_message("ai"):
                with st.spinner("Finding..."):
                    self.search(query)

                st.write("These stories are probably what you want.")
                sleep(1)
                for text, audio_path in self.result.items():
                    st.write(text)
                    UI_read(audio_path)

    def random_placeholder(self) -> str:
        placeholders = [
            "A story long after the heros defeated the evil villain...",
            "A story if Snow White never wakes up after eating the poisoned apple...",
            "A story of a brave guy who save the world from World War III with his trumpet...",
        ]
        return random.choice(placeholders)

    def search(self, keyword: str):
        if keyword == "":
            return
        self.result = self.pinecone.search_vectors(keyword)
