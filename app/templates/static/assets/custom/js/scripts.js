// script customizado para atualizar os preços exibidos na página de detalhe
// a partir da variação selecionada

(function () {
  // obtendo o select das variações
  select_variacao = document.getElementById("select-variacoes");

  // obtendo o span com o preço
  variation_preco = document.getElementById("variation-preco");

  // obtendo o span com o preço promocional
  variation_preco_promocional = document.getElementById(
    "variation-preco-promocional"
  );

  // se o select de variação não for encontrado, encerra o script
  if (!select_variacao) {
    return;
  }

  // se o span de preço não for encontrado, encerra o script
  if (!variation_preco) {
    return;
  }

  // inserindo um listener de variação no select
  select_variacao.addEventListener("change", function () {
    // atribui o preço baseado na variação selecionada
    preco = this.options[this.selectedIndex].getAttribute("data-preco");

    // atribui o preço promocional baseado na variação selecionada
    preco_promocional = this.options[this.selectedIndex].getAttribute(
      "data-preco-promocional"
    );

    // atualizando o span de preço
    variation_preco.innerHTML = preco;

    // se o span de preço promocional existir
    if (variation_preco_promocional) {
      // atualizando o span de preço promocional
      variation_preco_promocional.innerHTML = preco_promocional;
    }
  });
})();
