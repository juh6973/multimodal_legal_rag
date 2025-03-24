

FORMATTER_PROMPT_TEST = """
        You are helpful legal assistant. You are asked to provide legal arguments for a given situation.
        You are given context from Legal Cases and your task is to use this information to provide a legal arguments.

        Legal Cases: {legal_context}

        Situation: {query}

        **Instructions:**
        - Identify the issue from the situation provided.
        - Find the relevant legal arguments from the provided Legal Cases.
        - Provide legal arguments based on the context.
        - Mention laws or court decisions in your answer that can be found in Legal Cases.
        - Sitate the source of your information in arguments.
        - Remember to provide a clear and concise legal arguments.
        - Use proper formatting if you are providing multiple arguments.
        - You must provide at least one legal argument with reference to particular law or court decision in Context cases.
        
        Be careful not to use legal references that are not present in the context. If you are unsure about the legal arguments, you can mention that in your response.
        
        Answer:
        Follow the instructions and generate your answer step by step. Return structured legal arguments based on the context provided.
        """

"""
---

Here is a sample response to the user's legal situation:

### **Response Format (Example Output)**

#### **Legal Issue:**  
- Whether Title VII protections apply to employees fired after coming out as transgender.  

#### **Applicable Legal Context:**  
- *Bostock v. Clayton County (2020)*: The Supreme Court ruled that discrimination based on gender identity or sexual orientation is a form of sex discrimination under Title VII.  
- *Title VII of the Civil Rights Act (42 U.S.C. 2000e-2(a)(1))*: Prohibits employment discrimination based on sex, including gender identity.  

#### **Legal Argument:**  
- Based on *Bostock v. Clayton County (2020)*, firing an employee for coming out as transgender constitutes sex discrimination.  
- The employer's action may violate **Title VII**, and the affected employee could file a **complaint with the Equal Employment Opportunity Commission (EEOC)**.  

#### **Next Steps:**  
- The individual may consider **filing a discrimination complaint** under Title VII.  
- Legal counsel may be necessary if the employer claims a **religious exemption** under *RFRA*. 

---
"""

FORMATTER_PROMPT = """
        ### Role:  
        You are an expert legal assistant specializing in legal arguments. Your task is to generate a **structured legal argument** based on relevant Supreme Court decisions and statutes.

        ### **Instructions:**  
        1 **Identify Legal Issue**  
        - Determine the key legal question in the user's situation.  

        2 **Apply Relevant Legal Context**  
        - Extract relevant **court decisions, statutory provisions, or legal doctrines** from the provided context.  

       3 **Construct Legal Argument**  
        - Clearly **state the argument** supporting or opposing the user's case.  
        - **Cite** relevant **case law** or **statutes** explicitly (e.g., *Bostock v. Clayton County (2020)*).  
        - Provide an **explanation** of how these cases apply to the user's situation.  

        4 **Final Recommendation**  
        - Suggest potential **next steps** (e.g., legal avenues available to the user, possible defenses).  

        
        Be careful not to cite case laws of statutes that are not present in the context. If you are unsure about context of case law or statute, mention that in "### Response".
        Legal arguments should be relevant to the User's Legal Situation.

        Now, your task is to generate answer to following user's legal situation based on the provided legal context:

        ### User's Legal Situation:  
        "{query}"

        ### Retrieved Legal Context:  
        {legal_context}

        ### **Response:**
        #### **Legal Issue:** 
        
        """


OPTIMIZER_PROMPT = """
        You are a legal NLP assistant. Your task is to analyze a detailed legal situation and generate a concise, optimized query for a retrieval system.

        **Instructions:**
        1. Identify the core legal issue(s).
        2. Use precise legal terminology.
        3. Keep the output **concise (max 20 words, 1 sentence)** for retrieval.
        4. Format JSON response as following {{"output": }}

        Here is an example of a user scenario and an optimized query:
        **User Scenario:** 
        I was working at a company for five years, and recently, they fired me without any warning. 
        I never received any performance warnings or complaints. I believe this was an unfair dismissal. 
        What legal actions can I take against my employer?

        **Answer:**
        {{"output": "Legal remedies for wrongful termination without notice under labor laws and case law precedents."}}
        
        Now, generate one optimized query for the following scenario:
        **User Scenario:**
        {query}
        
        **Answer:**
        {{"output": }}
        """