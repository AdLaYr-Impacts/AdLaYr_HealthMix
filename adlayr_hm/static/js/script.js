// password eye config
function togglePassword() {
  const passwordField = document.getElementById("password");
  passwordField.type = passwordField.type === "password" ? "text" : "password";
  const icon = document.querySelector('.toggle-password');
  console.log(icon)
  if (icon.textContent.trim() === '🙈') {
    icon.textContent = '🐵';
  } else {
    icon.textContent = '🙈';
  }
}

function toggleconfirmPassword() {
  const passwordField = document.getElementById("confirm_password");
  passwordField.type = passwordField.type === "password" ? "text" : "password";
  const icon = document.querySelector('.toggle-confirm-password');
  if (icon.textContent.trim() === '🙈') {
    icon.textContent = '🐵';
  } else {
    icon.textContent = '🙈';
  }
}


// OTP verification
const otpBoxes = document.querySelectorAll(".otp-box");
const otpHidden = document.getElementById("otp");
const otpForm = document.querySelector("form");

otpBoxes.forEach((box, index) => {
  box.addEventListener("input", () => {
    box.value = box.value.replace(/[^0-9]/g, "");
    if (box.value && index < otpBoxes.length - 1) {
      otpBoxes[index + 1].focus();
    }
  });
  box.addEventListener("keydown", (e) => {
    if (e.key === "Backspace" && !box.value && index > 0) {
      otpBoxes[index - 1].focus();
    }
  });
});
otpForm.addEventListener("submit", () => {
  otpHidden.value = Array.from(otpBoxes)
    .map(input => input.value)
    .join("");
});

// Login Page
document.addEventListener("DOMContentLoaded", () => {
  const card = document.querySelector('.glass-card');
  card.style.opacity = 0;
  card.style.transform = "translateY(20px)";
  setTimeout(() => {
    card.style.transition = "all 0.8s ease";
    card.style.opacity = 1;
    card.style.transform = "translateY(0)";
  }, 200);
});

// Sign Up + OTP Verification Success Message
setTimeout(() => {
  document.querySelectorAll('.custom-toast').forEach(toast => {
    toast.remove();
  });
}, 4000);


// ********************** //
// Product Details //
// ********************* //

function changeImage(el) {
  const mainImage = document.getElementById("mainImage");

  // Fade out
  mainImage.classList.add("hide");

  setTimeout(() => {
    mainImage.src = el.src;
    mainImage.classList.remove("hide");
  }, 200);

  document.querySelectorAll(".thumb").forEach(t => {
    t.classList.remove("active");
  });

  el.classList.add("active");
}

function updateQty(value) {
  let qty = document.getElementById("qty");
  let current = parseInt(qty.value);

  if (current + value >= 1) {
    qty.value = current + value;
  }
}

// cart - x if not login
function showLoginAlert() {
  const alertBox = document.getElementById("loginAlert");
  const bubble = alertBox.querySelector(".glass-bubble");

  alertBox.style.display = "block";
  bubble.style.animation = "glassSlideIn 0.45s ease forwards";

  setTimeout(() => {
    bubble.style.animation = "glassFadeOut 0.4s ease forwards";
  }, 3500);

  setTimeout(() => {
    alertBox.style.display = "none";
  }, 4000);
}

document.addEventListener("click", function (e) {
  if (e.target.classList.contains("glass-login-btn")) {
    document.getElementById("loginAlert").style.display = "none";
  }
});


// ********************** //
// Cart Page Configurations //
// ********************* //

function changeQty(btn, delta) {
  const qtyEl = btn.parentElement.querySelector('.qty');
  let qty = parseInt(qtyEl.innerText);
  qty = Math.max(1, qty + delta);
  qtyEl.innerText = qty;
  updateTotals();
}

function updateTotals() {
  let subtotal = 0;

  document.querySelectorAll('.cart-item').forEach(item => {
    const price = parseInt(item.querySelector('.price')?.dataset.price);
    const qty = parseInt(item.querySelector('.qty').innerText);
    const total = price * qty;

    item.querySelector('.item-total').innerText = `₹${total}`;
    subtotal += total;
  });

  document.getElementById('subtotal').innerText = `₹${subtotal}`;
  document.getElementById('orderTotal').innerText = `₹${subtotal}`;
}
