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
      *                 - LER    ARQINPZD ZONADO
      *
      *                 - GRAVAR ARQOUTPD COMPACTADO
      *                   @SINAL TRATAMENTO DE SINAL
      *
      *----------------------------------------------------------------*
      *    ARQUIVOS....:                                               *
      *                DDNAME           I/O        INCLUDE/BOOK
      *                ARQINPZD          I         DECLARADO NO PGM
      *                ARQOUTPD          O         @BOOKOUT
      *----------------------------------------------------------------*
      *    BOOK'S......:                                               *
      *    @BOOKOUT - BOOK DE SAIDA
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

           SELECT ARQINPZD ASSIGN      TO   UT-S-ARQINPZD
                      FILE STATUS      IS   WRK-FS-ARQINPZD.

           SELECT ARQOUTPD ASSIGN      TO   UT-S-ARQOUTPD
                      FILE STATUS      IS   WRK-FS-ARQOUTPD.

      *================================================================*
       DATA                            DIVISION.
      *================================================================*

      *----------------------------------------------------------------*
       FILE                            SECTION.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
      *   INPUT:   ARQUIVO DE ENTRADA - ARQINPZD
      *            ORG. SEQUENCIAL    - LRECL   = @LENGTHIN
      *----------------------------------------------------------------*
       FD  ARQINPZD
           RECORDING MODE IS F
           LABEL RECORD IS STANDARD
           BLOCK CONTAINS 0 RECORDS.

       01  FD-ARQINPZD                 PIC  X(@LENGTHIN).

      *----------------------------------------------------------------*
      *   OUTPUT:  ARQUIVO DE SAIDA   - ARQOUTPD
      *            ORG. SEQUENCIAL    - LRECL   = @LENGTHOUT
      *----------------------------------------------------------------*
       FD  ARQOUTPD
           RECORDING MODE IS F
           LABEL RECORD IS STANDARD
           BLOCK CONTAINS 0 RECORDS.

       01  FD-ARQOUTPD                 PIC  X(@LENGTHOUT).

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

           03 WRK-LIDOS-ARQINPZD       PIC  9(009) COMP-3  VALUE ZEROS.
           03 WRK-GRAVADOS-ARQOUTPD    PIC  9(009) COMP-3  VALUE ZEROS.
           03 WRK-DISPLAY              PIC +Z(08)9         VALUE ZEROS.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE TESTE DE FILE-STATUS               ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  WRK-FS-ARQINPZD             PIC  X(002)         VALUE SPACES.
       01  WRK-FS-ARQOUTPD             PIC  X(002)         VALUE SPACES.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE TRATAMENTO DE ERRO DE ARQUIVOS     ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  WRK-NOME-ARQUIVO            PIC  X(008)         VALUE SPACES.
       01  WRK-FILE-STATUS             PIC  X(002)         VALUE SPACES.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE ENTRADA ARQINPZD                   ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
@LVL01BKIN
@BOOKIN

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE SAIDA ARQOUTPD                     ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
@LVL01BKOUT
       COPY @BOOKOUT.

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

           PERFORM 3000-PROCESSAR UNTIL WRK-FS-ARQOUTPD EQUAL '10'.

           PERFORM 9000-FINALIZAR.

      *----------------------------------------------------------------*
       0000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1000-INICIAR                    SECTION.
      *----------------------------------------------------------------*

           OPEN INPUT   ARQINPZD
                OUTPUT  ARQOUTPD.

           PERFORM 1100-TESTAR-FILE-STATUS.

      *----------------------------------------------------------------*
       1000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1100-TESTAR-FILE-STATUS         SECTION.
      *----------------------------------------------------------------*

           PERFORM 1110-TESTAR-FS-ARQINPZD.

           PERFORM 1120-TESTAR-FS-ARQOUTPD.

      *----------------------------------------------------------------*
       1100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1110-TESTAR-FS-ARQINPZD         SECTION.
      *----------------------------------------------------------------*

           IF  WRK-FS-ARQINPZD         NOT EQUAL  '00'
               MOVE 'ARQINPZD'         TO WRK-NOME-ARQUIVO
               MOVE WRK-FS-ARQINPZD    TO WRK-FILE-STATUS
               PERFORM 9100-FORMATAR-ERRO-ARQUIVO
           END-IF.

      *----------------------------------------------------------------*
       1110-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1120-TESTAR-FS-ARQOUTPD          SECTION.
      *----------------------------------------------------------------*

           IF  WRK-FS-ARQOUTPD         NOT EQUAL  '00'
               MOVE 'ARQOUTPD'         TO WRK-NOME-ARQUIVO
               MOVE WRK-FS-ARQOUTPD    TO WRK-FILE-STATUS
               PERFORM 9100-FORMATAR-ERRO-ARQUIVO
           END-IF.

      *----------------------------------------------------------------*
       1120-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2000-VERIFICAR-VAZIO            SECTION.
      *----------------------------------------------------------------*

           PERFORM 2100-LER-ARQINPZD.

           IF (WRK-LIDOS-ARQINPZD      EQUAL     ZEROS)
               DISPLAY '************ @PGMID ************'
               DISPLAY '*                                *'
               DISPLAY '*     ARQUIVO ARQINPZD VAZIO     *'
               DISPLAY '*       PROGRAMA ENCERRADO       *'
               DISPLAY '*                                *'
               DISPLAY '************ @PGMID ************'
               MOVE 'ARQINPZD'         TO WRK-NOME-ARQUIVO
               MOVE WRK-FS-ARQINPZD    TO WRK-FILE-STATUS
               PERFORM 9000-FINALIZAR
           END-IF.

      *----------------------------------------------------------------*
       2000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2100-LER-ARQINPZD               SECTION.
      *----------------------------------------------------------------*

           READ ARQINPZD               INTO @REGIN.

           IF WRK-FS-ARQINPZD          EQUAL     '10'
               GO TO 2100-99-FIM
           END-IF.

           PERFORM 1110-TESTAR-FS-ARQINPZD.
           ADD  1  TO   WRK-LIDOS-ARQINPZD.

      *----------------------------------------------------------------*
       2100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       3000-PROCESSAR                  SECTION.
      *----------------------------------------------------------------*

           PERFORM 3100-FORMATAR-ARQOUTPD.
           PERFORM 3200-GRAVAR-ARQOUTPD.
           PERFORM 2100-LER-ARQINPZD.

      *----------------------------------------------------------------*
       3000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       3100-FORMATAR-ARQOUTPD          SECTION.
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
       3200-GRAVAR-ARQOUTPD            SECTION.
      *----------------------------------------------------------------*

           WRITE FD-ARQOUTPD           FROM    @REGOUT.

           PERFORM 1120-TESTAR-FS-ARQOUTPD.

           ADD 1                       TO  WRK-GRAVADOS-ARQOUTPD.

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
           MOVE    WRK-LIDOS-ARQINPZD   TO WRK-DISPLAY
           DISPLAY '* LIDOS    ARQINPZD : ' WRK-DISPLAY
           DISPLAY '*                              *'
           MOVE    WRK-GRAVADOS-ARQOUTPD  TO WRK-DISPLAY
           DISPLAY '* GRAVADOS ARQOUTPD : ' WRK-DISPLAY
           DISPLAY '*                              *'
           DISPLAY '*********** @PGMID ***********'

           CLOSE ARQOUTPD
                 ARQINPZD.

           PERFORM 1100-TESTAR-FILE-STATUS.

           STOP RUN.

      *----------------------------------------------------------------*
       9000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*
      *================================================================*
