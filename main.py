import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer

# Adapter Base
class LLMAdapter:
    def generate_response(self, prompt):
        raise NotImplementedError("Este método deve ser implementado pelos Adapters.")

# Adapter para Modelo Local
class LocalLLMAdapter(LLMAdapter):
    def __init__(self, model_name="EleutherAI/gpt-neo-1.3B"):
        print(f"Carregando o modelo local: {model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_response(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model.generate(**inputs, max_length=150, num_return_sequences=1)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

# Função para inicializar o Adapter
def get_llm_adapter(adapter_type, **kwargs):
    if adapter_type == "local":
        return LocalLLMAdapter(model_name=kwargs.get("model_name", "EleutherAI/gpt-neo-1.3B"))
    else:
        raise ValueError(f"Adapter '{adapter_type}' não suportado.")

# Prompt do sistema
SYSTEM_PROMPT = (
    "Você é um vendedor serio especializado em nossos produtos. Responda somente o que for perguntado, "
    "sem enrolar demais. Se o cliente perguntar sobre algo que nao tem na loja, simplesmente responda "
    "'Nao encontrei exatamente, pode ser mais especifico?'. Nao de informacao de nada que nao tenha a ver "
    "com a pergunta do usuario. Se o cliente perguntar de algo que nao esta nas informacoes adicionais, "
    "diga que nao tem certeza, para confirmar no site oficial."
)

# Dados Mocados para o Classificador
mensagens_mocadas = [
    "Não quero comprar", "Pago R$10", "Quanto custa?",
    "Estou interessado no curso", "É muito caro",
    "Quais os bônus do curso?", "Só pago R$50",
    "Não estou interessado", "O curso tem garantia?"
]

categorias_mocadas = [
    "Resposta Negativa Direta", "Oferta Muito Baixa", "Encaminhar para LLM",
    "Encaminhar para LLM", "Encaminhar para LLM",
    "Encaminhar para LLM", "Oferta Muito Baixa",
    "Resposta Negativa Direta", "Encaminhar para LLM"
]

# Pipeline de Classificação
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('classifier', DecisionTreeClassifier())
])
pipeline.fit(mensagens_mocadas, categorias_mocadas)

# Funções de Processamento por Categoria
def processar_resposta_negativa(mensagem):
    return "Resposta Negativa Direta", "Entendido! Caso mude de ideia, estaremos aqui."

def processar_oferta_baixa(mensagem):
    return "Oferta Muito Baixa", "Infelizmente, não podemos aceitar esse valor. Estamos oferecendo o melhor preço possível."

def processar_llm(mensagem):
    """
    Processa a mensagem pelo modelo LLM usando o Adapter.
    """
    prompt = SYSTEM_PROMPT + f"\nUsuário: {mensagem}\nResposta:"
    resposta = llm_adapter.generate_response(prompt)
    return "Encaminhar para LLM", resposta

# Dispatch Table: Mapeamento de Categorias para Funções
dispatch_table = {
    "Resposta Negativa Direta": processar_resposta_negativa,
    "Oferta Muito Baixa": processar_oferta_baixa,
    "Encaminhar para LLM": processar_llm,
}

# Função Principal de Processamento
def processar_mensagem(user_id, mensagem):
    """
    Processa a mensagem do usuário através de jornadas definidas usando dispatch table.
    """
    # Jornada 1: Verificação por regras simples
    regra_resultado = verificar_mensagem_regra(mensagem)
    if regra_resultado:
        return dispatch_table[regra_resultado](mensagem)
    
    # Jornada 2: Classificação com Machine Learning
    categoria = pipeline.predict([mensagem])[0]
    return dispatch_table[categoria](mensagem)

def verificar_mensagem_regra(mensagem):
    """
    Aplica regras simples para categorizar a mensagem sem usar ML.
    """
    palavras_negativas = ["não quero", "não compro", "não estou interessado"]
    for palavra in palavras_negativas:
        if palavra in mensagem.lower():
            return "Resposta Negativa Direta"
    
    if "pago" in mensagem.lower():
        try:
            valor = int(''.join(filter(str.isdigit, mensagem)))
            if valor < 100:  # Limite arbitrário
                return "Oferta Muito Baixa"
        except ValueError:
            pass
    return None

# Inicializar o Adapter para o Modelo Local
llm_adapter = get_llm_adapter(adapter_type="local", model_name="EleutherAI/gpt-neo-1.3B")

# Teste do Sistema
if __name__ == "__main__":
    mensagens_teste = [
        "Pago R$30 pelo produto",
        "Quais os bônus do curso?",
        "Não quero comprar, obrigado",
        "O curso tem garantia?",
        "Quanto custa o curso?",
        "Estou interessado no curso, como funciona?"
    ]

    for user_id, mensagem in enumerate(mensagens_teste, start=1):
        categoria, resposta = processar_mensagem(user_id, mensagem)
        print(f"Usuário {user_id} - Mensagem: {mensagem}")
        print(f"Categoria: {categoria}")
        print(f"Resposta: {resposta}\n")
