// 1. Acesse o shell do MongoDB: mongosh

// 2. Crie um banco de dados e uma coleção:
use meu_banco_mongo;
db.createCollection("produtos");

// 3. Insira documentos:
db.produtos.insertOne({
 nome: "Smartphone X",
 marca: "TechCorp",
 especificacoes: {
 ram: "8GB",
 armazenamento: "128GB",
 cor: "Preto"
 },
 tags: ["eletronicos", "celular", "android"],
 preco: 999.99
});

db.produtos.insertOne({
 nome: "Smartwatch Y",
 marca: "WearableCo",
 especificacoes: {
 bateria: "2 dias",
 funcoes: ["monitor cardiaco", "gps"]
 },
 tags: ["eletronicos", "vestivel"],
 preco: 249.50
});

// 4. Consulte documentos:
// Encontrar todos os produtos:
db.produtos.find({});

// Encontrar produtos da marca "TechCorp":
db.produtos.find({ marca: "TechCorp" });

// Encontrar produtos com "celular" na lista de tags:
db.produtos.find({ tags: "celular" });

// Encontrar produtos com RAM de "8GB":
db.produtos.find({ "especificacoes.ram": "8GB" });
