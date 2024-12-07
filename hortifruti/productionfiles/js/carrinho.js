// Funções



// Eventos

document.addEventListener("click", (e) => {
    const targetEl = e.target;
    const parentEl = targetEl.closest(".product-card");
    // o pai será o cartão do produto
    let qtd;

    if (parentEl && parentEl.querySelector(".qtd"))
        qtd = Number(parentEl.querySelector(".qtd").value);

    if (targetEl.classList.contains("bi-plus") && qtd < 99) {
        qtd += 1;
        parentEl.querySelector(".qtd").value = qtd;
        atualizarQuantidade(parentEl.dataset.itemId, qtd);
    }

    else if (targetEl.classList.contains("bi-dash") && qtd > 0) {
        qtd -= 1;
        parentEl.querySelector(".qtd").value = qtd;
        atualizarQuantidade(parentEl.dataset.itemId, qtd);
    }

    //acho que não vai precisar
    // if(targetEl.classList.contains("remove-item")) {
    //     // remover item do BD

    // }
});

function getCSRFToken() {
    const csrfToken = document.cookie.split(';')
        .find(cookie => cookie.trim().startsWith('csrftoken='));
    return csrfToken ? csrfToken.split('=')[1] : null;
}

// Função para enviar requisição de atualização ao backend
function atualizarQuantidade(item_id, quantidade) {
    const csrfToken = getCSRFToken();  // Pega o token CSRF

    if (!csrfToken) {
        console.error("CSRF token não encontrado!");
        return;
    }

    fetch(`/pedido/carrinho/alterar/${item_id}/${quantidade}/`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken  // Inclui o CSRF token nos cabeçalhos
        },
        body: JSON.stringify({ quantidade: quantidade })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao atualizar a quantidade");
            }
            return response.json(); // ou `response.text()` se não estiver retornando JSON
        })
        .then(data => {
            window.location.reload()
            console.log("Quantidade atualizada com sucesso:", data);
        })
        .catch(error => {
            console.error("Erro ao atualizar quantidade:", error);
        });
}