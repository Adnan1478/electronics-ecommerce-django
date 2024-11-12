document.addEventListener('DOMContentLoaded', function() {
  // Define the maximum quantity
  const MAX_QUANTITY = 10;

  // Get all increment and decrement buttons
  const incrementButtons = document.querySelectorAll('.cartIncrement');
  const decrementButtons = document.querySelectorAll('.cartDecrement');

  incrementButtons.forEach(button => {
      button.addEventListener('click', function() {
          const quantityElement = this.nextElementSibling;
          let currentQuantity = parseInt(quantityElement.textContent);

          // Check if the current quantity is less than the maximum quantity
          if (currentQuantity < MAX_QUANTITY) {
              quantityElement.textContent = currentQuantity + 1;
          }
      });
  });

  decrementButtons.forEach(button => {
      button.addEventListener('click', function() {
          const quantityElement = this.previousElementSibling;
          let currentQuantity = parseInt(quantityElement.textContent);

          // Decrease the quantity only if it's greater than 1
          if (currentQuantity > 1) {
              quantityElement.textContent = currentQuantity - 1;
          }
      });
  });
});
  
  // Profile Dropdown Function
  document.addEventListener('DOMContentLoaded', function() {
    var profileDropdownToggle = document.getElementById('profile-dropdown-toggle');
    var profileDropdown = document.getElementById('profile-dropdown');

    // Toggle dropdown when clicking on the profile image or username
    profileDropdownToggle.addEventListener('click', function() {
        profileDropdown.classList.toggle('show');
    });

    // Close dropdown if user clicks outside of it
    document.addEventListener('click', function(event) {
        if (!profileDropdownToggle.contains(event.target) && !profileDropdown.contains(event.target)) {
            profileDropdown.classList.remove('show');
        }
    });
});

// Toast Alert
const addToCartButtons = document.querySelectorAll('.add-to-cart-button');
const notification = document.getElementById('notification');

// Add click event listeners to each button
addToCartButtons.forEach(button => {
  button.addEventListener('click', function() {
    // Show notification
    notification.classList.remove('hidden');
    notification.classList.add('show');

    // Hide notification after 3 seconds
    setTimeout(() => {
      notification.classList.remove('show');
      notification.classList.add('hidden');
    }, 3000);

    // Add your logic here to handle adding the product to the cart
  });
});

// Addtocart 
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.add-to-cart-button').forEach(button => {
    button.addEventListener('click', event => {
      const productId = event.target.closest('.cards').querySelector('.productId').value;
      fetch(`/add_to_cart/${productId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
      })
      .then(response => response.json())
      .then(data => {
        console.log('Product added to cart:', data);
        // Optional: Update cart UI or show a confirmation message
      })
      .catch(error => console.error('Error:', error));
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  // Handle Remove button click
  document.querySelectorAll('.remove-from-cart-button').forEach(button => {
    button.addEventListener('click', function () {
      const productId = this.getAttribute('data-id');
      
      fetch(`/remove-from-cart/${productId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': '{{ csrf_token }}'
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Remove the item from the DOM
          this.closest('article').remove();
        } else {
          alert('Failed to remove item from cart');
        }
      })
      .catch(error => console.error('Error:', error));
    });
  });

  // Handle Buy button click
  document.querySelectorAll('.buy-button').forEach(button => {
    button.addEventListener('click', function () {
      window.location.href = "{% url 'checkout' %}";
    });
  });
});