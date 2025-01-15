const popUp = document.querySelector("#pop-up");
const searchInput = document.querySelector("#search-input");

let precoUnico = 0;
document.addEventListener("click", (e) => {
    const targetEl = e.target;
    // o pai será o cartão do produto

    if (targetEl.classList.contains("add-item")) {
        const parentEl = targetEl.closest(".product-card");

        const image = parentEl.querySelector("img");
        const name = parentEl.querySelector("h3");
        const price = parentEl.querySelector(".price");
        popUp.innerHTML = "";
        precoUnico = Number(price.innerText);

        const template = `
        <div class="add-card" data-item-id="${parentEl.dataset.itemId}">
            <div class="cancel"><button><i class="bi bi-x"></i></button></div>
            <img src="${image.src}" alt="${image.alt}">
            <h3>${name.innerText}</h3>
            <p id="preco-total">R$ ${price.innerText}</p>
            <div class="qtd-item">
                <p>Quantidade</p>
                <div class="modify-qtd">
                    <button><i class="bi bi-plus"></i></button>
                    <input class="qtd" value="1" readonly></input>
                    <button><i class="bi bi-dash"></i></button>
                </div>
            </div>
            <button class="confirm-btn">Confirmar</button>
        </div>
        `
        // transformando a string template em HTML
        const parser = new DOMParser();
        const htmlTemplate = parser.parseFromString(template, "text/html");

        // adicionando ao pop-up
        const popUpContent = htmlTemplate.querySelector(".add-card");
        popUp.appendChild(popUpContent);

        popUp.showModal();
    } else if (targetEl.classList.contains("bi-plus")) {
        const parentEl = targetEl.closest(".add-card");
        let qtd = Number(parentEl.querySelector(".qtd").value);
        if (qtd < 99) qtd += 1;
        parentEl.querySelector(".qtd").value = qtd;

        const totalElement = parentEl.querySelector("#preco-total");// Converte para número
        const total = (precoUnico * qtd).toFixed(2);
        // Atualizando o preço total no pop-up
        totalElement.innerText = `R$ ${total}`;
    } else if (targetEl.classList.contains("bi-dash")) {
        const parentEl = targetEl.closest(".add-card");
        let qtd = Number(parentEl.querySelector(".qtd").value);
        if (qtd > 0) qtd -= 1;
        parentEl.querySelector(".qtd").value = qtd;

        const totalElement = parentEl.querySelector("#preco-total");// Converte para número
        const total = (precoUnico * qtd).toFixed(2);
        // Atualizando o preço total no pop-up
        totalElement.innerText = `R$ ${total}`;
    } else if (targetEl.classList.contains("bi-x")) {
        popUp.close();
    }

    else if (targetEl.classList.contains("confirm-btn")) {
        const parentEl = targetEl.closest(".add-card");
        const item_id = parentEl.dataset.itemId;
        const quantidade = Number(parentEl.querySelector(".qtd").value);

        if (!csrfToken) {
            console.error("CSRF token não encontrado!");
            return;
        }

        fetch(`/pedido/adicionar/${item_id}/${quantidade}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ item_id: item_id, quantidade: quantidade }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Erro ao adicionar o item no carrinho");
                }
                return response.json();
            })
            .then(data => {
                console.log("Item adicionado ao carrinho:", data);
                const confirmBtn = document.querySelector(".confirm-btn");
                confirmBtn.innerText = "Adicionado ao carrinho!";

                setTimeout(() => {
                    popUp.close(); // Fecha o pop-up após adicionar
                }, 1000);
            })
            .catch(error => {
                console.error("Erro ao adicionar ao carrinho:", error);
            });
    }
});

popUp.addEventListener("click", (e) => {
    const rect = popUp.getBoundingClientRect();

    if (e.clientX < rect.left || e.clientX > rect.right || e.clientY < rect.top || e.clientY > rect.bottom) popUp.close();
});

searchInput.addEventListener("keyup", (e) => {
    const search = e.target.value;
    const itens = document.querySelectorAll(".product-card");

    itens.forEach((item) => {
        let itemName = item.querySelector("h3").innerText.toLowerCase();

        const normalizedSearch = search.toLowerCase();

        item.style.display = "flex";

        if(!itemName.includes(normalizedSearch))
            item.style.display = "none";
    })
});

