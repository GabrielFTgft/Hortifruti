// Eventos

document.addEventListener("click", (e) => {
    const targetEl = e.target;
    const parentEl = targetEl.closest(".product-card");
    // o pai será o cartão do produto
    let qtd;

    if(parentEl && parentEl.querySelector(".qtd"))
        qtd = Number(parentEl.querySelector(".qtd").value);


    if(targetEl.classList.contains("bi-plus") && qtd < 99) {
        qtd += 1;
        parentEl.querySelector(".qtd").value = qtd;
    }

    else if(targetEl.classList.contains("bi-dash") && qtd > 0) {
        qtd -= 1;
        parentEl.querySelector(".qtd").value = qtd;
    }

    if(targetEl.classList.contains("remove-item")) {
        // remover item do BD

    }
});