function showForm(id)
{
    let form = document.getElementById(id);
    if(form.style.display != "flex")
    {
        form.style.display = "flex";
    }
    else
    {
        form.style.display = "none";
    }

    
}