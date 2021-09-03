const quizBox = document.getElementById('quiz-box')
const url = window.location.href


$.ajax({
    type: 'GET',
    url: `${url}quiz/list/`,
    success: function(response){
        const data = response
        data.forEach(el => {
          addList(el)
        })
    },
    error: function(error){
        console.log(error)
    }   
})


function addList(element) {
  quizBox.innerHTML += `
  <tr>
  <td class="px-6 py-4 whitespace-nowrap">
    <div class="flex items-center">

      <div class="ml-4">
        <div class="text-sm font-medium text-black">
          ${element.name} - ${element.id}
        </div>
      </div>
    </div>
  </td>
  <td class="px-6 py-4 whitespace-nowrap">
    <div class="text-sm text-black">${element.number_of_questions}問</div>
  </td>
  <td class="px-6 py-4 whitespace-nowrap">
    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
    ${element.difficulty}
    </span>
  </td>
  <td class="px-6 py-4 whitespace-nowrap text-sm text-black">
  ${element.rimit_time}分
  </td>
  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
    <a href="${url}questions/data/${element.id}" class="text-indigo-600 hover:text-indigo-900">このクイズをうける</a>
  </td>
  </tr>
  `
}









