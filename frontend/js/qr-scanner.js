/**
 * QrScanner — componente reutilizável de leitura de QR Code / código de barras.
 *
 * Usa a biblioteca html5-qrcode (carregada via CDN na página) para ligar a
 * câmera traseira do dispositivo, ler qualquer código (QR ou de barras) e
 * devolver o texto lido através do callback `onScan`.
 *
 * Uso:
 *   const scanner = new QrScanner({
 *     readerId: 'leitor-camera',        // id do <div> onde a câmera é renderizada
 *     onScan: function (codigo) { ... }, // chamado com o texto lido
 *     onError: function (mensagem) { ... }, // chamado em erro de câmera/permissão
 *   });
 *
 *   scanner.iniciar(); // liga a câmera
 *   scanner.parar();   // desliga a câmera (também é chamado sozinho após ler um código)
 *   scanner.destruir(); // limpa tudo (chamar ao desmontar/sair da página)
 */
function QrScanner(opcoes) {
    this.readerId = opcoes.readerId;
    this.onScan = opcoes.onScan || function () {};
    this.onError = opcoes.onError || function () {};

    this.instancia = null;
    this.escaneando = false;
}

QrScanner.prototype.iniciar = function () {
    var self = this;

    if (self.escaneando) return;

    if (typeof Html5Qrcode === 'undefined') {
        self.onError('Não foi possível carregar o leitor de QR Code. Verifique sua conexão e tente novamente.');
        return;
    }

    self.instancia = new Html5Qrcode(self.readerId);

    var configuracao = { fps: 10, qrbox: { width: 250, height: 250 } };

    self.instancia.start(
        { facingMode: 'environment' },
        configuracao,
        function (textoDecodificado) {
            // Detectou um QR Code ou código de barras: para a câmera
            // automaticamente e só então avisa quem está usando o componente.
            self.parar().then(function () {
                self.onScan(textoDecodificado);
            });
        },
        function () {
            // Erro de leitura de um frame individual (nenhum código encontrado
            // naquele instante): é normal e esperado, não deve gerar alerta.
        }
    ).then(function () {
        self.escaneando = true;
    }).catch(function (erro) {
        self.escaneando = false;
        console.error('Erro ao iniciar o QrScanner:', erro);
        self.onError('Não foi possível acessar a câmera. Verifique se a permissão foi concedida e tente novamente.');
    });
};

QrScanner.prototype.parar = function () {
    var self = this;

    if (!self.instancia || !self.escaneando) {
        return Promise.resolve();
    }

    return self.instancia.stop()
        .then(function () {
            self.escaneando = false;
            return self.instancia.clear();
        })
        .catch(function (erro) {
            self.escaneando = false;
            console.error('Erro ao parar o QrScanner:', erro);
        });
};

// Limpa o componente por completo. Deve ser chamado quando a página que usa
// o scanner é desmontada/fechada, para garantir que a câmera não fique presa.
QrScanner.prototype.destruir = function () {
    return this.parar();
};
