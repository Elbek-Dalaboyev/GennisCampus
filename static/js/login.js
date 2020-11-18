const signInbutton = document.getElementById('signIn');
const signUpbutton = document.getElementById('signUp');
const container = document.getElementById('container');

signUpbutton.addEventListener('click', () => {
    container.classList.add('right-panel-active')
})

signInbutton.addEventListener('click', () => {
    container.classList.remove('right-panel-active')
})
