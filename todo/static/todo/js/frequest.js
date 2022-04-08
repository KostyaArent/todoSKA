let csrftoken = getCookie('csrftoken');
let sessionid = getCookie('sessionid');


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};


async function fetchCloseTodo(url, data, csrftoken) {
  const response = await fetch(url, {
      method: 'POST',
      body: data,
      headers: { 'Accept': 'application/json, text/plain, */*',
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken },
  });
  if (!response.ok) {
    const message = `An error has occured: ${response.status}`;
    throw new Error(message);
  }
  console.log(`${response.status}`);
}


$(document).ready(function () {
  $('.closeTodo').change(function (e) {
    const url = $(this).attr("action");
    const status = $("select").closest($(e.target)).val()
    let data = JSON.stringify({
        status: status,
    });
    fetchCloseTodo(url, data, csrftoken).catch(error => {
      console.log(error.message); // 'An error has occurred: 404'
    });
  })
})
