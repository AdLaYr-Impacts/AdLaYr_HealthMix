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
document.querySelectorAll('.otp-box').forEach((box, index, boxes) => {
  box.addEventListener('input', () => {
    if (box.value.length === 1 && index < boxes.length - 1) {
      boxes[index + 1].focus();
    }
  });
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
