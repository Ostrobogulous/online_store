function submitSortForm() {
    document.getElementById('sortForm').submit();
}

function submitCurrencyForm(){
  document.getElementById('currencyForm').submit();
}

function showConfirmation() {
  var name = document.getElementById('name').value;
  var category = document.getElementById('category').value;
  var brand = document.getElementById('brand').value;
  var description = document.getElementById('description').value;
  var quantity = document.getElementById('quantity').value;
  var price = document.getElementById('price').value;
  var confirmationMessage = "Confirm entered info:\n\n";
  confirmationMessage += "Name: " + name + "\n";
  confirmationMessage += "Category: " + category + "\n";
  confirmationMessage += "Brand: " + brand + "\n";
  confirmationMessage += "Description: " + description + "\n";
  confirmationMessage += "Quantity: " + quantity + "\n";
  confirmationMessage += "Price: " + price + "\n";
  return confirm(confirmationMessage);
}

function showReviewConfirmation() {
  var rating = document.getElementById('rating').value;
  var content = document.getElementById('content').value;
  var confirmationMessage = "Confirm your review:\n\n";
  confirmationMessage += "Rating: " + rating + "\n";
  confirmationMessage += "Content: " + content + "\n";
  return confirm(confirmationMessage);
}

function setupReviews() {
  const openReviewsButton = document.querySelector('.open-reviews-button');
  const reviewsOverlay = document.querySelector('.reviews-overlay');
  const closeReviewsButton = document.querySelector('.close-reviews-button');
  openReviewsButton.addEventListener('click', () => {
    reviewsOverlay.style.display = 'block';
  });
  closeReviewsButton.addEventListener('click', () => {
    reviewsOverlay.style.display = 'none';
  });
}

function setupAddReview() {
  const openAddReviewButton = document.querySelector('.open-add-review-button');
  const addReviewOverlay = document.querySelector('.add-review-overlay');
  const closeAddReviewButton = document.querySelector('.close-add-review-button');
  openAddReviewButton.addEventListener('click', () => {
  addReviewOverlay.style.display = 'block';
  });
  closeAddReviewButton.addEventListener('click', () => {
  addReviewOverlay.style.display = 'none';
  });
}