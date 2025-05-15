// Fungsi untuk menampilkan loading indicator
function showLoading() {
  const button = document.querySelector('button[type="submit"]');
  if (button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Loading...';
    button.disabled = true;

    // Simpan teks asli untuk digunakan nanti
    button.dataset.originalText = originalText;
  }
}

// Fungsi untuk menyembunyikan loading indicator
function hideLoading() {
  const button = document.querySelector('button[type="submit"]');
  if (button && button.dataset.originalText) {
    button.innerHTML = button.dataset.originalText;
    button.disabled = false;
  }
}

// Fungsi untuk validasi input
function validateInput(input, pattern, errorMessage) {
  const value = input.value;
  const isValid = pattern.test(value);

  const errorElement = input.parentElement.querySelector(".error-message");
  if (!isValid) {
    if (!errorElement) {
      const newError = document.createElement("p");
      newError.className = "error-message text-red-500 text-xs mt-1";
      newError.textContent = errorMessage;
      input.parentElement.appendChild(newError);
    }
    input.classList.add("border-red-500");
    return false;
  } else {
    if (errorElement) {
      errorElement.remove();
    }
    input.classList.remove("border-red-500");
    return true;
  }
}

// Event listener untuk form pencarian
document.addEventListener("DOMContentLoaded", function () {
  const searchForm = document.querySelector('form[action*="dashboard"]');
  if (searchForm) {
    searchForm.addEventListener("submit", function (e) {
      const cityInput = document.getElementById("city");
      if (!cityInput.value.trim()) {
        e.preventDefault();
        alert("Silakan masukkan nama kota!");
        return;
      }

      showLoading();
    });
  }

  // Event listener untuk form login
  const loginForm = document.querySelector('form[action*="login"]');
  if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
      const usernameInput = document.getElementById("username");
      const passwordInput = document.getElementById("password");

      let isValid = true;

      if (!usernameInput.value.trim()) {
        isValid = false;
        validateInput(usernameInput, /.+/, "Username tidak boleh kosong");
      }

      if (!passwordInput.value.trim()) {
        isValid = false;
        validateInput(passwordInput, /.+/, "Password tidak boleh kosong");
      }

      if (!isValid) {
        e.preventDefault();
      } else {
        showLoading();
      }
    });
  }

  // Event listener untuk form registrasi
  const registerForm = document.querySelector('form[action*="register"]');
  if (registerForm) {
    registerForm.addEventListener("submit", function (e) {
      const usernameInput = document.getElementById("username");
      const passwordInput = document.getElementById("password");
      const apiKeyInput = document.getElementById("api_key");
      const termsCheckbox = document.getElementById("terms");

      let isValid = true;

      // Validasi username (minimal 3 karakter)
      if (
        !validateInput(
          usernameInput,
          /.{3,}/,
          "Username harus minimal 3 karakter"
        )
      ) {
        isValid = false;
      }

      // Validasi password (minimal 8 karakter)
      if (
        !validateInput(
          passwordInput,
          /.{8,}/,
          "Password harus minimal 8 karakter"
        )
      ) {
        isValid = false;
      }

      // Validasi API key (minimal 32 karakter)
      if (!validateInput(apiKeyInput, /.{32,}/, "API key tidak valid")) {
        isValid = false;
      }

      // Validasi terms
      if (!termsCheckbox.checked) {
        isValid = false;
        alert("Anda harus menyetujui Syarat dan Ketentuan");
      }

      if (!isValid) {
        e.preventDefault();
      } else {
        showLoading();
      }
    });
  }

  // Tambahkan animasi fade-in untuk kartu cuaca
  const weatherCard = document.querySelector(".weather-card");
  if (weatherCard) {
    weatherCard.classList.add("opacity-0");

    setTimeout(() => {
      weatherCard.classList.add("transition-opacity", "duration-500");
      weatherCard.classList.remove("opacity-0");
    }, 100);
  }

  // Auto-hide untuk flash messages
  const flashMessages = document.querySelectorAll('[role="alert"]');
  flashMessages.forEach((message) => {
    setTimeout(() => {
      message.style.transition = "opacity 1s ease-out";
      message.style.opacity = "0";

      setTimeout(() => {
        message.remove();
      }, 1000);
    }, 5000);
  });
});
