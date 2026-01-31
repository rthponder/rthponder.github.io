document.addEventListener("DOMContentLoaded", function () {
  const user = "academicponder"; 
  const domain = "gmail.com";
  const email = user + "@" + domain;
  const link = document.getElementById("email-link");
  if (link) {
    link.href = "mailto:" + email;
  }
});