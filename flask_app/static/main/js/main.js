/** Functionality for nav menu bar */
function dropdownbarnew()
{
    let drop = document.getElementById("dropdownboxnew");


    if(drop.style.display === 'flex')
    {
        drop.style.display = 'none';
    }
    else
    {
        drop.style.display = 'flex';
    }
    
}


let current_img_index = 0;

function displaymultiimage(event)
{

    let clicked_element = this.parentNode;

    // Transparent black overlay
    let overlay = document.getElementById("imageoverlay");

    //Box for images to be put into
    let imgbox = document.getElementById("imgbox");

    // First image
    change_image(0, clicked_element);


    /*Toggle on overlay */
    overlay.style.display = "flex";



    /* DEFINING FUNCTIONS */

    // Handles previous image functionality
    function leftarrow()
    {
        change_image(-1, clicked_element);
    }

    // Handles next image functionality
    function rightarrow()
    {
        change_image(1, clicked_element);
    }

    // Handles checking if user pressed an arrow key to go to the next or previous image
    function check_arrow(event)
    {
        console.log("Keydown! Key: " + event.key)
        if(event.key === "ArrowLeft" || event.key === "a")
        {
            change_image(-1, clicked_element);
        }
        else if(event.key === "ArrowRight" || event.key === "d")
        {
            change_image(1, clicked_element);
        }
    }

    // Handles closing an overlay when the user clicks outside the box
    function close_overlay(event)
    {
        var x = event.clientX;
        var y = event.clientY;

        img_box_pos = imgbox.getBoundingClientRect();

        if(x < img_box_pos.left || x > img_box_pos.right || y < img_box_pos.top || y > img_box_pos.bottom)
        {
            destroy();
        }
    }

    // Handles destroying all event listeners and removing the overlay
    function destroy()
    {
        document.getElementById("leftarrow").removeEventListener("click", leftarrow);
        document.getElementById("rightarrow").removeEventListener("click", rightarrow);
        document.removeEventListener("keydown", check_arrow);
        document.getElementById("xbutton").removeEventListener("click", destroy);
        destroymultiimage();
    }

    /* ADDING EVENT LISTENERS */
    document.getElementById("leftarrow").addEventListener("click", leftarrow);
    document.getElementById("rightarrow").addEventListener("click", rightarrow);
    document.addEventListener("keydown", check_arrow);
    document.getElementById("xbutton").addEventListener("click", destroy);
    overlay.addEventListener("click", close_overlay);

}

/* Changes the current image of the overlay.
    inc: How many increments to image array (1 goes to next image, -1 goes to previous) 
    clicked_element: The image display the user clicked on
*/
function change_image(inc, clicked_element)
{
    console.log("Changing image! Inc: " + inc);
    jQuery.ajax({
        url: "/getimagefiles",
        type: "POST",
        data: "./mysite/flask_app/static/main/images/" + clicked_element.id + "-images/", // Python path (for pany: "./mysite/flask_app/static/main/images/")
        success: function (img_arr) 
        {
            image_array = img_arr.split(" ");

            console.log(image_array)
            
            // If going next, current index cannot be larger than image array. If going previous, current index cannot be zero.
            if((inc === 1 && current_img_index != image_array.length-1) || (inc === -1 && current_img_index != 0) || (inc === 0))
            {
                current_img_index += inc;
                document.getElementById("currentimage").src = "../../static/main/images/" + clicked_element.id + "-images/" + image_array[current_img_index];
                document.getElementById("imagecountertext").innerHTML = (current_img_index + 1) + "/" + image_array.length
            }
            console.log("IMG INDEX: " + current_img_index + " AT IMAGE: " + image_array[current_img_index])

        }
    });
}

function destroymultiimage()
{
    /* Hide display */
    overlay = document.getElementById("imageoverlay");
    if(overlay.style.display != "none")
    {
        overlay.style.display = "none";
        current_img_index = 0;
    }

}