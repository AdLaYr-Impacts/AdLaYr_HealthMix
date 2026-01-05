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
  document.getElementById("mainImage").src = el.src;

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