# Aula 03 - Estruturas de Dados + JSON
# Tema: Sets (Conjuntos)

# --- 1. Criação e Deduplicação ---
categorias = {'gato', 'cachorro', 'pássaro', 'gato'}
print("Set categorias (duplicatas removidas):", categorias)

# Deduplicar uma lista convertendo para set
tags_brutas = ['python', 'ia', 'python', 'ml', 'ia', 'python']
tags_unicas = set(tags_brutas)
print("Tags originais:", tags_brutas)
print("Tags únicas:", tags_unicas)

# Teste de pertencimento O(1)
print("python está nas tags?", 'python' in tags_unicas)
print("java está nas tags?", 'java' in tags_unicas)


# --- 2. Adição e Remoção ---
print("\n--- Adicionando e Removendo ---")
tags_unicas.add('deep-learning')
print("Após add('deep-learning'):", tags_unicas)

tags_unicas.discard('java') # Não gera erro se a chave não existir
print("Após discard('java'):", tags_unicas)

tags_unicas.remove('ml') # Remove o elemento (gera erro se não existir)
print("Após remove('ml'):", tags_unicas)


# --- 3. Operações de Conjuntos ---
print("\n--- Operações de Conjuntos ---")
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

print("Set A:", a)
print("Set B:", b)
print("União (A | B):", a | b)
print("Interseção (A & B):", a & b)
print("Diferença (A - B):", a - b)
print("Diferença simétrica (A ^ B):", a ^ b)

print("\n{1, 2} é subconjunto de A?", {1, 2}.issubset(a))
print("A é superconjunto de {1, 2}?", a.issuperset({1, 2}))
