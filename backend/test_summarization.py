# Test script for summarization service
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from app.services.analysis.summarization import summarization_service

def test_summarization():
    """Test the summarization service with sample texts."""
    print("\nTesting Summarization Service")
    print("============================")
    
    # Test article text
    article_text = """
    Artificial intelligence is transforming industries across the global economy. Companies are racing to implement AI solutions to improve efficiency, cut costs, and develop new products and services. This technological revolution has significant implications for the workforce, with automation potentially displacing certain jobs while creating new roles that require different skills.

    Recent advances in large language models have demonstrated remarkable capabilities in natural language processing. These models can now perform tasks like drafting emails, writing code, and translating languages with impressive accuracy. However, concerns about bias, privacy, and the environmental impact of training these models persist.

    Governments worldwide are grappling with how to regulate AI development and deployment. The European Union has proposed comprehensive AI regulations that would classify AI systems according to their potential risk and impose different requirements based on those classifications. Meanwhile, the United States has taken a more sector-specific approach to regulation.

    In healthcare, machine learning algorithms trained on large medical datasets can identify patterns that might escape human observation. However, integrating these tools into clinical workflows presents challenges, and questions about liability and patient privacy remain unresolved.

    The financial sector is leveraging blockchain technology and neural networks for fraud detection, risk assessment, and algorithmic trading. Banks are using machine learning to analyze transaction data and identify suspicious activities in real-time. Investment firms are employing AI to analyze market trends and make trading decisions.

    Despite the potential benefits, the rapid adoption of AI raises important ethical questions. How do we ensure that AI systems are fair and don't perpetuate existing biases? Who is responsible when an AI system makes a mistake? How can we protect privacy in an era of increasingly sophisticated data analysis?

    As quantum computing and big data techniques continue to evolve, collaboration between technologists, policymakers, ethicists, and the public will be essential to harness the benefits of these technologies while mitigating potential harms. The decisions we make today about how to develop and govern AI will shape its impact on society for generations to come.
    """
    
    print("\nGenerating summaries for sample article text...")
    
    try:
        # Generate summaries
        extractive_summary = summarization_service.generate_extractive_summary(article_text)
        beginner_summary = summarization_service.generate_beginner_summary(article_text)
        technical_summary = summarization_service.generate_technical_summary(article_text)
        
        # Print results
        print("\nExtractive Summary:")
        print(extractive_summary)
        print(f"Length: {len(extractive_summary.split())} words")
        
        print("\nBeginner Summary:")
        print(beginner_summary)
        print(f"Length: {len(beginner_summary.split())} words")
        
        print("\nTechnical Summary:")
        print(technical_summary)
        print(f"Length: {len(technical_summary.split())} words")
        
        # Test with an actual article structure
        print("\nTesting with article data structure...")
        article_data = {
            "title": "Advances in Quantum Computing Break New Ground in Cryptography",
            "description": "Researchers have developed quantum algorithms that could revolutionize encryption methods while raising concerns about current security standards.",
            "content": "A team of computer scientists from MIT and Google have announced a breakthrough in quantum computing that could have far-reaching implications for cybersecurity and encryption. The researchers successfully demonstrated a new quantum algorithm that can factor large numbers exponentially faster than current methods, potentially threatening widely-used RSA encryption that secures much of our digital infrastructure.\n\nThe quantum computer used in the experiment, equipped with 72 qubits, was able to solve complex mathematical problems that would take traditional supercomputers thousands of years to complete. 'This represents a significant milestone in quantum computing's progress toward practical applications,' said Dr. Eleanor Chen, lead researcher on the project.\n\nCryptography experts are urging organizations to accelerate their transition to quantum-resistant encryption standards. The National Institute of Standards and Technology (NIST) has been working on post-quantum cryptography standards, which are now gaining renewed attention.\n\nHowever, the researchers emphasized that commercial applications are still years away, as current quantum systems require extreme cooling and are prone to error. 'We're demonstrating what's theoretically possible, but practical, widespread deployment faces significant engineering challenges,' noted Dr. Chen.\n\nThe breakthrough has sparked debates about data security, with some experts recommending that organizations start inventorying their cryptographically protected data and developing quantum transition plans. Critics worry that sensitive data encrypted today could be vulnerable to decryption in the future when more powerful quantum computers become available - a concern known as 'harvest now, decrypt later' attacks."
        }
        
        summaries = summarization_service.summarize_article(article_data)
        
        print("\nArticle Summaries:")
        print("\nExtractive:")
        print(summaries['extractive'])
        print(f"Length: {len(summaries['extractive'].split())} words")
        
        print("\nBeginner:")
        print(summaries['beginner'])
        print(f"Length: {len(summaries['beginner'].split())} words")
        
        print("\nTechnical:")
        print(summaries['technical'])
        print(f"Length: {len(summaries['technical'].split())} words")
        
    except Exception as e:
        print(f"Error in test: {e}")
    
    return True

if __name__ == "__main__":
    test_summarization()