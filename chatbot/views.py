from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from elizagpt.env import API_KEY
import requests
import json

modelo = "gpt-3.5-turbo"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
link = "https://api.openai.com/v1/chat/completions"

# Create your views here.
def index(request):
    '''
    Ao carregar o site manda uma requisição para a OpenAI API configurando
    o modelo para atuar como um terapeuta psicanalista
    '''

    therapist_config = {
        "model": modelo,
        "messages": [
            {"role": "system", "content": "You are a Freudian psychologist therapist and will help online users with their problems."
                                          "Be friendly but honest with them. Introduce yourself as ElizaGPT and your credentials."
                                          "Be concise in your advices using up to 100 words. "
                                          "Ask some questions about the subject before give a final advice."}
        ],
        "temperature": 0.8,
        "max_tokens": 200
    }

    # Transforma em JSON para ser enviado pelo requests
    json_config = json.dumps(therapist_config)

    # Executa a requisição com a módulo requests e armazena a resposta em prompt_request
    prompt_request = requests.post(
        url=link,
        headers=headers,
        data=json_config
    )

    # Transforma a resposta em JSON
    prompt_answer = prompt_request.json()

    # Captura a parte de interesse
    therapist_intro = prompt_answer['choices'][0]['message']['content']

    return render(
        request,
        template_name='chatbot/index.html',
        context={
            'therapist_intro': therapist_intro
        }
    )

def send_prompt(request):
    if request.method == "POST":
        # Recebe prompt da interface
        prompt_received = json.loads(request.body)

        # Se não for enviado nenhum prompt configura a API para perguntar se o usuário quer falar sobre algo
        if prompt_received['user_prompt'] == '':
            # Constrói o prompt configurado para envio à API
            prompt_to_elizagpt = {
                "model": modelo,
                "messages": [
                    {"role": "system", "content": "Ask to user if he or she wants to keep talking.  Be assertive."}
                ],
                "temperature": 1.0,
                "max_tokens": 80
            }

        # Constrói o prompt configurado para envio à API
        prompt_to_elizagpt = {
            "model": modelo,
            "messages": [
                {"role": "system", "content":  "Limit to the prompt subject.  "
                                               "If user ask something outside of the scope of therapy bring him or her "
                                               "back to the subject in discussion. "
                                               "Give a short answer and ask something more about the theme."},
                {"role": "user", "content": prompt_received['user_prompt']}
            ],
            "temperature": 0.8,
            "max_tokens": 80
        }
        json_config = json.dumps(prompt_to_elizagpt)

        # Envia requisção à API da OpenAI
        request_to_elizagpt = requests.post(
            url=link,
            headers=headers,
            data=json_config
        )

        #  Se houver retorno da API envia a resposta para a interface;  caso contrário envia uma mensagem
        #  dizendo que o ElizaGPT está fora no momento, pedindo para retornar mais tarde
        if request_to_elizagpt.status_code == 200:
            answer_from_elizagpt = request_to_elizagpt.json()

            therapist_answer = answer_from_elizagpt['choices'][0]['message']['content']


            return JsonResponse(
                {"elizagpt_answer":  f"{therapist_answer}"}
            )
        else:
            return JsonResponse(
                {"elizagpt_answer": "Sorry!  I'm out at the time!  Please return later!"}
            )


