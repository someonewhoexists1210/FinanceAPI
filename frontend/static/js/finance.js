
function deleteGoal(id){
    window.location.href = '/delete_goal/' + id;
}

document.addEventListener('DOMContentLoaded', function() {
    
    let currentIndex = 0;
    let models = document.querySelectorAll('.modal');

    function displayNextModel() {
        if (currentIndex < models.length) {
            models[currentIndex].style.display = 'block';
            currentIndex++;
        }
    }

    function closeModal(button) {
        button.parentElement.parentElement.style.display = 'none';
        displayNextModel();
    }
    displayNextModel();
    let closeButtons = document.getElementsByClassName('close');
    Array.from(closeButtons).forEach(function(button) {
        button.addEventListener('click', () => closeModal(button));
    });        
});
