import re

def read_questions_from_input_file(file_name):
    file = open(file_name, "r")
    doc_list = [line for line in file]
    doc_str = ''.join(doc_list)
    faq_sentences = re.split(r'[\n\r.!?]', doc_str)
    return faq_sentences