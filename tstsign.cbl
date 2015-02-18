       IDENTIFICATION DIVISION.
       PROGRAM-ID. TSTSIGN.
       AUTHOR.     flavio@casacurta.com.
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01.
           03 VAL   PIC S9(5) COMP-3 VALUE -12345.
           03 VAL-S PIC S9(5) SIGN TRAILING SEPARATE VALUE ZEROS.

       PROCEDURE DIVISION.
       PGP-MAIN SECTION.
            MOVE VAL TO VAL-S.
            DISPLAY 'VAL-S = ' VAL-S
            MULTIPLY -1 BY VAL-S
            DISPLAY 'VAL-S = ' VAL-S
           GOBACK.

      *SYSOUT
      *VAL-S = 12345-
      *VAL-S = 12345+

