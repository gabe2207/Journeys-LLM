Sistema de Processamento de Mensagens com LLM e Adapter
Este projeto implementa um sistema modular para processar mensagens de usuários utilizando Modelos de Linguagem Natural (LLM). Ele utiliza o padrão Adapter Design Pattern para garantir flexibilidade na escolha e integração de diferentes modelos, permitindo trocar entre um modelo local ou outros tipos de backends com alterações mínimas no restante do código.

Principais Componentes
1. Adapter Design Pattern
Interface Base (LLMAdapter):

Define um método genérico generate_response que deve ser implementado por qualquer modelo, garantindo uma interface consistente.
Isso assegura que o restante do código não precise se preocupar com os detalhes específicos de como o modelo é inicializado ou processado.
Adapter para Modelo Local (LocalLLMAdapter):

Implementa a interface LLMAdapter.
Usa o framework Hugging Face Transformers para carregar e interagir com um modelo local como EleutherAI/gpt-neo-1.3B.
Fornece a funcionalidade de gerar respostas baseadas em prompts fornecidos pelo sistema.
Função de Inicialização (get_llm_adapter):

Centraliza a lógica para selecionar e configurar o adapter correto.
Atualmente suporta apenas modelos locais, mas pode ser estendido facilmente para suportar modelos online ou outros adaptadores.
2. Fluxo de Processamento
O sistema processa mensagens de usuários através de um pipeline dividido em etapas claras:

Jornada 1: Verificação por Regras Simples:

Verifica se a mensagem se enquadra em categorias predefinidas, como "Resposta Negativa Direta" ou "Oferta Muito Baixa".
As mensagens identificadas são processadas diretamente, sem passar por classificação ou modelos LLM.
Jornada 2: Classificação com Machine Learning:

Para mensagens que não se encaixam nas regras simples, utiliza um pipeline de Machine Learning (TF-IDF + Decision Tree) para categorizá-las.
As categorias possíveis são:
"Resposta Negativa Direta"
"Oferta Muito Baixa"
"Encaminhar para LLM"
Jornada 3: Processamento pelo LLM:

Mensagens categorizadas como "Encaminhar para LLM" são enviadas ao modelo configurado pelo adapter.
Um prompt específico é usado para fornecer contexto e gerar respostas adequadas.
3. Dispatch Table
O código utiliza uma dispatch table para mapear categorias de mensagens às funções de processamento correspondentes.
Isso elimina a necessidade de múltiplos if ou elif, tornando o código mais modular e fácil de expandir.
Flexibilidade do Adapter
O uso do adapter permite:

Troca Fácil de Modelos:

Se você quiser usar um modelo diferente, basta criar um novo adapter que implemente LLMAdapter e alterar a configuração em get_llm_adapter.
O restante do código não precisa ser modificado.
Suporte a Múltiplos Backends:

Você pode adicionar suporte para um modelo online ou um modelo local diferente apenas criando uma nova classe adapter e adicionando a lógica correspondente em get_llm_adapter.
Manutenção Simplificada:

Caso precise alterar a forma como os prompts são processados ou otimizados para um modelo específico, as mudanças ficam isoladas dentro do adapter.

Exemplos Práticos de Uso
Exemplo 1: Configuração do Adapter
Você pode configurar o sistema para usar um modelo local:

llm_adapter = get_llm_adapter(adapter_type="local", model_name="EleutherAI/gpt-neo-1.3B")
No futuro, se quiser trocar para um modelo online (como OpenAI GPT ou Groq), basta implementar um OnlineLLMAdapter e configurar
llm_adapter = get_llm_adapter(adapter_type="online", api_key="sua-chave-api")


Exemplo 2: Processamento de Mensagens
Entrada:
Mensagens fornecidas pelos usuários:
mensagens_teste = [
    "Pago R$30 pelo produto",
    "Quais os bônus do curso?",
    "Não quero comprar, obrigado",
    "O curso tem garantia?",
    "Quanto custa o curso?",
    "Estou interessado no curso, como funciona?"
]
Saída:
O sistema processa cada mensagem e retorna respostas apropriadas:
Usuário 1 - Mensagem: Pago R$30 pelo produto
Categoria: Oferta Muito Baixa
Resposta: Infelizmente, não podemos aceitar esse valor. Estamos oferecendo o melhor preço possível.

Usuário 2 - Mensagem: Quais os bônus do curso?
Categoria: Encaminhar para LLM
Resposta: O curso inclui acesso ao grupo exclusivo no WhatsApp e material complementar em PDF.

Usuário 3 - Mensagem: Não quero comprar, obrigado
Categoria: Resposta Negativa Direta
Resposta: Entendido! Caso mude de ideia, estaremos aqui.

Usuário 4 - Mensagem: O curso tem garantia?
Categoria: Encaminhar para LLM
Resposta: Sim, o curso possui uma garantia de 7 dias.

Usuário 5 - Mensagem: Quanto custa o curso?
Categoria: Encaminhar para LLM
Resposta: O preço do curso é R$199,00.

Usuário 6 - Mensagem: Estou interessado no curso, como funciona?
Categoria: Encaminhar para LLM
Resposta: Este é um curso completo para iniciantes aprenderem programação com Python.

Cenários de Teste
Cenário 1: Testar Fluxo Completo
Configure o adapter para o modelo local e processe mensagens de teste.
Valide que as mensagens são classificadas corretamente e que as respostas são coerentes.
Cenário 2: Trocar para Outro Modelo
Adicione um novo adapter (como OnlineLLMAdapter) e configure o sistema para usá-lo.
Teste se o modelo online é usado corretamente sem alterações no código principal.
Cenário 3: Regras Simples e Classificação
Teste mensagens que se enquadram nas categorias de regras simples, como:
"Não quero comprar" (Resposta Negativa Direta).
"Pago R$10" (Oferta Muito Baixa).
Valide que essas mensagens são processadas sem passar pelo LLM.


Conclusão
A implementação com o adapter oferece:

Flexibilidade para trocar entre modelos sem alterar a lógica principal.
Modularidade para adicionar novos backends facilmente.
Eficiência ao processar mensagens usando regras simples ou modelos de classificação antes de acionar o LLM.
