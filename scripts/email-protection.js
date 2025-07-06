document.addEventListener("DOMContentLoaded", function () {
  const user = "karthikeyapoondla"; 
  const domain = "yahoo.com";
  const email = user + "@" + domain;
  const link = document.getElementById("email-link");
  if (link) {
    link.href = "mailto:" + email;
  }
});