function definingKeyType () {
    let rad = document.getElementsByName('flexRadioDefault');
    let typeKey = document.getElementById("FormControlTypeKey");
    for (let i = 0; i < rad.length; i++) {
        if (rad[i].checked) {
            if (i === 0) {
                typeKey.removeAttribute("disabled");
                typeKey.setAttribute("disabled", "disabled");
                typeKey.value = "";
            } else {
                typeKey.removeAttribute("disabled");
                typeKey.value = "";
            }
        }
    }
}