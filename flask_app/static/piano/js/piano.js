const sound = {65:"http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
                87:"http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
                83:"http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
                69:"http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
                68:"http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
                70:"http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
                84:"http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
                71:"http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
                89:"http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
                72:"http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
                85:"http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
                74:"http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
                75:"http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
                79:"http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
                76:"http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
                80:"http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
                186:"http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"};

keys = document.getElementById("keybox");
keys.addEventListener('mouseover', revkeys);
document.addEventListener('keydown', playpiano);


function revkeys()
{
    /*
    Reveals keys upon a mouseover event
    */

    let keytext = keys.getElementsByTagName('p');

    for(const text of keytext)
    {
        text.style.opacity = 1;
        
    }

    setTimeout(() => {
        for(const text of keytext)
        {
            text.style.opacity = 0;
        }
      }, 1000);
     false;
    
}

let monstercheck = '';       //Keeps track of the string for key presses to check if the monster should appear
let monsterappear = false;   //True if the monster appears
let logkeys = false;         //Should the program be keeping track of key presses?


function playpiano(key)
{
    /*
    Plays piano according to the keycode of the key press while changing the color of pressed keys.
    Will start the "scary" function if "weseeyou" is entered. 
    */
    if(!monsterappear)
    {
        let a;
        if(key.code === "KeyA")
        {
            logkeys = false;
            monstercheck = '';
            a = new Audio(sound[65]);
            document.getElementById("white1").style.backgroundColor = "gray";
            setTimeout(() => {
                document.getElementById("white1").style.backgroundColor = "white";
            }, 200);
            false;
        }
        if(key.code === "KeyW")
        {
            logkeys = true;              //Always start logging keys if there is a W press
            a = new Audio(sound[87]);
            document.getElementById("black1").style.backgroundColor = "#5e5e5e";
            setTimeout(() => {
                document.getElementById("black1").style.backgroundColor = "black";
            }, 200);
            false;
        }
        if(key.code === "KeyS")
        {
            if(monstercheck != "KeyWKeyE")  // Checking to make sure key presses are on the right track
            {
                logkeys = false;
                monstercheck = '';
            }
            a = new Audio(sound[83]);
            document.getElementById("white2").style.backgroundColor = "gray";
            setTimeout(() => {
                document.getElementById("white2").style.backgroundColor = "white";
            }, 200);
            false;
        }
        if(key.code === "KeyE")
        {
            if(monstercheck != "KeyW" && monstercheck != "KeyWKeyEKeyS" && monstercheck != "KeyWKeyEKeySKeyE")  // Checking to make sure key presses are on the right track
            {
                logkeys = false;
                monstercheck = '';
            }
            a = new Audio(sound[69]);
            document.getElementById("black2").style.backgroundColor = "#5e5e5e";
            setTimeout(() => {
                document.getElementById("black2").style.backgroundColor = "black";
            }, 200);
            false;
        }
        if(key.code === "KeyD")
        {
            logkeys = false;
            monstercheck = '';
            a = new Audio(sound[68]);
            document.getElementById("white3").style.backgroundColor = "gray";
            setTimeout(() => {
                document.getElementById("white3").style.backgroundColor = "white";
            }, 200);
            false;
        }
        if(key.code === "KeyF")
        {
            logkeys = false;
            monstercheck = '';
            a = new Audio(sound[70]);
            document.getElementById("white4").style.backgroundColor = "gray";
            setTimeout(() => {
                document.getElementById("white4").style.backgroundColor = "white";
            }, 200);
            false;
        }
        if(key.code === "KeyT")
        {
            logkeys = false;
            monstercheck = '';
            a = new Audio(sound[84]);
            document.getElementById("black3").style.backgroundColor = "#5e5e5e";
            setTimeout(() => {
                document.getElementById("black3").style.backgroundColor = "black";
            }, 200);
            false;
        }
        if(key.code === "KeyG")
        {
            logkeys = false;
            monstercheck = '';
            a = new Audio(sound[71]);
            document.getElementById("white5").style.backgroundColor = "gray";
            setTimeout(() => {
                document.getElementById("white5").style.backgroundColor = "white";
            }, 200);
            false;
        }
        if(key.code === "KeyY")
        {
            if(monstercheck != "KeyWKeyEKeySKeyEKeyE")  // Checking to make sure key presses are on the right track
            {
                logkeys = false;
                monstercheck = '';
            }
            a = new Audio(sound[89]);
            document.getElementById("black4").style.backgroundColor = "#5e5e5e";
            setTimeout(() => {
                document.getElementById("black4").style.backgroundColor = "black";
            }, 200);
            false;
        }
        if(key.code === "KeyH")
        {
            logkeys = false;
            monstercheck = '';
            a = new Audio(sound[72]);
            document.getElementById("white6").style.backgroundColor = "gray";
            setTimeout(() => {
                document.getElementById("white6").style.backgroundColor = "white";
            }, 200);
            false;
        }
        if(key.code === "KeyU")
        {
            if(monstercheck != "KeyWKeyEKeySKeyEKeyEKeyYKeyO")  // Checking to make sure key presses are on the right track
            {
                logkeys = false;
                monstercheck = '';
            }
            a = new Audio(sound[85]);
            document.getElementById("black5").style.backgroundColor = "#5e5e5e";
            setTimeout(() => {
                document.getElementById("black5").style.backgroundColor = "black";
            }, 200);
            false;
        }
        if(key.code === "KeyJ")
        {
            logkeys = false;
            monstercheck = '';
            a = new Audio(sound[74]);
            document.getElementById("white7").style.backgroundColor = "gray";
            setTimeout(() => {
                document.getElementById("white7").style.backgroundColor = "white";
            }, 200);
            false;
        }
        if(key.code === "KeyK")
        {
            logkeys = false;
            monstercheck = '';
            a = new Audio(sound[75]);
            document.getElementById("white8").style.backgroundColor = "gray";
            setTimeout(() => {
                document.getElementById("white8").style.backgroundColor = "white";
            }, 200);
            false;
        }
        if(key.code === "KeyO")
        {
            if(monstercheck != "KeyWKeyEKeySKeyEKeyEKeyY")  // Checking to make sure key presses are on the right track
            {
                logkeys = false;
                monstercheck = '';
            }
            a = new Audio(sound[79])
            document.getElementById("black6").style.backgroundColor = "#5e5e5e";
            setTimeout(() => {
                document.getElementById("black6").style.backgroundColor = "black";
            }, 200);
            false;
        }
        if(key.code === "KeyL")
        {
            logkeys = false;
            monstercheck = '';
            a = new Audio(sound[76]);
            document.getElementById("white9").style.backgroundColor = "gray";
            setTimeout(() => {
                document.getElementById("white9").style.backgroundColor = "white";
            }, 200);
            false;
        }
        if(key.code === "KeyP")
        {
            logkeys = false;
            monstercheck = '';
            a = new Audio(sound[80]);
            document.getElementById("black7").style.backgroundColor = "#5e5e5e";
            setTimeout(() => {
                document.getElementById("black7").style.backgroundColor = "black";
            }, 200);
            false;
        }
        if(key.code === "Semicolon")
        {
            logkeys = false;
            monstercheck = '';
            a = new Audio(sound[186]);
            document.getElementById("white10").style.backgroundColor = "gray";
            setTimeout(() => {
                document.getElementById("white10").style.backgroundColor = "white";
            }, 200);
            false;
        }
        a.play();

        if(logkeys)
        {
            monstercheck += key.code;
        }

        if(monstercheck === 'KeyWKeyEKeySKeyEKeyEKeyYKeyOKeyU')
        {
            scary();
        }
    }
    

}

function scary()
{
    /*
    Function for the event where the monster appears
    */
    spook = new Audio("https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1");
    spook.play();

    monsterappear = true;

    let monsterimg = document.getElementById("monsterimg");
    monsterimg.style.opacity = 1;
    monsterimg.style.zIndex = 99;
}
