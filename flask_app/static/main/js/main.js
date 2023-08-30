function displayEmail()
{
    
    document.getElementById("sessionemail").innerHTML =
                                        "Welcome, " + (document.cookie).slice(6);
}