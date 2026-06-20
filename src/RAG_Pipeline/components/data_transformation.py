import os
import sys
from dataclasses import dataclass
from typing import List
import json


from src.RAG_Pipeline.exception import CustomException
from src.RAG_Pipeline.logger import logging

from unstructured.chunking.title import chunk_by_title
from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage
from langchain_core.documents import Document






@dataclass
class DataTransformationConfig:
    pass
    # self.transformation




class DataTransformation:

    def __init__(self):
        # pass
        self.data_transformation_config = DataTransformation()

    


    def create_chunks_by_title(elements, max_chars = 3000, new_chunk_start_after = 2400, merge_chunks_under_chars = 500 ):
        """Creating Intelligent chunks using title based strategy"""

        try:
            logging.info(f'Creating Intelligent chunks using title based strategy || {len(elements)} Elements || {max_chars} || {new_chunk_start_after} || {merge_chunks_under_chars}')

            chunks = chunk_by_title(
                elements, # The Parsed PDF elements from previous step
                max_characters=max_chars, # Hard Limit - Never exceeds 3000 character per chunk
                new_after_n_chars=new_chunk_start_after, # Try to start new Chunk after N chars (2400)
                combine_text_under_n_chars=merge_chunks_under_chars # Merge tiny chunks under 500 chars
            )

            logging.info(f"=== Created: {len(chunks)} Chunks ===")

            return chunks
        
        except Exception as e:
            raise CustomException(e, sys)




    def get_chunk_detail(chunks, idx):
        '''Find Chunk details through Index'''
        try:
            # pass
            return chunks[idx].to_dict()

        except IndexError as e:
            logging.error(e)
        except Exception as e:
            raise CustomException(e, sys)




    def seperate_content_types(chunk):
        """Analyze what type of content are in a Chunk"""

        try:

            content_data = {
                'text': chunk.text,
                'tables': [],
                'images': [],
                'types': ['text']
            }

            # Check for tables and images in original elements
            if hasattr(chunk, 'metadata') and hasattr(chunk.metadata, 'orig_elements'):
                for element in chunk.metadata.orig_elements:
                    element_type = type(element).__name__

                    # Handle Tables
                    if element_type == 'Table':
                        content_data['types'].append('table')
                        table_html = getattr(element.metadata, 'text_as_html', element.text)
                        content_data['tables'].append(table_html)

                    # Handle Images
                    elif element_type == 'Image':
                        if hasattr(element, 'metadata') and hasattr(element.metadata, 'image_base64'):
                            content_data['types'].append('image')
                            content_data['images'].append(element.metadata.image_base64)

            content_data['types'] = list(set(content_data['types']))
            return content_data
        
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)




    def create_AI_enhanced_summary(text: str, tables: List[str], images: List[str], model='deepseek-v3.1:671b-cloud', temp = 0) -> str:
        """Create AI Enhanced Summary for Mixed Content"""

        try:

            llm_model = ChatOllama(
                model=model,
                temperature=temp
            )

            prompt_text = f"""You are creating a searchable description for document content retrieval.
            
            CONTENT TO ANALYZE:
            TEXT CONTENT:
            {text}
            """

            # Add tables if Present

            if tables:
                prompt_text += "TABLES:\n"

                for i, table in enumerate(tables):
                    prompt_text += f"Table {i+1}: \n{table}\n\n"

                    prompt_text += """
                    YOUR TASK:
                    Generate a comprehensive, searchable description that covers:

                    1. Key facts, numbers and data points from text and tables
                    2. Main topics & concepts discussed
                    3. Questions this content could answer
                    4. Visual content analysis (charts, diagrams, patterns in images)
                    5. Alternative search terms users might use

                    Make it detailed and searchable - prioritize findability over brevity.

                    SEARCHABLE DESCRIPTION:
                    """

            # Build message content starting with text
            message_content = [{'type': 'text', 'text': prompt_text}]

            # Add Images to the message
            if images:
                for image in images:
                    message_content.append({
                        'type': 'image_url',
                        'image_url': {'url': f"data:image/jpeg;base64,{image}"}
                    })
            
            message = HumanMessage(content=message_content)

            response = llm_model.invoke(message)
            return response.content
        
        except Exception as ex:
            logging.warning(f"AI Summary Failed: {ex}")


            # Fallback to Simple Summary
            summary = f"{text[:300]}..."

            if tables:
                summary += f" [Contains {len(tables)} table(s)]"
            if images:
                summary += f" [Containes {len(images)} image(s)]"

            return summary
    




    def summarize_chunks(self, chunks):
        """Process All Chunks with AI Summaries"""
        logging.info("Processing Chunks with AI Summaries")

        try:
            langchain_documents = []

            total_chunks = len(chunks)

            for i, chunk in enumerate(chunks):
                current_chunk = i + 1
                logging.info(f">>  Processing Chunk  {current_chunk}/{total_chunks} -----------")

                # Analyze Chunk Content
                content_data = self.seperate_content_types(chunk)

                # Debug prints
                logging.info(f"------->>  Types Found: {content_data['types']} ------------")
                logging.info(f"------->>  Tables: {len(content_data['tables'])} Tables ------------")
                logging.info(f"------->>  Images: {len(content_data['images'])} Images ------------")

                # Create AI-Enhanced Summary if Chunk has Tables & Images
                if content_data['tables'] or content_data['images']:
                    logging.info(f"-------->> Creating AI summary for Mixed Content...")

                    try:
                        enhanced_content = self.create_AI_enhanced_summary(
                            content_data['text'],
                            content_data['tables'],
                            content_data['images'],
                        )

                        logging.info(f"------->> AI Summary Created Successfully")
                        logging.info(f"------->> Enhanced Content Preview: {enhanced_content[:200]}...")

                    except Exception as e:
                        logging.info(f"AI Summary Failed...")
                        enhanced_content = content_data['text']

                # If chunk does not have any Table or Image
                else:
                    logging.info(f"------->> Using only raw Text (No Tables/Images)")
                    enhanced_content = content_data['text']

                
                # Create LangChain Document with Rich Metadata
                doc = Document(
                    page_content=enhanced_content,
                    metadata = {
                        "original_content": json.dumps({
                            "raw_text": content_data['text'],
                            "tables_html": content_data['tables'],
                            "images_base64": content_data['images']
                        })
                    }
                )

                langchain_documents.append(doc)

            logging.info(f">> Processed {len(langchain_documents)} Chunks")
            return langchain_documents
        
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)
    


