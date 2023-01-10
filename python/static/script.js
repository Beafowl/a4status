const progressBarAngels = document.getElementsByClassName('progress-bar')[0]
const progressBarDemons = document.getElementsByClassName('progress-bar')[1]

const reqURL = 'http://beafowl.de/a4status';

// get values from the api server
const getData = async () => {

    d = await fetch(reqURL, { mode: 'same-origin' })
    .then((response) => response.json())
    .then((data) => {

        return data;
    });
    return d;
}

// applies the new values
const updateWebpage = (dataObject) => {

    // check if 100 percent has not been reached yet
    // if one has reached 100%, change the bar to a 'minutes left' bar that decrements

    if (dataObject.angels.percentage != 100) {

        progressBarAngels.style.setProperty('--width', dataObject.angels.percentage);
        progressBarAngels.setAttribute('data-label', `${dataObject.angels.percentage}%`)
        progressBarAngels.style.setProperty('--gradientColor1', '#af99b0')
        progressBarAngels.style.setProperty('--gradientColor2', '#bfacc0')

    } else {

        dataObject.angels.percentage = Math.floor((dataObject.angels.closes_in / 60) * 100);
        progressBarAngels.style.setProperty('--width', dataObject.angels.percentage);
        progressBarAngels.setAttribute('data-label', `Das Tor zur Raidhöhle ist offen! ${dataObject.angels.closes_in} Minuten übrig.`)
        progressBarAngels.style.setProperty('--gradientColor1', '#ff9400')
        progressBarAngels.style.setProperty('--gradientColor2', '#ffa200')
        // background-image: linear-gradient(#af99b0, #bfacc0);
    }

    if (dataObject.demons.percentage != 100) {

        progressBarDemons.style.setProperty('--width', dataObject.demons.percentage);
        progressBarDemons.setAttribute('data-label', `${dataObject.demons.percentage}%`);
        progressBarDemons.style.setProperty('--gradientColor1', '#af99b0');
        progressBarDemons.style.setProperty('--gradientColor2', '#bfacc0');
    } else {

        dataObject.demons.percentage = Math.floor((dataObject.demons.closes_in / 60) * 100);
        progressBarDemons.style.setProperty('--width', dataObject.demons.percentage);
        progressBarDemons.setAttribute('data-label', `Das Tor zur Raidhöhle ist offen! ${dataObject.demons.closes_in} Minuten übrig.`);
        progressBarDemons.style.setProperty('--gradientColor1', '#ff9400');
        progressBarDemons.style.setProperty('--gradientColor2', '#ffa200');
    }
}

// fetch new data from the api server and update webpage
const update = async () => {

    data = await getData()
    updateWebpage(data);
}

// update when webpage will be loaded
update();

// then every 29 seconds
setInterval(async () => {

    // set values when the webpage will be loaded

    await update();

}, 29 * 1000)