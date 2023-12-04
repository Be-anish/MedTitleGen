# mlapp/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, GenerationConfig
from peft import PeftModel, PeftConfig
import torch
import os

config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'MedTitleGen'))
peft_model_base = AutoModelForSeq2SeqLM.from_pretrained(os.path.join(os.path.dirname(__file__), '..', 'model_falconsai'), local_files_only=True,torch_dtype=torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained(os.path.join(os.path.dirname(__file__), '..', 'model_falconsai'),local_files_only=True)

# Load your PEFT model
peft_model = PeftModel.from_pretrained(peft_model_base,
                                       config_path,
                                       torch_dtype=torch.bfloat16,
                                       is_trainable=False).to('cpu')

@api_view(['POST'])
def predict_title_api(request):
    if request.method == 'POST':
        try:
            input_text = request.data.get('input', '')
            prompt = f"""
            Please summarize the given abstract to a title:
            {input_text}
            """

            # Tokenize and generate output
            input_ids = tokenizer.encode(prompt, return_tensors='pt', max_length=1024, truncation=True).to('cpu')
            peft_model_outputs = peft_model.generate(input_ids=input_ids)
            peft_model_text_output = tokenizer.decode(peft_model_outputs[0], skip_special_tokens=True)

            # Prepare JSON response
            response_data = {'output': peft_model_text_output}
            return Response(response_data)

        except Exception as e:
            return Response({'error': str(e)}, status=500)
