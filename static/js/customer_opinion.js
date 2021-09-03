const url = window.location.href
console.log(url)

const customerPostForm = document.getElementById('customer-post-form')

const alertBox = document.getElementById('alert-box')

const author = document.getElementById('id_author')
const description = document.getElementById('id_description')
const email = document.getElementById('id_email')
const title = document.getElementById('id_title')


const csrf = document.getElementsByName('csrfmiddlewaretoken')


const handleAlerts = (type, text) =>{
    alertBox.innerHTML = `
    <div class="bg-${type}-100 border border-${type}-400 text-${type}-700 px-4 py-3 rounded relative" role="alert">
    <span class="block sm:inline">${text}</span>
    <span class="absolute top-0 bottom-0 right-0 px-4 py-3">
        <svg class="fill-current h-6 w-6 text-${type}-500" role="button" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><title>Close</title><path d="M14.348 14.849a1.2 1.2 0 0 1-1.697 0L10 11.819l-2.651 3.029a1.2 1.2 0 1 1-1.697-1.697l2.758-3.15-2.759-3.152a1.2 1.2 0 1 1 1.697-1.697L10 8.183l2.651-3.031a1.2 1.2 0 1 1 1.697 1.697l-2.758 3.152 2.758 3.15a1.2 1.2 0 0 1 0 1.698z"/></svg>
    </span>
    </div>
    `
}



customerPostForm.addEventListener('submit', e=>{
    e.preventDefault()

    const formData = new FormData()
    formData.append('csrfmiddlewaretoken', csrf[0].value)
    formData.append('author', author.value)
    formData.append('email', email.value)
    formData.append('title', title.value)
    formData.append('description', description.value)
    $.ajax({
        type: 'POST',
        url: url,
        data: formData,
        success: function(response) {
            console.log(response)
            const successText = `${response.author}さん、貴重なご意見ありがとうございます。`
            handleAlerts('green', successText)
            setTimeout(()=>{
                alertBox.innerHTML = ""
                author.value = ""
                email.value = ""
                title.value = ""
                description.value = ""
            }, 3000)
        },
        error: function(error) {
            console.log(error)
            handleAlerts('red', '空欄を埋めてください。')
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})