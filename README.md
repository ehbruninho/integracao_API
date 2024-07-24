
# API INTEGRAÇÃO MEGAZAP + GLPI

Repositório para armazenar codigo desenvolvido para resolver problemas de integração que tivemos durante a implementação.

## 📚 Documentação API
- [Documentação API](http://54.207.73.132/glpi)




## ⚙️Configurações necessárias
| Ação | Descrição | Status |
|------|-----------| ------ |
|1° Passo | Cadastrar usuários com suas respectivas entidades | Feito |
| 2° Passo | Atribuir permissão de admin para esse usuario | Feito |
|3° Passo | Gerar uma API_Token para cada usuário cadastrado | Feito |
|4° Passo | Exportar banco de dados com todos usuários cadastrados (Atualizar banco)| Em Andamento |

## 💻 Explicação sobre o codigo

Primeiramente, descobri que para conseguir verificar todos os chamados, é necessário ter um usuário vinculado exclusivamente à entidade que se deseja consultar. Em seguida, é preciso gerar um API_Token para esse usuário.

Depois de cadastrar todos os clientes vinculados às suas respectivas entidades, passamos para o código.

No código Python que criei, há uma primeira função chamada valida_CNPJ. Nela, o cliente digita o CNPJ, o qual é validado para verificar se existe no banco de dados. Se o CNPJ for encontrado, uma mensagem é exibida informando que ele foi encontrado e indicando o ID da entidade associada.

A seguir, é feita uma outra validação, utilizando o ID obtido na validação anterior (valida_CNPJ) como argumento para uma função criada para identificar (consulta_token) se existe um usuário com um API_Token ativo nessa entidade. Caso exista, o cliente pode escolher entre consultar os tickets ou incluir um novo ticket.

Tanto a função de inclusão de ticket quanto a função de consulta de tickets recebem como argumento o API_Token passado pela função consulta_token.

