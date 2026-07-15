let currentStep = 0;

const steps = document.querySelectorAll(".step");
const progress = document.getElementById("progress");

function showStep(index){

    steps.forEach(step => step.classList.remove("active"));

    steps[index].classList.add("active");

    progress.style.width = ((index + 1) * 25) + "%";
}

function nextStep(){

    if(currentStep < steps.length-1){

        currentStep++;

        showStep(currentStep);

    }

}

function previousStep(){

    if(currentStep>0){

        currentStep--;

        showStep(currentStep);

    }

}

showStep(0);