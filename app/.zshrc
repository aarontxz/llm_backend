export JAVA_HOME=$(/usr/libexec/java_home)
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi
export PATH=~/.npm-global/bin:$PATH # for Zsh

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# The next line updates PATH for the Google Cloud SDK.
if [ -f '/Users/aaron/Downloads/google-cloud-sdk/path.zsh.inc' ]; then . '/Users/aaron/Downloads/google-cloud-sdk/path.zsh.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f '/Users/aaron/Downloads/google-cloud-sdk/completion.zsh.inc' ]; then . '/Users/aaron/Downloads/google-cloud-sdk/completion.zsh.inc'; fi
export PATH="/usr/local/opt/mongodb-community/bin:$PATH"

