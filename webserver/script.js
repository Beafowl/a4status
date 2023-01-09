const progressBarAngels = document.getElementsByClassName('progress-bar')[0]
const progressBarDemons = document.getElementsByClassName('progress-bar')[1]

const LOCAL = true;

// get values from the api server
const getData = async () => {

    const reqURL = LOCAL ? '../data.json' : 'http://beafowl.de/a4status'

    d = await fetch(reqURL, { mode: 'same-origin' })
    .then((response) => response.json())
    .then((data) => {

        return data;
    });
    return d;
}

// applies the new values
const updateWebpage = (dataObject) => {

    progressBarAngels.style.setProperty('--width', dataObject.angel_status);
    progressBarAngels.setAttribute('data-label', `${dataObject.angel_status}%`)

    progressBarDemons.style.setProperty('--width', dataObject.demon_status);
    progressBarDemons.setAttribute('data-label', `${dataObject.demon_status}%`)



}

// fetch new data from the api server and update webpage
const update = async () => {

    data = await getData()
    console.log(data);
    updateWebpage(data);
}

// update when webpage will be loaded
update();

// then every 29 seconds
setInterval(() => {

    // set values when the webpage will be loaded

    update();



}, 29 * 1000)