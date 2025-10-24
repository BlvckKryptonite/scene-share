// Burger Script
      const burger = document.querySelector(".burger");
      const nav = document.querySelector(".nav-links");
      burger.addEventListener("click", () => {
        nav.classList.toggle("active");
      });

//  Movie Descriptions - Read More / Show Less logic
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.movie-description').forEach(desc => {
    const fullText = desc.textContent.trim();
    const maxLength = 150; // adjust character limit as desired

    if (fullText.length > maxLength) {
      const shortText = fullText.slice(0, maxLength).trim();
      desc.innerHTML = `
        <span class="short-text">${shortText}...</span>
        <span class="full-text" style="display:none;">${fullText}</span>
        <span class="read-more">Read More</span>
      `;

      const readMoreBtn = desc.querySelector('.read-more');
      readMoreBtn.addEventListener('click', () => {
        const shortTextSpan = desc.querySelector('.short-text');
        const fullTextSpan = desc.querySelector('.full-text');

        const isCollapsed = fullTextSpan.style.display === 'none';
        shortTextSpan.style.display = isCollapsed ? 'none' : 'inline';
        fullTextSpan.style.display = isCollapsed ? 'inline' : 'none';
        readMoreBtn.textContent = isCollapsed ? 'Show Less' : 'Read More';
      });
    }
  });
});

// Toggle Reviews' Visibility
document.querySelectorAll('.toggle-reviews').forEach(btn => {
  btn.addEventListener('click', () => {
    const list = document.querySelector(btn.dataset.target);
    list.classList.toggle('active');
    btn.textContent = list.classList.contains('active') ? 'Hide Reviews' : 'Show Reviews';
  });
});


// Review LIKE button AJAX script:
document.addEventListener('DOMContentLoaded', function() {
  const likeForms = document.querySelectorAll('.like-form');

  likeForms.forEach(form => {
    const button = form.querySelector('.like-btn');
    const reviewId = form.dataset.reviewId;
    const csrfToken = button.dataset.csrf;

    button.addEventListener('click', () => {
      fetch(`/community/like/${reviewId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json'
        }
      })
      .then(res => res.json())
      .then(data => {
        if (data.error) return;

        // Update button style
        if (data.liked) {
          button.classList.add('liked');
          button.querySelector('i').classList.replace('fa-regular', 'fa-solid');
          button.querySelector('.like-text').textContent = 'Liked';
        } else {
          button.classList.remove('liked');
          button.querySelector('i').classList.replace('fa-solid', 'fa-regular');
          button.querySelector('.like-text').textContent = 'Like';
        }

        // Update count
        button.querySelector('.like-count').textContent = data.like_count;
      })
      .catch(err => console.error(err));
    });
  });
});


// REVIEW VISUAL FEEDBACK
  // Remove messages after a while
  setTimeout(() => {
    const messages = document.querySelectorAll('.messages .alert');
    messages.forEach(msg => {
      msg.style.transition = 'opacity 0.5s, transform 0.5s';
      msg.style.opacity = '0';
      msg.style.transform = 'translateY(-10px)';
      setTimeout(() => msg.remove(), 500);
    });
  }, 3000); // Can adjust accordingly
  

// Override injected styles for error message
document.addEventListener('DOMContentLoaded', function () {
  // Find all message nodes that are error alerts
  const errorAlerts = document.querySelectorAll('.alert.error');

  errorAlerts.forEach(el => {
    // Force white text inline with !important 
    el.style.setProperty('color', 'white', 'important');

    // Set background inline too 
    el.style.setProperty('background-color', '#e53935', 'important');

    // Ensure children inherit color
    el.querySelectorAll('*').forEach(child => {
      child.style.setProperty('color', 'white', 'important');
    });
  });
});


// Watchlist AJAX Toggle
// Handles adding/removing movies from the user's watchlist without reloading the page.

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

const csrftoken = getCookie("csrftoken");

// Add click event to all watchlist buttons
document.querySelectorAll(".watchlist-btn").forEach(button => {
    button.addEventListener("click", async (e) => {
        e.preventDefault(); // Prevent full page reload

        const url = button.getAttribute("href");

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept": "application/json",
                },
            });

            if (!response.ok) throw new Error("Network response was not OK");

            const data = await response.json();

            // Show instant feedback message
            const messageBox = document.createElement("div");
            messageBox.textContent = data.message;
            messageBox.classList.add("alert");

            // Style differently depending on status
            if (data.status === "added") {
                messageBox.classList.add("alert-success");
            } else if (data.status === "removed") {
                messageBox.classList.add("alert-warning");
            } else {
                messageBox.classList.add("alert-info");
            }

            document.body.prepend(messageBox);

            setTimeout(() => messageBox.remove(), 3000);

            // Toggle button text
            button.textContent =
                data.status === "added" ? "Remove from Watchlist" : "Add to Watchlist";

        } catch (error) {
            console.error("Error toggling watchlist:", error);
        }
    });
});