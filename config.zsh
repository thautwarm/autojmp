autoload -U add-zsh-hook

add-zsh-hook -Uz chpwd (){
  emulate -L zsh
  ajmp update "$pwd"
}

j(){
  cd "$(ajmp complete $@)"
}
