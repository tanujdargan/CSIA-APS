// Initialize Firebase
var firebaseConfig = {
    apiKey: "AIzaSyBzAOFDCn0D4CJCMqfwwQrnuTltMKZowDw",
    authDomain: "csia-5825d.firebaseapp.com",
    databaseURL: "https://csia-5825d-default-rtdb.asia-southeast1.firebasedatabase.app/",
    projectId: "csia-5825d",
    storageBucket: "csia-5825d.appspot.com",
    messagingSenderId: "144604127326",
    appId: "1:144604127326:web:d63d822a8327f708e154cf",
    measurementId: "G-ENG9V1LE8C"
  };
  
  firebase.initializeApp(firebaseConfig);
  
  // Add logout button event listener
  window.onload = function() {
    document.getElementById("logout-button").addEventListener("click", function() {
      firebase.auth().signOut();
    });
  };
  
  // Listen for user authentication state changes
  firebase.auth().onAuthStateChanged(function(user) {
    if (!user) {
      // User is signed out, redirect to login page
      window.location.replace("./home.html");
    }
  });
  