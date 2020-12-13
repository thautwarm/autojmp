## autojmp

An autojump implementation applicable to **any shell** and **any OS** by restoring [Xython/rtpy](https://github.com/Xython/wisepy/tree/836b63c33685b6107e528256a3cc0a9600015140).

Keep things simple and portable, do not fuck your brain.

### Common Configurtions

```bash
export AUTOJMP_MAX_CACHE=999
export AUTOJMP_WORD_ANA_LEN=3 # 3-gram is precise enough!
```

### Zsh

Firstly install `autojmp`: `pip install autojmp`.

Then, append the following contents to your `~/.zshrc`:

```zsh
autoload -U add-zsh-hook

add-zsh-hook -Uz chpwd (){
  emulate -L zsh
  ajmp update "$pwd"
}

j(){
  cd "$(ajmp complete $@)"
} 
```

Using it in this way:

```zsh
➜  github j desk git
➜  github pwd
/c/Users/twshe/Desktop/github
➜  github j git
➜  github pwd
/c/Users/twshe/github
```

### Motivation

Currently I have to work on Windows and I do need `zsh`. This leads me to MSYS2.
However, `autojump` installation does not work for MSYS2.
Hence I restored my own autojump implementation made years ago. 
