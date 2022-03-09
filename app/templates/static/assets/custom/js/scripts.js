// script customizado para atualizar os preços exibidos na página de detalhe
// a partir da variação selecionada

(function () {
  // obtendo o select das variações
  select_variacao = document.getElementById("select-variacoes");

  // obtendo o span com o preço
  variation_preco = document.getElementById("variation-preco");

  // obtendo o span com o preço tachado
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

    // convertendo o preço para float
    preco_float = preco.replace("R$ ", "").replace(",",".");
    preco_float = Number.parseFloat(preco_float);
    
    // atribui o preço promocional baseado na variação selecionada
    preco_promocional = this.options[this.selectedIndex].getAttribute(
      "data-preco-promocional"
    );

    // convertendo o preço promocional para float
    preco_promocional_float = preco_promocional.replace("R$ ", "").replace(",",".");
    preco_promocional_float = Number.parseFloat(preco_promocional_float);

    console.log(preco_float)
    console.log(preco_promocional_float)

    

    // se o preço for maior que o preço promocional
    if (preco_float > preco_promocional_float) {

      // atualizando o span de preço
      variation_preco.innerHTML = preco;
      // atualizando o span de preço tachado
      variation_preco_promocional.innerHTML = preco_promocional;
    }
    else{

      // atualizando o span de preço
      variation_preco.innerHTML = "";
      // atualizando o span de preço
      variation_preco_promocional.innerHTML = preco;
    }
  });
})();
