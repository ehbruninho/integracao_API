1° Passo - Cadastrar usuários com suas respectivas entidades
2° Passo - Atribuir permissão de admin para esse usuario
3° Passo - Gerar uma API_Token para cada usuário cadastrado
4° Passo - Exportar banco de dados com todos usuários cadastrados (Atualizar banco)
 

Vamos lá:

Primeiramente descobri que para conseguir verificar todos chamados, preciso de um usuário vinculado na entidade que preciso consultar (Somente nela). Após preciso gerar um API_Token desse usuário. 

Depois de cadastrar todos clientes vinculados as suas respectivas entidades, precisamos ir para o código. 

No código em python que criei eu faço uma primeira função (valida CNPJ) onde o cliente digita o CNPJ, ele valida para verificar se existe, exibe uma mensagem dizendo que encontrou e me informa qual id da entidade. 

Após é efetuada outra validação, pegando esse id da validação anterior (valida CNPJ) e usando como argumento na função criada para identificar (consulta token) se existe um usuário com api_token ativa nessa entidade. Caso exista, o cliente escolhe se quer chamar função de consultar os tickets ou incluir um novo ticket. 

Tanto a função incluir ticket quanto a função consultar ticket estão recebendo como argumento o api_token passado por parâmetro da consulta encontrar_token)

