const finalizeBtn = document.querySelector("#finalize-order-btn");
const addressForm = document.querySelector("#address-form");
const cepInput = document.querySelector("#cep-input");
const cancelBtn = document.querySelector("#cancel-btn");

function validDigits(text) {
    return text.replace(/[^0-9]/g, "");
    // só aceita dígitos de 0 a 9, o resto substitui por "", o g indica que é global
}

// Eventos
finalizeBtn.addEventListener("click", () => {
    addressForm.showModal();
});

addressForm.addEventListener("click", (e) => {
    const rect = addressForm.getBoundingClientRect();

    if (e.clientX < rect.left || e.clientX > rect.right || e.clientY < rect.top || e.clientY > rect.bottom) addressForm.close();
});

cepInput.addEventListener("input", (e) => {
    const updatedValue = validDigits(e.target.value);

    e.target.value = updatedValue;
});

cancelBtn.addEventListener("click", (e) => {
    e.preventDefault();

    addressForm.close();
});

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