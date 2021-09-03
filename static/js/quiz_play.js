console.log('hello')

const url = window.location.href
const questionBox = document.getElementById('question-box')
const questionForm = document.getElementById('question-form')
const resultBox = document.getElementById('result-box')
const timerBox = document.getElementById('timer-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const activateTimer = (time) => {

    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>残り0${time}:00</b>`
    } else {
        timerBox.innerHTML = `<b>残り${time}:00</b>`
    }
    let minutes = time - 1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    const timer = setInterval(()=>{
        seconds -- 
        if (seconds < 0) {
            seconds = 59
            minutes --
        }
        if (minutes.toString().length < 2) {
            displayMinutes = '0' + minutes
        } else {
            displayMinutes = minutes
        }
        if (seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        } else {
            displaySeconds = seconds
        }
        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = "<b>00:00</b>"
            setTimeout(()=> {
                clearInterval(timer)
                alert('Time Over')
                sendData()
            },500)
            
        }
        timerBox.innerHTML = `<b>残り${displayMinutes}:${displaySeconds}</b>`
    },1000)
}

$.ajax({
    type: 'GET',
    url: `${url}data/`,
    success: function(response){
        const data = response.data
        let count = 0
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)){
                count ++
                questionBox.innerHTML += `
                <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt class="text-sm font-medium text-gray-500">
                    ${count}問
                    </dt>
                    <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    ${question}
                    </dd>
                </div>
                `
                answers.forEach(answer =>{
                    
                    questionBox.innerHTML += `

                    <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt class="text-sm font-medium text-gray-500">
                        </dt>
                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                        <input class="form-radio ans text-sm" type="radio" id="${question}-${answer}" name="${question}"  value="${answer}">
                        <span class="ml-2" for="${question}">${answer}</span>
                        </dd>
                    </div>
                    `
                })
            }
        });
        activateTimer(response.time)
    },
    error: function(error){
        console.log(error)
    },
})




const sendData = function(){
    const ansElements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    ansElements.forEach(el =>{
        if (el.checked){
            data[el.name] = el.value
        } else {
            if(!data[el.name]){
                data[el.name] = null
            }
        }
    });
    $.ajax({
        type: 'POST',
        url: `${url}result/`,
        data: data,
        success: function(response) {
            questionForm.classList.add('not-visible')
            const results = response.results
            console.log('results', results)
            results.forEach(result => {
                console.log('result', result)
                for (const [quesiton, information] of Object.entries(result)){
                    console.log('quetion', quesiton)
                    const yourAnswer = information.your_answer
                    const correctAnswer = information.correct_answer
                    const expalaination = information.question_expalination.expalaination
                    const explaination_source = information.question_expalination.explaination_source
                    console.log(yourAnswer)
                    console.log(correctAnswer)
                    console.log(expalaination)
                    console.log(explaination_source)
                    resultBox.innerHTML += `
                    <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt class="text-sm font-medium text-gray-500">
                        問題
                        </dt>
                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                        ${quesiton}
                        </dd>
                    </div>
                    <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt class="text-sm font-medium text-gray-500">
                        答え
                        </dt>
                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                        ${correctAnswer}
                        </dd>
                    </div>
                    <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt class="text-sm font-medium text-gray-500">
                        解説
                        </dt>
                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                        ${expalaination}
                        </dd>
                    </div>
                    <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt class="text-sm font-medium text-gray-500">
                        ソース
                        </dt>
                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                        ${explaination_source}
                        </dd>
                    </div>
                    `
                }
            })
        },
        error: function(error) {
            console.log(error)
        }
    })
}

questionForm.addEventListener('submit', e=>{
    e.preventDefault()
    sendData()
})