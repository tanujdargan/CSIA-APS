// Initialize Firebase
firebase.initializeApp({
    apiKey: "AIzaSyBzAOFDCn0D4CJCMqfwwQrnuTltMKZowDw",
    authDomain: "csia-5825d.firebaseapp.com",
    databaseURL: "https://csia-5825d-default-rtdb.asia-southeast1.firebasedatabase.app/",
    projectId: "csia-5825d",
    storageBucket: "csia-5825d.appspot.com",
    messagingSenderId: "144604127326",
    appId: "1:144604127326:web:d63d822a8327f708e154cf",
    measurementId: "G-ENG9V1LE8C"
});

window.onload = function() {
// check if the user is logged in or not
firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    // show logout form and hide login form
    document.getElementById("login-form").style.display = "none";
    document.getElementById("logout-form").style.display = "block";
    document.getElementById("user-email").innerHTML = "Logged in as " + user.email;
  } else {
    // show login form and hide logout form
    document.getElementById("login-form").style.display = "block";
    document.getElementById("logout-form").style.display = "none";
  }
});
}

// Login functionality 
window.onload = function() {
document.getElementById("login-button").addEventListener("click", function() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  firebase.auth().signInWithEmailAndPassword(email, password)
    .then(function() {
      // hide error message
      document.getElementById("error-message").style.display = "none";
    })
    .catch(function(error) {
      // handle login error
      document.getElementById("error-message").innerHTML = error.message;
      document.getElementById("error-message").style.display = "block";
    });
});
}
window.onload = function() {
// Sign up functionality
document.getElementById("signup-button").addEventListener("click", function() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  firebase.auth().createUserWithEmailAndPassword(email, password)
    .then(function() {
      // hide error message
      document.getElementById("error-message").style.display = "none";
    })
    .catch(function(error) {
      // handle sign-up error
      document.getElementById("error-message").innerHTML = error.message;
      document.getElementById("error-message").style.display = "block";
    });
});
}