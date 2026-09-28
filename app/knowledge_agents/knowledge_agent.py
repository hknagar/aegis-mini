from pathlib import Path

from app.services.vector_store import (
    add_document,
    search_documents
)
from app.services.gemini_service import client


class KnowledgeAgent:

    def load_documents(self, directory: str):

        path = Path(directory)

        documents = []

        for file in path.glob("*.txt"):

            documents.append({
                "source": file.name,
                "text": file.read_text()
            })

        return documents

    def chunk_text(self, text: str, chunk_size: int = 500):

        words = text.split()

        chunks = []

        for i in range(0, len(words), chunk_size):

            chunk = " ".join(
                words[i:i + chunk_size]
            )

            chunks.append(chunk)

        return chunks

    def ingest(self, directory: str):

        documents = self.load_documents(directory)

        for document in documents:

            chunks = self.chunk_text(
                document["text"]
            )

            for index, chunk in enumerate(chunks):

                document_id = (
                    f"{document['source']}_{index}"
                )

                add_document(
                    document_id=document_id,
                    text=chunk,
                    source=document["source"]
                )

    def answer_question(self, question: str):

        results = search_documents(question)

        documents = results["documents"][0]

        context = "\n\n".join(documents)

        prompt = f"""
You are the Acme Retail Knowledge Agent.

Answer the user's question using ONLY the provided
knowledge context.

If the answer is not present in the context,
say that the information is not available.

Knowledge context:

{context}

User question:

{question}
"""

        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        return {
            "answer": response.output_text,
            "sources": results["metadatas"][0]
        }

# the previous lines of code below:
# from pathlib import Path

# from app.services.vector_store import add_document


# class KnowledgeAgent:

#     def load_documents(self, directory: str):

#         path = Path(directory)

#         documents = []

#         for file in path.glob("*.txt"):

#             documents.append({
#                 "source": file.name,
#                 "text": file.read_text()
#             })

#         return documents

#     def chunk_text(self, text: str, chunk_size: int = 500):

#         words = text.split()

#         chunks = []

#         for i in range(0, len(words), chunk_size):

#             chunk = " ".join(
#                 words[i:i + chunk_size]
#             )

#             chunks.append(chunk)

#         return chunks

#     def ingest(self, directory: str):

#         documents = self.load_documents(directory)

#         for document in documents:

#             chunks = self.chunk_text(
#                 document["text"]
#             )

#             for index, chunk in enumerate(chunks):

#                 document_id = (
#                     f"{document['source']}_{index}"
#                 )

#                 add_document(
#                     document_id=document_id,
#                     text=chunk,
#                     source=document["source"]
#                 )

# # below is the previous code
# # from pathlib import Path


# # class KnowledgeAgent:

# #     def load_documents(self, directory: str):

# #         path = Path(directory)

# #         documents = []

# #         for file in path.glob("*.txt"):

# #             documents.append({
# #                 "source": file.name,
# #                 "text": file.read_text()
# #             })

# #         return documents

# #     def chunk_text(self, text: str, chunk_size: int = 500):

# #         words = text.split()

# #         chunks = []

# #         for i in range(0, len(words), chunk_size):

# #             chunk = " ".join(
# #                 words[i:i + chunk_size]
# #             )

# #             chunks.append(chunk)

# #         return chunks