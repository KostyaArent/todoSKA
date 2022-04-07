

data = JSON.stringify({
    headline: "Testing",
    tag: "Testing",
    background_image: "Testing",
    content: "Testing",
    user: 1
})

let csrftoken = getCookie('csrftoken');
let response = fetch(url, {
    method: 'POST',
    body: data,
    headers: { 'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        "X-CSRFToken": csrftoken },
})


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
}

$(document).ready(function () {
  $('.closeTodo.td.select').change(function (e) {
    const targetId = $(this).attr("action")
    console.log(targetId)
} }
