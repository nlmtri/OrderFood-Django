const modalBtns = [...document.querySelectorAll('.dish-modal')];
const overlayElem = document.querySelector('.overlay');
const modalElem = document.querySelector('.modal');
const modalBody = document.getElementById('modal-body');
const modalTitle = document.getElementById('modal-title')

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
        let dish = data.bundle.dish;
        modalTitle.innerHTML = `${dish.name}`;
        const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
        modalBody.innerHTML = `
            <form id="add-to-cart-form" action="/add-to-cart/" method="post">
                <div class="d-flex" style="width: max-content;gap: 1.5rem;">
                    <img src="${dish.url}" style="width: 150px;height: 150px;object-fit: cover;object-position: center;border-radius: 6px;" alt="${dish.name}">
                    <div class="card-body">
                        <h5 class="modal-title text-wrap" id="modal-title">${dish.name}</h5>
                        <p class="card-text">${dish.price} đ</p>
                        <p class="card-text">${dish.description}</p>
                        <div>
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <input type="hidden" name="dish_id" value="${dataPk}">
                            <input type="number" name="qty" class="form-control qty-input" value="1" min="1" max="100" step="1" />
                        </div>
                    </div>
                </div>
                <div class="mb-3 mt-2">
                    <label for="note" class="form-label">Ghi chú</label>
                    <textarea name="note" style="resize: none;" class="form-control" id="note" rows="3"></textarea>
                </div>
                <button type="submit" class="btn btn-success">Thêm vào giỏ</button>
        `;
        
        const form = document.getElementById('add-to-cart-form');
        const qtyInput = form.querySelector('.qty-input');
        qtyInput.addEventListener('change', () => {
            const qty = qtyInput.value;
            // Optionally update some dynamic elements or data attributes if needed
        });
    })    
    .catch(error => console.error(error));

}));