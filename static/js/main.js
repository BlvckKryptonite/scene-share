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