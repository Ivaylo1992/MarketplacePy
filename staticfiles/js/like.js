document.addEventListener("DOMContentLoaded", function () {
const likeBtns = document.querySelectorAll('.like-btn');

likeBtns.forEach(btn => {
    btn.addEventListener('click', function(event) {
        const itemId = this.dataset.itemId;

        // Send the AJAX request to toggle like
        fetch(`/api/like/${itemId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            }
        })
        .then(response => response.json())  // Expect JSON response
        .then(data => {
            console.log(data);  // Log the response to see the returned data

            // Toggle the heart icon based on is_liked value
            const heartIcon = this.querySelector('i');
            if (data.is_liked) {
                heartIcon.classList.remove('far');  // Remove 'far' (empty heart)
                heartIcon.classList.add('fas');    // Add 'fas' (filled heart)
                this.classList.add('liked');       // Optional: Add a class to the button
            } else {
                heartIcon.classList.remove('fas');  // Remove 'fas' (filled heart)
                heartIcon.classList.add('far');     // Add 'far' (empty heart)
                this.classList.remove('liked');    // Optional: Remove 'liked' class
            }

            // Update the like count (if you want to display it)
            const likeCount = this.querySelector('.like-count');
            if (likeCount) {
                likeCount.textContent = data.like_count;
            }
        })
        .catch(error => console.error("Error:", error));
    });
});
    // Helper to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});