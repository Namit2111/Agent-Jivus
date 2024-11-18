from summarizer_groq import llama_summarize_content,llama_get_category,get_file
category = llama_get_category(content)
if category == "product_case_study":
    summary = llama_summarize_content(get_file(file_path="product_case_study.pdf"))
elif category == "asking_for_product":
    summary = llama_summarize_content(get_file(file_path="asking_for_product.pdf"))
else:
    summary = llama_summarize_content(get_file(file_path="other.pdf"))