from gtts import gTTS

sentences = [
    'Bem-vindo ao Blind Guide, aguarde enquanto estabelecemos conexão GPS.',
    'Tudo pronto. Vamos. Siga em frente.',
    'Em dois metros, vire à esquerda.',
    'Em um metro, vire à esquerda.',
    'Prepare-se para virar à esquerda.',
    'Vire à esquerda!',
    'Em dois metros, vire à direita.',
    'Em um metro, vire à direita.',
    'Prepare-se para virar à direita.',
    'Vire à direita!',
    'Você chegou ao seu destino.',
    'Você chegou, destino está à sua esquerda.',
    'Você chegou, obrigado por contar com nosso guia!',
    'Chegamos ao fim do nosso vídeo, obrigado pela atenção!',
    'Como posso ajudar?',
    'Olhe para direita!',
    'Olhe para esquerda!',
    'Aguardando passagem de veículos.',
    'Tudo limpo, atravesse com cuidado!'
]

file_names = [
    'welcome.mp3',
    'ready.mp3',
    '2m_left.mp3',
    '1m_left.mp3',
    'prep_left.mp3',
    'left.mp3',
    '2m_right.mp3',
    '1m_right.mp3',
    'prep_right.mp3',
    'right.mp3',
    'reached.mp3',
    'reached_left.mp3',
    'reached_thanks.mp3',
    'ending_presentation.mp3',
    'help.mp3',
    'look_right.mp3',
    'look_left.mp3',
    'waiting.mp3',
    'all_clear.mp3'
]
print(f'{len(sentences)} e {len(file_names)}')
for sentence, name in zip(sentences, file_names):
    sound = gTTS(text=sentence, lang='pt-BR')
    sound.save(name)
    print(f'File {name} saved!')