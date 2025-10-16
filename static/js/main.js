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
  }, 2000); // Can adjust accordingly
  

// Override injected styles for error message
document.addEventListener('DOMContentLoaded', function () {
  // Find all message nodes that are error alerts
  const errorAlerts = document.querySelectorAll('.messages .alert.error');

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