      *================================================================*
       IDENTIFICATION                  DIVISION.
      *================================================================*

       PROGRAM-ID. @PGMID.
       AUTHOR.     C&C.

      *================================================================*
      *                        S O N D A   I T                         *
      *----------------------------------------------------------------*
      *    PROGRAMA....: @PGMID
      *    PROGRAMADOR.: C&C
      *    DATA........: @DATE
      *----------------------------------------------------------------*
      *    OBJETIVO....:
      *                 - LER    ARQINPPD COMPACTADO
      *
      *                 - GRAVAR ARQOUTZD ZONADO
      *                   @SINAL TRATAMENTO DE SINAL
      *
      *----------------------------------------------------------------*
      *    ARQUIVOS....:                                               *
      *                DDNAME           I/O        INCLUDE/BOOK
      *                ARQINPPD          I         @BOOKIN
      *                ARQOUTZD          O         DECLARADO NO PGM
      *----------------------------------------------------------------*
      *    BOOK'S......:                                               *
      *    @BOOKIN - BOOK DE ENTRADA
      *================================================================*

      *================================================================*
       ENVIRONMENT                     DIVISION.
      *================================================================*

      *----------------------------------------------------------------*
       CONFIGURATION                   SECTION.
      *----------------------------------------------------------------*

       SPECIAL-NAMES.
           DECIMAL-POINT               IS   COMMA.

      *----------------------------------------------------------------*
       INPUT-OUTPUT                    SECTION.
      *----------------------------------------------------------------*

       FILE-CONTROL.

           SELECT ARQINPPD ASSIGN      TO   UT-S-ARQINPPD
                      FILE STATUS      IS   WRK-FS-ARQINPPD.

           SELECT ARQOUTZD ASSIGN      TO   UT-S-ARQOUTZD
                      FILE STATUS      IS   WRK-FS-ARQOUTZD.

      *================================================================*
       DATA                            DIVISION.
      *================================================================*

      *----------------------------------------------------------------*
       FILE                            SECTION.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
      *   INPUT:   ARQUIVO DE ENTRADA - ARQINPPD
      *            ORG. SEQUENCIAL    - LRECL   = @LENGTHIN
      *----------------------------------------------------------------*
       FD  ARQINPPD
           RECORDING MODE IS F
           LABEL RECORD IS STANDARD
           BLOCK CONTAINS 0 RECORDS.

       01  FD-ARQINPPD                 PIC  X(@LENGTHIN).

      *----------------------------------------------------------------*
      *   INPUT:   ARQUIVO DE SAIDA   - ARQOUTZD
      *            ORG. SEQUENCIAL    - LRECL   = @LENGTHOUT
      *----------------------------------------------------------------*
       FD  ARQOUTZD
           RECORDING MODE IS F
           LABEL RECORD IS STANDARD
           BLOCK CONTAINS 0 RECORDS.

       01  FD-ARQOUTZD                 PIC  X(@LENGTHOUT).

      *----------------------------------------------------------------*
       WORKING-STORAGE                 SECTION.
      *----------------------------------------------------------------*

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       77  FILLER                      PIC  X(050)        VALUE
           '*** INICIO DA WORKING-STORAGE SECTION         ****'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       77  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE ACUMULADORES                       ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-ACUMULADORES.

           03 WRK-LIDOS-ARQINPPD       PIC  9(009) COMP-3  VALUE ZEROS.
           03 WRK-GRAVADOS-ARQOUTZD    PIC  9(009) COMP-3  VALUE ZEROS.
           03 WRK-DISPLAY              PIC +Z(08)9         VALUE ZEROS.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE TESTE DE FILE-STATUS               ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-FS-ARQINPPD             PIC  X(002)         VALUE SPACES.
       01  WRK-FS-ARQOUTZD             PIC  X(002)         VALUE SPACES.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE TRATAMENTO DE ERRO DE ARQUIVOS     ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-NOME-ARQUIVO            PIC  X(008)         VALUE SPACES.
       01  WRK-FILE-STATUS             PIC  X(002)         VALUE SPACES.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE ENTRADA ARQINPPD                   ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
@LVL01BKIN
       COPY @BOOKIN.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE SAIDA ARQOUTZD                     ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
