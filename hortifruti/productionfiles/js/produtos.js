const popUp = document.querySelector("#pop-up");

document.addEventListener("click", (e) => {
    console.log("clique");
    const targetEl = e.target;
    // o pai será o cartão do produto

    if(targetEl.classList.contains("add-item")) {
        popUp.innerHTML = "";
        const parentEl = targetEl.closest(".product-card");

        const image = parentEl.querySelector("img");
        const name = parentEl.querySelector("h3");

        const template = `
        <div class="add-card" data-item-id="${parentEl.dataset.itemId}">
            <img src="${image.src}" alt="${image.alt}">
            <h3>${name.innerText}</h3>
            <p>R$ </p>
            <div class="qtd-item">
                <p>Quantidade</p>
                <div class="modify-qtd">
                    <button><i class="bi bi-plus"></i></button>
                    <input class="qtd" value="1" readonly></input>
                    <button><i class="bi bi-dash"></i></button>
                </div>
            </div>
            <form method="POST" action="{% url 'adicionar_ao_carrinho' item.id %}">
                {% csrf_token %}
                <button class="confirm-btn">Confirmar</button>
            </form>
        </div>
        `
        // transformando a string template em HTML
        const parser = new DOMParser();
        const htmlTemplate = parser.parseFromString(template, "text/html");

        // adicionando ao pop-up
        const popUpContent = htmlTemplate.querySelector(".add-card");
        popUp.appendChild(popUpContent);

        popUp.showModal();
    }

    else if(targetEl.classList.contains("bi-plus")) {
        const parentEl = targetEl.closest(".add-card");
        let qtd = Number(parentEl.querySelector(".qtd").value);
        if(qtd < 99)
            qtd += 1;
        parentEl.querySelector(".qtd").value = qtd;
    }

    else if(targetEl.classList.contains("bi-dash")) {
        const parentEl = targetEl.closest(".add-card");
        let qtd = Number(parentEl.querySelector(".qtd").value);
        if(qtd > 0)
            qtd -= 1;
        parentEl.querySelector(".qtd").value = qtd;
    }

})