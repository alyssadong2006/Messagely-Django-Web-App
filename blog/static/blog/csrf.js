function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




//dislikes
// const btn2 = document.querySelectorAll('.dislike')
// for (const dislike of btn2) {
//     dislike.addEventListener('click', dislikeHandler);
//     }


// function Like(id) {
//     var csrftoken = getCookie("csrftoken");
//     const response = fetch("/comments/like/"+id+"/", {
//         method: "POST",
//         headers: {
//             "X-CSRFToken": csrftoken,
//         },
//     });
// }

// function Dislike(id) {
//     var csrftoken = getCookie("csrftoken");

//     const response = fetch("/comments/dislike/"+id+"/", {
//         method: "POST",
//         headers: {
//             "X-CSRFToken": csrftoken,
//         },
//     });
// };

// console.log(response)

// const pre = document.querySelector('pre');

// function likeHandler(event) {
// 	event.preventDefault();
  
//   // Get the element that was clicked on. It's the event
//   // currentTarget property.
//   alert("hi")
	
// }

// // Select multiple classes: both like & dislike buttons
// document.querySelectorAll('i')
// 	.forEach(function (link) {
// 		link.addEventListener('click', likeHandler);
// 	});

