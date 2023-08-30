/** Functionality for nav menu bar */
function dropdownbar()
{
    let drop = document.getElementById("dropdownbox");


    if(drop.style.display === 'flex')
    {
        drop.style.display = 'none';
    }
    else
    {
        drop.style.display = 'flex';
    }
    
}

/** Functionality for the feedback form button */
function feedbackform()
{
    let form = document.getElementById("feedbackbox");

    if(form.style.display === 'flex')
    {
        form.style.display = 'none';
        form.style.zIndex = -100;

        /**
         * Below section clears the input box if it is closed out
         */
        let feedback = document.getElementById("feedbackform").elements;

        for(let i = 0; i < feedback.length-1; i++)
        {
            feedback[i].value = ''
        }
    }
    else
    {
        form.style.display = 'flex';
        form.style.zIndex = 101;
    }
    
}