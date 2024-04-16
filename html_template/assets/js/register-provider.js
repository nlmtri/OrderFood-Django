const multiStepForm = document.querySelector("[data-multi-step]");  // query đến form 
const formSteps = [...multiStepForm.querySelectorAll("[data-step]")];
let currentStep = formSteps.findIndex(step => {
    return step.classList.contains('active');
});

// find() áp dụng trong array
// ?. là optional chaining: kiểm tra nulllist (một thuộc tính hoặc phương thức có tồn tại trong đối tượng hay không?)
// dataset.step để lấy giá trị của data-step

if (currentStep < 0) {
    currentStep = 0;
    showCurrentStep();
    // formSteps[currentStep].classList.add('active');
}

// console.log(currentStep);

multiStepForm.addEventListener('click', (e) => {
    let incrementor;
    if (e.target.matches("[data-next]")) {
        // currentStep += 1;
        incrementor = 1;
    } else if (e.target.matches("[data-previous]")) {
        // currentStep -= 1;
        incrementor = -1;
    }

    if (incrementor == null) return;

    const inputs = [...formSteps[currentStep].querySelectorAll("input")];

    const allValid = inputs.every(input => input.reportValidity());  // output trả về true hoặc false
    console.log(allValid);
    if (allValid) {
        currentStep += incrementor;
        showCurrentStep();
    }

    // console.log(currentStep);
});

formSteps.forEach(step => {
    step.addEventListener("animationend", e => {
        formSteps[currentStep].classList.remove("hide");
        e.target.classList.toggle("hide", !e.target.classList.contains("active"));
    });
});

function showCurrentStep() {
    formSteps.forEach((step, index) => {
        step.classList.toggle("active", index === currentStep);
    });
}

// 20:33
