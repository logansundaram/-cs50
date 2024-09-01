function apply(event){
    let button = event.target;
    name = button.id;
    let html = `Congrats! You got into ${name}!`;
    button.parentElement.querySelector('.apply').innerHTML = html;

}
