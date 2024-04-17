const modalBtns = [...document.querySelectorAll('.dish-modal')];
const overlayElem = document.querySelector('.overlay');
const modalElem = document.querySelector('.modal');
const modalBody = document.getElementById('modal-body');
const modalTitle = document.getElementById('modal-title')
const submitModalBtn = document.getElementById('submit-modal');

overlayElem.addEventListener('click', () => {
    overlayElem.style.display = 'none';
    modalElem.classList.remove('show-modal');
});

modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', () => {
    const closeModalBtn = document.querySelector('.btn-close');

    overlayElem.style.display = 'block';
    modalElem.classList.add('show-modal');

    closeModalBtn.addEventListener('click', () => {
        overlayElem.style.display = 'none';
        modalElem.classList.remove('show-modal');
    });

    const dataPk = modalBtn.getAttribute('data-pk');
    // console.log(dataPk);
    fetch(`/dishes/${dataPk}/`)
    .then(response => {
        return response.json();
    })
    .then(data => {
        // console.log(data.bundle);
        let dish = data.bundle.dish;
        // console.log(dish);
        modalTitle.innerHTML = `${dish.name}`;
        modalBody.innerHTML = `
        <div class="d-flex" style="width: max-content;gap: 1.5rem;">
            <img src="${dish.url}" style="width: 150px;height: 150px;object-fit: cover;object-position: center;border-radius: 6px;" alt="${dish.name}">
            <div class="card-body">
                <h5 class="card-title">${dish.name}</h5>
                <p class="card-text">${dish.price} đ</p>
                <div>
                    <input type="number" class="form-control" min="1" max="100" step="1" />
                </div>
            </div>
        </div>
        <div class="mb-3 mt-2">
            <label for="exampleFormControlTextarea1" class="form-label">Ghi chú</label>
            <textarea style="resize: none;" class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
        </div>
        `; // price ở trên có thể fix lấy từ button với data attribute
        submitModalBtn.innerHTML = `Thêm +${dish.price} đ`
    })
    .catch(error => console.error(error));

}));