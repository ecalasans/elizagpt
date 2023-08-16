let tela = document.getElementById("answer_screen");
let txt_question = document.getElementById("user_type");
let btn_send_question = document.getElementById("user_question");
let csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value

// // Adiciona a intro do Eliza na tela
// const intro = document.createElement("p");
// intro.setAttribute("class", ".answer-elizagpt");
// intro.innerHTML = {{ therapist_intro }};
// tela.appendChild(intro);

let mensagens = '';

let url_api = "{% url '" + "send_prompt" + "' %}"

const sendPrompt = async (url_api) => {
    let data = {
        user_prompt: txt_question.value
    }
    console.log(data);

    const response = await fetch(
            url_api, {
                    method: "POST",
                    body: JSON.stringify(data),
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrf_token
                    }
            });
    const resp_json = await response.json();

    console.log(resp_json['elizagpt_answer']);

    const answer_from_elizagpt = document.createElement("p");
    answer_from_elizagpt.setAttribute("class", "answer-elizagpt");
    answer_from_elizagpt.innerHTML = resp_json['elizagpt_answer'];
    tela.appendChild(answer_from_elizagpt);

    tela.scrollTop = tela.scrollHeight;
}

btn_send_question.addEventListener(
    "click",
    (event) => {
        event.preventDefault();
        mensagens = "<p class='prompt-elizagpt'>" + txt_question.value + "</p>";
        tela.innerHTML += mensagens;

        tela.scrollTop = tela.scrollHeight;

        txt_question.value = "";
    }
);
