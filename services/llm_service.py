from typing import List, Dict, Any, AsyncGenerator
from openai import AsyncOpenAI
from app.settings import settings


class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.LLM_MODEL
    
    def _build_prompt(self, question: str, context: List[Dict[str, Any]]) -> str:
        context_text = "\n\n".join([
            f"Document: {chunk['title']}\n{chunk['content']}"
            for chunk in context
        ])
        
        prompt = f"""You are a helpful assistant that answers questions based on the provided context.

Context:
{context_text}

Question: {question}

Instructions:
- Answer the question based ONLY on the information provided in the context above
- If the context doesn't contain enough information to answer the question, say so
- Be concise but comprehensive
- If you quote from the context, mention which document it's from

Answer:"""
        
        return prompt
    
    async def generate_answer(
        self,
        question: str,
        context: List[Dict[str, Any]],
        temperature: float = 0.7
    ) -> str:
        """
        Generate answer using LLM
        
        Args:
            question: User question
            context: List of relevant document chunks
            temperature: LLM temperature
            
        Returns:
            Generated answer
        """
        prompt = self._build_prompt(question, context)
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based on provided documents."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()
    
    async def generate_answer_stream(
        self,
        question: str,
        context: List[Dict[str, Any]],
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """
        Generate answer with streaming
        
        Args:
            question: User question
            context: List of relevant document chunks
            temperature: LLM temperature
            
        Yields:
            Answer chunks
        """
        prompt = self._build_prompt(question, context)
        
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based on provided documents."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=1000,
            stream=True
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    
    def is_initialized(self) -> bool:
        """Check if LLM service is initialized"""
        return self.client is not None
