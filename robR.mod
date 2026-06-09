MODULE MainModule
    LOCAL CONST string YuMi_App_Program_Version:="1.0.1";
    TASK PERS tooldata tPince3D:=[TRUE,[[-0.430664,-0.747915,115.185],[1,0,0,0]],[0.353,[7.4,2.5,22.1],[1,0,0,0],0,0,0]];
    !Do not edit or remove this line!
    !Do not edit or remove this line!
    TASK PERS tooldata tPointe3D:=[TRUE,[[-0.614658,-0.47242,144.97],[1,0,0,0]],[0.355,[7.6,2.6,25.2],[1,0,0,0],0,0,0]];
    !TASK PERS wobjdata wPlaque:=[FALSE,TRUE,"",[[220.22,127.686,8.29376],[0.703284,-0.00123052,0.000705409,-0.710907]],[[0,0,0],[1,0,0,0]]];
    TASK PERS wobjdata wPlaque:=[FALSE,TRUE,"",[[231.471,118.946,9.75126],[0.704787,-0.000962526,0.00262938,-0.709413]],[[0,0,0],[1,0,0,0]]];
    !Do not edit or remove this line!

    ! compteur PERS des coups
    PERS num NombreCoup:=6;
    ! qui jou ? BLACK:FALSE / WHITE:TRUE
    PERS bool WhosPlayingNow:=FALSE;
    !Position de synchronisation
    VAR syncident syncStep1;
    PERS tasks tsklstYUMI{2}:=[["T_ROB_R"],["T_ROB_L"]];
    ! Historique des cases prise et depot
    VAR num CasePriseR{5}:=[0,0,0,0,0];
    VAR num CaseDepotR{5}:=[0,0,0,0,0];
    ! Matrice Jeu
    PERS num MatriceJeu{2,5}:=[[0,5,0,4,2],[0,6,0,8,0]];

    ! Game finish
    PERS bool GameFinish:=TRUE;
    ! Winner
    PERS string Winner{3}:=["Black","White","NULL"];
    ! IP and Port
    !VAR string IP:="10.2.30.125";
    VAR string IP:="10.2.30.128";
    VAR num PORT:=21;
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    VAR string text;
    VAR iodev infile;
    VAR socketdev socket1;
    VAR string str_data;
    ! Matrice de la situation du jeu
    VAR num MoveIA:=0;
    TASK PERS tooldata toolPointe3D:=[TRUE,[[1.38577,0.660996,147.958],[1,0,0,0]],[0.34,[7.6,2.6,25.2],[1,0,0,0],0,0,0]];



    VAR syncident sync2;
    VAR syncident sync3;
    VAR syncident sync4;
    VAR syncident sync5;
    VAR syncident sync6;
    VAR syncident sync7;
    VAR syncident sync8;
    VAR syncident sync9;
    VAR syncident sync01;
    VAR syncident sync02;
    VAR syncident sync03;
    VAR syncident sync04;
    VAR syncident sync05;
    VAR syncident sync06;
    VAR syncident sync07;
    VAR syncident sync08;
    VAR syncident sync09;
    VAR syncident sync10;
    VAR syncident sync11;
    VAR syncident sync12;
    VAR syncident sync13;
    VAR syncident sync14;
    PERS num Inc;
    VAr num IncR2;

    !TASK PERS LogAxis log_Axis:=[FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,TRUE];
    TASK PERS LogAxis log_Axis:=[TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE];
    TASK PERS TapSpeedLim tapspeed_Limit:=[3,3,3,3,3,3,1.5];
    VAR bool Again:=TRUE;
    PROC main()
        !**********************************************************************************************
        BackupCamToCtrl HandCameraR,TRUE;
        IF Again=TRUE THEN
        StartConnection IP, PORT;
        Again:=FALSE;
        ENDIF
        !T_Init;
        MoveJ PpriseVue,v100,z50,VisionR\WObj:=wPlaque;
        !WaitForTap;
        WaitforTap\logAx:=log_Axis\tapSpdLim:=tapspeed_Limit;
        !T_PriseVue;
        Game;

        !TPReadFK reg1,"Play Again?",stEmpty,stEmpty,stEmpty,"Yes","No";
        !IF reg1=4 THEN
    
        !  TPWrite "PLAY AGAIN!";
        !   RANGE CasePriseR,CaseDepotR;
        !  T_Init;
        ! WaitSyncTask syncStep1,tsklstYUMI;
        ! Game;
        !ELSEIF reg1=5 THEN
        !  TPWrite "STOP!";
        !  RANGE CasePriseR,CaseDepotR;
        !  T_Init;
        !  WaitSyncTask syncStep1,tsklstYUMI; 
        ! ENDIF

        !**********************************************************************************************
        ! RANGEMENT 
        IncR2:=14;
        WaitSyncTask sync01,tsklstYUMI;
        FlagRANGE:=TRUE;
        !T_Init;
        ! Point de synchronisation
        T_RANGEV1_R;
        WaitSyncTask sync02,tsklstYUMI;
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{1,i}=3 THEN
                T_ECHANGE_R 3,0;
                MatriceJeu{1,i}:=0;

            ENDIF
        ENDFOR
        WaitSyncTask sync03,tsklstYUMI;
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{1,i}=6 THEN
                T_ECHANGE_R 6,0;
                MatriceJeu{1,i}:=0;
  
            ENDIF
        ENDFOR
        WaitSyncTask sync04,tsklstYUMI;
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{1,i}=9 THEN
                T_ECHANGE_R 9,0;
                MatriceJeu{1,i}:=0;

            ENDIF
        ENDFOR
        WaitSyncTask sync05,tsklstYUMI;
        !===============================================
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{2,i}=1 THEN
                T_ECHANGE_R 0,IncR2;
                IncR2:=IncR2-1;
            ENDIF
        ENDFOR
        WaitSyncTask sync06,tsklstYUMI;
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{2,i}=4 THEN
                T_ECHANGE_R 0,IncR2;
                IncR2:=IncR2-1;
            ENDIF
        ENDFOR
        WaitSyncTask sync07,tsklstYUMI;
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{2,i}=7 THEN
                T_ECHANGE_R 0,IncR2;
                IncR2:=IncR2-1;
            ENDIF
        ENDFOR
        !****************************************************
        WaitSyncTask sync08,tsklstYUMI;
       Reset Collision_Avoidance;
        ! Rangement milieu
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{2,i}=2 THEN
                T_MovePtoCase 2,IncR2;
                IncR2:=IncR2-1;
            ENDIF
        ENDFOR
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{2,i}=5 THEN
                T_MovePtoCase 5,IncR2;
                IncR2:=IncR2-1;
            ENDIF
        ENDFOR
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{2,i}=8 THEN
                T_MovePtoCase 8,IncR2;
                IncR2:=IncR2-1;
            ENDIF
        ENDFOR
    Set Collision_Avoidance;
        
        WaitSyncTask sync5,tsklstYUMI;
        T_Init;
        !stop;
    ENDPROC

    PROC Game()
        StarGame;

        WHILE GameFinish=FALSE DO
            LectureJeu;
            IF NombreCoup=1 AND GameFinish=FALSE THEN
                T_MovePtoCase 14,MoveIA;
                CasePriseR{1}:=14;
                CaseDepotR{1}:=MoveIA;
            ELSEIF NombreCoup=2 AND GameFinish=FALSE THEN
                T_MovePtoCase 13,MoveIA;
                CasePriseR{2}:=13;
                CaseDepotR{2}:=MoveIA;
            ELSEIF NombreCoup=3 AND GameFinish=FALSE THEN
                T_MovePtoCase 12,MoveIA;
                CasePriseR{3}:=12;
                CaseDepotR{3}:=MoveIA;
            ELSEIF NombreCoup=4 AND GameFinish=FALSE THEN
                T_MovePtoCase 11,MoveIA;
                CasePriseR{4}:=11;
                CaseDepotR{4}:=MoveIA;
            ELSEIF NombreCoup=5 AND GameFinish=FALSE THEN
                T_MovePtoCase 10,MoveIA;
                CasePriseR{5}:=10;
                CaseDepotR{5}:=MoveIA;
            ELSEIF NombreCoup=6 THEN
            GameFinish:=TRUE;
            ENDIF
            NombreCoup:=NombreCoup+1;
            IF NombreCoup=6 THEN
                GameFinish:=TRUE;
            ENDIF

             !WaitTime 2;
             !SocketClose socket1;
        ENDWHILE

        TPWRITE "GAME FINISHED!";
        !SocketClose socket1;
    ENDPROC

    PROC InitGame()
        reset custom_DO_0;
        NombreCoup:=1;
        WhosPlayingNow:=FALSE;
        ! Black starting
        MatriceJeu:=[[0,0,0,0,0],[0,0,0,0,0]];
        CasePriseR:=[0,0,0,0,0];
        CaseDepotR:=[0,0,0,0,0];
        GameFinish:=FALSE;
        MoveIA:=0;
        InitCameraAndGrip;
        TPErase;
        FlagRANGE:=FALSE;
        !StartConnection IP,PORT;
    ENDPROC

    PROC StarGame()
        VAR string str_start;
        VAR bool val_start;
        reset custom_DO_0;
        WaitDI custom_DI_0,1;
        InitGame;
        str_start:=Connection(IP,PORT,"D");
        IF StrToVal(str_start,val_start)=TRUE THEN
            set custom_DO_0;
        ENDIF
        !WaitDO custom_DO_0,1;
        TPWrite "GAME START!";
    ENDPROC

    PROC StartConnection(string ip2,num port2)
        SocketClose socket1;
        SocketCreate socket1;
        SocketConnect socket1,ip2,port2;
    ENDPROC

ENDMODULE