@LVL01BKOUT
@BOOKOUT

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** FIM DA WORKING-STORAGE SECTION             ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

      *================================================================*
       PROCEDURE                       DIVISION.
      *================================================================*

      *----------------------------------------------------------------*
       0000-ROTINA-PRINCIPAL           SECTION.
      *----------------------------------------------------------------*

           PERFORM 1000-INICIAR.

           PERFORM 2000-VERIFICAR-VAZIO.

           PERFORM 3000-PROCESSAR UNTIL WRK-FS-ARQINPPD EQUAL '10'.

           PERFORM 9000-FINALIZAR.

      *----------------------------------------------------------------*
       0000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1000-INICIAR                    SECTION.
      *----------------------------------------------------------------*

           OPEN INPUT   ARQINPPD
                OUTPUT  ARQOUTZD.

           PERFORM 1100-TESTAR-FILE-STATUS.

      *----------------------------------------------------------------*
       1000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1100-TESTAR-FILE-STATUS         SECTION.
      *----------------------------------------------------------------*

           PERFORM 1110-TESTAR-FS-ARQINPPD .

           PERFORM 1120-TESTAR-FS-ARQOUTZD.

      *----------------------------------------------------------------*
       1100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1110-TESTAR-FS-ARQINPPD          SECTION.
      *----------------------------------------------------------------*

           IF  WRK-FS-ARQINPPD         NOT EQUAL  '00'
               MOVE 'ARQINPPD'         TO WRK-NOME-ARQUIVO
               MOVE WRK-FS-ARQINPPD    TO WRK-FILE-STATUS
               PERFORM 9100-FORMATAR-ERRO-ARQUIVO
           END-IF.

      *----------------------------------------------------------------*
       1110-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1120-TESTAR-FS-ARQOUTZD         SECTION.
      *----------------------------------------------------------------*

           IF  WRK-FS-ARQOUTZD         NOT EQUAL  '00'
               MOVE 'ARQOUTZD'         TO WRK-NOME-ARQUIVO
               MOVE WRK-FS-ARQOUTZD    TO WRK-FILE-STATUS
               PERFORM 9100-FORMATAR-ERRO-ARQUIVO
           END-IF.

      *----------------------------------------------------------------*
       1120-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2000-VERIFICAR-VAZIO            SECTION.
      *----------------------------------------------------------------*

           PERFORM 2100-LER-ARQINPPD .

           IF (WRK-LIDOS-ARQINPPD      EQUAL     ZEROS)
               DISPLAY '************ @PGMID ************'
               DISPLAY '*                                *'
               DISPLAY '*     ARQUIVO ARQINPPD VAZIO     *'
               DISPLAY '*       PROGRAMA ENCERRADO       *'
               DISPLAY '*                                *'
               DISPLAY '************ @PGMID ************'
               MOVE 'ARQINPPD'         TO WRK-NOME-ARQUIVO
               MOVE WRK-FS-ARQINPPD    TO WRK-FILE-STATUS
               PERFORM 9000-FINALIZAR
           END-IF.

      *----------------------------------------------------------------*
       2000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2100-LER-ARQINPPD               SECTION.
      *----------------------------------------------------------------*

           READ ARQINPPD               INTO @REGIN.

           IF WRK-FS-ARQINPPD          EQUAL     '10'
               GO TO 2100-99-FIM
           END-IF.

           PERFORM 1110-TESTAR-FS-ARQINPPD.
           ADD  1  TO   WRK-LIDOS-ARQINPPD.

      *----------------------------------------------------------------*
       2100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       3000-PROCESSAR                  SECTION.
      *----------------------------------------------------------------*

           PERFORM 3100-FORMATAR-ARQOUTZD.
           PERFORM 3200-GRAVAR-ARQOUTZD.
           PERFORM 2100-LER-ARQINPPD.

      *----------------------------------------------------------------*
       3000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       3100-FORMATAR-ARQOUTZD          SECTION.
      *----------------------------------------------------------------*

           INITIALIZE @REGOUT
            REPLACING ALPHANUMERIC DATA BY SPACES
             NUMERIC DATA BY ZEROS.

@FORMATOUT
           .
      *----------------------------------------------------------------*
       3100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       3200-GRAVAR-ARQOUTZD            SECTION.
      *----------------------------------------------------------------*

           WRITE FD-ARQOUTZD           FROM    WRK-ARQOUTZD-REGISTRO.

           PERFORM 1120-TESTAR-FS-ARQOUTZD.

           ADD 1                       TO  WRK-GRAVADOS-ARQOUTZD.

      *----------------------------------------------------------------*
       3200-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       9100-FORMATAR-ERRO-ARQUIVO      SECTION.
      *----------------------------------------------------------------*

           DISPLAY '*********** @PGMID ***********'
           DISPLAY '*                              *'
           DISPLAY '*  ERRO DE ACESSO A ARQUIVO    *'
           DISPLAY '*                              *'
           DISPLAY '********************************'
           DISPLAY '* ARQUIVO     : ' WRK-NOME-ARQUIVO ' *'
           DISPLAY '* FILE STATUS : ' WRK-FILE-STATUS '       *'
           DISPLAY '********************************'

           MOVE 16 TO RETURN-CODE.

           STOP RUN.

      *----------------------------------------------------------------*
       9100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       9000-FINALIZAR                  SECTION.
      *----------------------------------------------------------------*
      *
           DISPLAY '*********** @PGMID ***********'
           DISPLAY '*                              *'
           DISPLAY '*     RESUMO PROCESSAMENTO     *'
           DISPLAY '* ---------------------------- *'
           MOVE    WRK-LIDOS-ARQINPPD   TO WRK-DISPLAY
           DISPLAY '* LIDOS    ARQINPPD : ' WRK-DISPLAY
           DISPLAY '*                              *'
           MOVE    WRK-GRAVADOS-ARQOUTZD  TO WRK-DISPLAY
           DISPLAY '* GRAVADOS ARQOUTZD : ' WRK-DISPLAY
           DISPLAY '*                              *'
           DISPLAY '*********** @PGMID ***********'

           CLOSE ARQINPPD
                 ARQOUTZD.

           PERFORM 1100-TESTAR-FILE-STATUS.

           STOP RUN.

      *----------------------------------------------------------------*
       9000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*
      *================================================================*
